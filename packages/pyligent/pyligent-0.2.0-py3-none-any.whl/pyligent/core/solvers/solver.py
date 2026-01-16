from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Literal, Optional, override

import torch
from datasets import Dataset
from loguru import logger
from peft import LoraConfig
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    PreTrainedModel,
    StoppingCriteriaList,
    StopStringCriteria,
)
from trl.trainer.sft_config import SFTConfig
from trl.trainer.sft_trainer import SFTTrainer

from pyligent.common.tensorboard_logger import (
    TensorBoardPerformanceLogger,
    TensorBoardPhaseLogger,
)
from pyligent.core import DiligentDataset, SamplingDatasetFunction, Solver
from pyligent.core.action import Action
from pyligent.core.path import PathContext


# ============================================================================
# Tokens config
# ============================================================================
@dataclass
class DiligentTokensConfig:
    node_start: str = "<node>"
    node_end: str = "</node>"
    backtrack_start: str = "<backtrack>"
    backtrack_end: str = "</backtrack>"
    done_start: str = "<done>"
    done_end: str = "</done>"
    stopping_tokens: list[str] = field(default_factory=list)

    def __post_init__(self):
        if len(self.stopping_tokens) == 0:
            self.stopping_tokens = [self.node_end, self.backtrack_end, self.done_end]

    def get_all_special_tokens(self) -> list[str]:
        return [
            self.node_start,
            self.node_end,
            self.backtrack_start,
            self.backtrack_end,
            self.done_start,
            self.done_end,
        ]


# ============================================================================
# Dtype pyligent.common.utils
# ============================================================================
def ensure_dtype_consistency(model: PreTrainedModel, target_dtype: torch.dtype):
    """
    Casts input/output embeddings and lm_head instances (on model, base_model,
    and base_model.model if present) to target_dtype with concise summary logging.
    """
    casted = []

    # Embeddings (via getters, as some pyligent.cores only expose methods)
    try:
        if hasattr(model, "get_input_embeddings"):
            emb = model.get_input_embeddings()
            if emb is not None:
                emb.to(target_dtype)
                casted.append("input_embeddings")
    except Exception:
        pass

    try:
        if hasattr(model, "get_output_embeddings"):
            oemb = model.get_output_embeddings()
            if oemb is not None:
                oemb.to(target_dtype)
                casted.append("output_embeddings")
    except Exception:
        pass

    # Potential lm_head locations: model, base_model, base_model.model
    roots = [
        (model, "model"),
        (getattr(model, "base_model", None), "base_model"),
        (getattr(getattr(model, "base_model", None), "model", None), "base_model.model"),
    ]

    for root, rname in roots:
        if root is None:
            continue
        try:
            lm = getattr(root, "lm_head", None)
            if lm is not None:
                lm.to(target_dtype)
                casted.append(f"{rname}.lm_head")
        except Exception:
            pass

    # if casted:
    #     logger.debug(f"casted to {target_dtype}: {', '.join(casted)}")
    # else:
    #     logger.debug(f"no dtype casts applied (target={target_dtype})")


def _register_lm_head_input_cast_hook(
    linear_module: torch.nn.Module,
) -> torch.utils.hooks.RemovableHandle:
    """
    Ensures the input tensor to lm_head matches its weight dtype.
    """

    def _pre_hook(mod, inputs):
        if not inputs:
            return inputs
        x = inputs[0]
        if isinstance(x, torch.Tensor):
            tgt = mod.weight.dtype
            if x.dtype != tgt:
                x = x.to(tgt)
                return (x,) + inputs[1:]
        return inputs

    return linear_module.register_forward_pre_hook(_pre_hook)


def apply_lm_head_cast_hooks(
    model: PreTrainedModel,
) -> List[torch.utils.hooks.RemovableHandle]:
    """
    Applies a single pre-forward input-cast hook to each distinct torch.nn.Linear
    lm_head discovered on model, base_model, and base_model.model.
    """
    hooks: List[torch.utils.hooks.RemovableHandle] = []
    seen: List[torch.nn.Module] = []

    roots = [
        model,
        getattr(model, "base_model", None),
        getattr(getattr(model, "base_model", None), "model", None),
    ]

    for root in roots:
        if root is None:
            continue
        try:
            lm = getattr(root, "lm_head", None)
            if isinstance(lm, torch.nn.Linear) and lm not in seen:
                hooks.append(_register_lm_head_input_cast_hook(lm))
                seen.append(lm)
        except Exception:
            pass

    # logger.debug(f"applied {len(hooks)} lm_head input-cast hook(s)")
    return hooks


# ============================================================================
# LlmSolver
# ============================================================================
class LlmSolver(Solver):
    _DEFAULT_SYS = (
        "You must output exactly ONE next action using one of these forms:\n"
        " <node>ID STEP_TEXT</node>\n"
        # " <backtrack>ID</backtrack>\n"
        " <done>FINAL_ANSWER</done>\n\n"
        "Never emit <backtrack>; backtracking is handled separately.\n"
        "Emit ONLY the tag. No commentary or reasoning."
    )

    _DEFAULT_USER = "PATH:\n{ctx}\n\nNext action?"

    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-0.6B",
        use_qlora: bool = True,
        bf16: bool = True,
        lr: float = 2e-5,
        max_seq_len: int = 2048,
        out_dir: Path = Path("output"),
        gen_cfg: Optional[dict] = None,
        checkpoint_save_strategy: str = "steps",
        checkpoint_save_steps: int = 100,
        checkpoint_save_total_limit: int = 5,
        chat_mode: Literal["user", "assistant"] = "user",
        system_prompt: Optional[str] = None,
        user_prompt: Optional[str] = None,
        use_k_sequences: bool = True,
    ):
        """Initialize the QwenSolver with configurable fine-tuning setup."""
        super().__init__(out_dir)
        self.chat_mode = chat_mode
        self.system_prompt: str = system_prompt or self._DEFAULT_SYS
        self.user_prompt: str = user_prompt or self._DEFAULT_USER
        self.model_name = model_name
        self.use_qlora = use_qlora
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dtype = (
            torch.bfloat16 if bf16 and torch.cuda.is_available() else torch.float16
        )

        self.lr = lr
        self.bf16 = bf16
        self.use_k_sequences = use_k_sequences

        # Initialize tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, use_fast=True, padding_side="left"
        )

        # Qwen models don't have a BOS token by default, only EOS
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            logger.info(f"Set pad_token to eos_token: {self.tokenizer.eos_token}")

        # Explicitly set BOS token to None if it doesn't exist (Qwen behavior)
        if self.tokenizer.bos_token is None:
            # Qwen models intentionally don't use BOS tokens
            logger.info(f"{self.model_name} model has no BOS token (this is expected)")

        # Load model with quantization
        logger.info(f"Loading model '{model_name}' with QLoRA={use_qlora}, BF16={bf16}")
        quant_cfg = None
        device_map = "auto"

        if use_qlora and torch.cuda.is_available():
            quant_cfg = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=self.dtype,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )
            device_map = {"": torch.cuda.current_device()}

        self.model: PreTrainedModel = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            dtype=self.dtype,
            quantization_config=quant_cfg,
        )

        ensure_dtype_consistency(self.model, self.dtype)
        self._lm_head_hooks = apply_lm_head_cast_hooks(self.model)

        self.model.config.pad_token_id = self.tokenizer.pad_token_id
        self.model.config.eos_token_id = self.tokenizer.eos_token_id
        self.model.config.bos_token_id = self.tokenizer.bos_token_id

        if (
            hasattr(self.model, "generation_config")
            and self.model.generation_config is not None
        ):
            gen_conf = self.model.generation_config
            gen_conf.pad_token_id = self.tokenizer.pad_token_id
            gen_conf.bos_token_id = self.tokenizer.bos_token_id  # Set to None for Qwen

        config = DiligentTokensConfig()
        self._stopping_criteria = StoppingCriteriaList(
            [
                StopStringCriteria(
                    tokenizer=self.tokenizer, stop_strings=config.stopping_tokens
                )
            ]
        )
        self.lora_cfg = self._build_lora_config()
        self.sft_cfg = self._build_sft_config(
            self.out_dir,
            lr,
            max_seq_len,
            self.time_stamp,
            bf16,
            checkpoint_save_steps,
            checkpoint_save_strategy,
            checkpoint_save_total_limit,
        )
        self.gen_cfg = self._default_gen_cfg(gen_cfg)
        self.trainer: Optional[SFTTrainer] = None
        self.trainer_phase_callback = TensorBoardPhaseLogger(
            self.out_dir, self.time_stamp
        )
        self.trainer_performance_callback = TensorBoardPerformanceLogger(
            self.out_dir, self.time_stamp
        )
        logger.info("✓ LlmSolver initialized successfully.\n")

        # NOTE: Just because they make me nervous
        try:
            logging.getLogger("trl").setLevel(logging.WARNING)
            logging.getLogger("transformers").setLevel(logging.WARNING)
        except:
            pass

    @staticmethod
    def _build_lora_config() -> LoraConfig:
        """Build LoRA configuration for parameter-efficient fine-tuning."""
        return LoraConfig(
            r=16,
            lora_alpha=32,
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
            target_modules=[
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
            ],
        )

    @staticmethod
    def _build_sft_config(
        out_dir: Path,
        lr: float,
        max_seq_len: int,
        time_stamp: str,
        bf16: bool = True,
        save_steps: int = 100,
        save_strategy: str = "steps",
        save_total_limit: int = 5,
    ) -> SFTConfig:
        """Build supervised fine-tuning configuration."""
        return SFTConfig(
            output_dir=str(out_dir / "checkpoints"),
            logging_dir=str(out_dir / "tensorboard_logs" / time_stamp),
            num_train_epochs=1,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=8,
            learning_rate=lr,
            logging_steps=10,
            save_steps=save_steps,
            save_strategy=save_strategy,
            save_total_limit=save_total_limit,
            warmup_ratio=0.03,
            bf16=bf16 and torch.cuda.is_available(),
            fp16=False,
            max_length=max_seq_len,
            packing=False,
            completion_only_loss=True,
            gradient_checkpointing=True,
            gradient_checkpointing_kwargs={"use_reentrant": False},
            lr_scheduler_type="cosine",
            weight_decay=0.01,
            dataloader_num_workers=0,
            remove_unused_columns=False,
            report_to=["tensorboard"],
        )

    @staticmethod
    def _default_gen_cfg(overrides: Optional[dict]) -> dict:
        """Build default generation configuration."""
        cfg = dict(
            max_new_tokens=256,
            min_new_tokens=3,
            do_sample=True,
            top_p=0.8,
            temperature=0.7,
            top_k=20,
            min_p=0.0,
            repetition_penalty=1.0,
        )
        if overrides:
            cfg.update(overrides)
        return cfg

    def _ctx_text(self, ctx: PathContext) -> str:
        """Convert PathContext to text representation."""
        return "\n".join(str(node.action) for node in ctx.nodes) if ctx else ""

    def _reapply_hooks_if_needed(self):
        """Re-apply lm_head hooks if model was wrapped/replaced."""
        if not hasattr(self, "_lm_head_hooks") or not self._lm_head_hooks:
            self._lm_head_hooks = apply_lm_head_cast_hooks(self.model)

    def _pairs_to_ds(self, dataset: DiligentDataset) -> Dataset:
        """Convert DiligentDataset pairs to HuggingFace Dataset."""
        rows = []
        for ctx, act in dataset.pairs:
            ctx_text = self._ctx_text(ctx)

            if self.chat_mode == "user":  # Standard approach
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt.format(ctx=ctx_text)},
                    {"role": "assistant", "content": str(act)},
                ]
                prompt_text = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=False,
                    enable_thinking=False,
                )

            elif self.chat_mode == "assistant":
                asistant_content = (
                    "\n".join(str(node.action) for node in ctx.nodes[1:]) if ctx else ""
                )
                asistant_content += f"\n{str(act)}"
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": str(ctx[0].action)},
                    {
                        "role": "assistant",
                        "content": asistant_content,
                    },
                ]
                prompt_text = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    enable_thinking=False,
                    # continue_final_message=not isinstance(act, DoneAction),
                    continue_final_message=False,
                )
            else:
                RuntimeError(f"Unknown chat mode `{self.chat_mode}`!")

            rows.append({"text": prompt_text})
        return Dataset.from_list(rows)

    def finetune(
        self,
        dataset_sampling_function: SamplingDatasetFunction,
        epochs: int,
        t: int,
        eval_dataset: Optional[Dataset] = None,
        phase: str = "SFT-A",
        **kwargs,
    ):
        """
        Fine-tune the model with automatic dataset resampling per epoch.

        Args:
            dataset_samplig_function: Callable that returns a DiligentDataset
            epochs: Number of training epochs
            eval_dataset: Optional evaluation dataset
            phase: Training phase identifier for logging
            t: Time step identifier for logging
        """
        self.trainer_phase_callback.set_phase(phase, t)

        # Train epoch by epoch with resampling
        for epoch in range(epochs):
            # Sample fresh dataset for this epoch
            dataset = dataset_sampling_function()
            train_ds = self._pairs_to_ds(dataset)

            # Configure for single epoch
            self.sft_cfg.num_train_epochs = 1

            # Create trainer for this epoch
            self.trainer = SFTTrainer(
                model=self.model,
                processing_class=self.tokenizer,
                args=self.sft_cfg,
                peft_config=self.lora_cfg
                if epoch == 0
                else None,  # Only apply LoRA on first epoch
                train_dataset=train_ds,
                eval_dataset=eval_dataset,
            )

            ensure_dtype_consistency(self.trainer.model, self.dtype)  # ty:ignore[invalid-argument-type]

            # Add callbacks
            self.trainer.add_callback(self.trainer_phase_callback)
            self.trainer.add_callback(self.trainer_performance_callback)

            # Train for one epoch
            self.trainer.train()
            self.trainer.accelerator.wait_for_everyone()

            # Update model reference
            self.model = self.trainer.model  # type: ignore

            # Re-ensure dtype and hooks
            ensure_dtype_consistency(self.model, self.dtype)
            self._lm_head_hooks = apply_lm_head_cast_hooks(self.model)

        logger.success("✓ Training completed for all epochs!\n")

    def propose_actions(
        self, contexts: list[PathContext], max_actions: int = 0
    ) -> tuple[list[list[Action | str]], int]:
        if self.use_k_sequences:
            return self._propose_actions_k_sequences(contexts, max_actions=max_actions)
        return self._propose_actions_1_sequence_loop(contexts, max_actions=max_actions)

    def _prepare_inputs(self, contexts: list[PathContext]):
        # model inference toggles
        self.model.eval()
        if hasattr(self.model, "gradient_checkpointing_disable"):
            self.model.gradient_checkpointing_disable()
        if hasattr(self.model.config, "use_cache"):
            self.model.config.use_cache = True

        if not contexts:
            return None, []

        prompt_texts = []
        for ctx in contexts:
            ctx_text = self._ctx_text(ctx)

            if self.chat_mode == "user":
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt.format(ctx=ctx_text)},
                ]
                prompt_text = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True,
                    enable_thinking=False,
                )
            elif self.chat_mode == "assistant":
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": str(ctx[0].action)},
                    {
                        "role": "assistant",
                        "content": "\n".join(str(node.action) for node in ctx.nodes[1:])
                        if ctx
                        else "",
                    },
                ]
                prompt_text = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    enable_thinking=False,
                    continue_final_message=True,
                )
            else:
                raise RuntimeError(f"Unknown chat mode `{self.chat_mode}`!")

            prompt_texts.append(prompt_text)

        device = next(self.model.parameters()).device
        inputs = self.tokenizer(prompt_texts, return_tensors="pt", padding=True).to(
            device
        )
        return inputs, prompt_texts

    def _sampling_gen_cfg(self, K: int) -> dict:
        gen_cfg = dict(self.gen_cfg)
        gen_cfg.pop("num_return_sequences", None)

        # Sampling-based defaults (override via self.gen_cfg as desired)
        gen_cfg["do_sample"] = True
        gen_cfg.setdefault("temperature", 0.8)
        gen_cfg.setdefault("top_p", 0.9)
        gen_cfg.setdefault("top_k", 50)

        # Keep sampling-only unless you intentionally mix with beams
        gen_cfg["num_beams"] = 1

        gen_cfg["num_return_sequences"] = K
        return gen_cfg

    def _propose_actions_k_sequences(
        self, contexts: list[PathContext], max_actions: int = 0
    ) -> tuple[list[list[Action | str]], int]:
        """Single call: num_return_sequences=K (fast, higher peak memory)."""
        solver_calls = 0
        inputs, _ = self._prepare_inputs(contexts)
        if inputs is None:
            return ([], solver_calls)

        K = max(1, int(max_actions) if max_actions else 1)
        gen_cfg = self._sampling_gen_cfg(K=K)
        prompt_len = inputs["input_ids"].shape[1]

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                **gen_cfg,
                stopping_criteria=self._stopping_criteria,
                tokenizer=self.tokenizer,
            )  # ty:ignore[call-non-callable]
            solver_calls += 1

        new_tokens = outputs[:, prompt_len:]
        decoded = self.tokenizer.batch_decode(new_tokens, skip_special_tokens=True)

        # decoded is length N*K -> reshape to N lists of K items
        N = len(contexts)
        batched_actions: list[list[Action | str]] = [
            decoded[i * K : (i + 1) * K] for i in range(N)
        ]

        del inputs, outputs, new_tokens
        torch.cuda.empty_cache()
        return (batched_actions, solver_calls)

    def _propose_actions_1_sequence_loop(
        self, contexts: list[PathContext], max_actions: int = 0
    ) -> tuple[list[list[Action | str]], int]:
        """K calls: num_return_sequences=1 (lower peak memory, slower)."""
        solver_calls = 0
        inputs, _ = self._prepare_inputs(contexts)
        if inputs is None:
            return ([], solver_calls)

        K = max(1, int(max_actions) if max_actions else 1)
        gen_cfg = self._sampling_gen_cfg(K=1)  # always 1 here
        prompt_len = inputs["input_ids"].shape[1]

        all_generated_outputs: list[list[str]] = []

        with torch.inference_mode():
            for k in range(K):
                outputs = self.model.generate(
                    **inputs,
                    **gen_cfg,
                    stopping_criteria=self._stopping_criteria,
                    tokenizer=self.tokenizer,
                )  # ty:ignore[call-non-callable]
                solver_calls += 1

                new_tokens = outputs[:, prompt_len:]
                decoded_batch = self.tokenizer.batch_decode(
                    new_tokens, skip_special_tokens=True
                )
                all_generated_outputs.append(decoded_batch)

                del outputs, new_tokens
                if k < K - 1:
                    torch.cuda.empty_cache()

        # transpose: K x N -> N x K
        N = len(contexts)
        batched_actions: list[list[Action | str]] = [
            [all_generated_outputs[k][i] for k in range(K)] for i in range(N)
        ]

        del inputs, all_generated_outputs
        torch.cuda.empty_cache()
        return (batched_actions, solver_calls)

    @override
    def save(self, output_dir: Path, metadata: Optional[dict] = None):
        if self.model is None:
            logger.error("Solver model is None")
            raise RuntimeError("Solver model is None")

        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving model checkpoint to {output_dir}...")

        # Save model (unwrap if using adapter)
        if hasattr(self.model, "merge_and_unload"):
            merged_model = self.model.merge_and_unload()  # type: ignore
            merged_model.save_pretrained(output_dir)
            logger.success("✓ Model saved (LoRA merged)")
        else:
            self.model.save_pretrained(output_dir)
            logger.success("✓ Model saved")

        # Save tokenizer
        self.tokenizer.save_pretrained(output_dir)
        logger.success("✓ Tokenizer saved")

        # Save metadata
        training_metadata = {
            "model_name": self.model_name,
            "use_qlora": self.use_qlora,
            "bf16": self.bf16,
            "lr": self.lr,
            "gen_cfg": self.gen_cfg,
        }

        if metadata:
            training_metadata.update(metadata)
        metadata_file = output_dir / "training_metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        logger.success(f"✓ Metadata saved to {metadata_file}")

        logger.success(f"✓ Complete checkpoint saved to {output_dir}")
