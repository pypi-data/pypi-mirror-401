from itertools import islice
from pathlib import Path
from typing import Optional

from loguru import logger

from pyligent.core.dataset import CumulativeDiligentDataset, DiligentDataset
from pyligent.core.explorer import Explorer
from pyligent.core.helpers.log_manager import (
    PipelineLoggingConfig,
    PipelineLoggingManager,
)
from pyligent.core.helpers.pipeline_components import (
    BuildTeacherDatasetPhase,
    ExplorationPhase,
    PhaseContext,
    PipelineConfig,
    SupervisedFinetunePhase,
)
from pyligent.core.solver import Solver
from pyligent.core.validator import Validator


class Pipeline:
    """Orchestrates the Diligent Learner training pipeline"""

    def __init__(
        self,
        solver: Solver,
        validator: Validator,
        explorer: Explorer,
        output_dir: Path | str,
        visualizer_kwargs: Optional[dict] = None,
        *,
        # Preferred: pass a fully constructed manager from the script.
        loggers: Optional[PipelineLoggingManager] = None,
        # Optional: allow Pipeline to construct the manager if not injected.
        logger_config: Optional[PipelineLoggingConfig] = None,
    ):
        self.solver = solver
        self.validator = validator
        self.explorer = explorer
        self.log_dir = Path(output_dir)

        # Logging: choose exactly ONE source of truth.
        if loggers is not None:
            self.loggers = loggers
        else:
            if logger_config is None:
                raise ValueError(
                    "Either `loggers` must be provided, or `logger_config` must be provided."
                )
            self._setup_logging(
                logger_config=logger_config,
                visualizer_kwargs=visualizer_kwargs,
            )

        # Phase registry
        self._setup_phases()

        # Explorer wiring (duck-typed logger interface)
        self.explorer.build(self.solver, self.validator)
        self.explorer.set_training_logger(self.loggers)

        # Validator hook logs live under the same manager
        self.loggers.setup_validator_logging_hooks(self.validator)

        logger.info(f"Detailed training log file: {self.loggers.training_log_path}")

    def _setup_logging(
        self,
        *,
        logger_config: PipelineLoggingConfig,
        visualizer_kwargs: Optional[dict] = None,
    ) -> None:
        """
        Initialize all logging sinks through a single manager.

        """
        if hasattr(self, "loggers") and self.loggers is not None:
            raise RuntimeError(
                "_setup_logging() was called but `self.loggers` is already initialized."
            )

        self.loggers = PipelineLoggingManager(
            log_dir=self.log_dir,
            solver_out_dir=self.solver.out_dir,
            time_stamp=self.solver.time_stamp,
            config=logger_config,
            visualizer_kwargs=visualizer_kwargs,
        )

    def _setup_phases(self):
        """Register training phases in execution order."""
        self.phases = {
            "build_teacher": BuildTeacherDatasetPhase(),
            "sft_a": SupervisedFinetunePhase("SFT-A", "A", "teacher"),
            # IMPORTANT: this assumes you already refactored ExplorationPhase
            # to NOT take DFSVisualizer/log_dir in constructor, and instead call
            # context.loggers.visualize_exploration(...).
            "exploration": ExplorationPhase(),
            "sft_b": SupervisedFinetunePhase("SFT-B", "B", "cumulative"),
            "final": SupervisedFinetunePhase("Final", "FINAL", "full"),
        }

    def _setup_phases(self):
        self.phases = {
            "build_teacher": BuildTeacherDatasetPhase(),
            "sft_a": SupervisedFinetunePhase("SFT-A", "A", "teacher"),
            "exploration": ExplorationPhase(),
            "sft_b": SupervisedFinetunePhase("SFT-B", "B", "cumulative"),
            "final": SupervisedFinetunePhase("Final", "FINAL", "full"),
        }

    def run(self, config: PipelineConfig) -> CumulativeDiligentDataset:
        """Execute the complete training pipeline"""
        max_chain_length = max(len(g) for g in config.gold_paths)
        self.cumulative_dataset: CumulativeDiligentDataset = (
            config.dataset_config.create_dataset()
        )

        # Reverse curriculum: iterate from depth 1 to max_chain_length
        for t in range(1, max_chain_length):
            logger.log("SECTION", f"Pipeline iteration t={t}/{max_chain_length - 1}")

            # Create shared context for this iteration
            context = PhaseContext(
                solver=self.solver,
                validator=self.validator,
                explorer=self.explorer,
                config=config,
                t=t,
                gold_paths=config.gold_paths,
                dataset=self.cumulative_dataset.at(t),
                sampling_dataset_function=lambda t=t: self.cumulative_dataset.at(t),
                loggers=self.loggers,
            )

            # Execute training pipeline for depth t
            self._execute_iteration(context)

        # Final training phase on complete dataset
        self._execute_final_phase(context, max_chain_length)

        return self.cumulative_dataset

    def _execute_iteration(self, context: PhaseContext):
        """Execute one iteration of the reverse curriculum"""

        # Stage 0: Build teacher dataset
        self.phases["build_teacher"].execute(context)
        self._log_pairs_sample(context.dataset, f"SFT-A teacher pairs @ t={context.t}")

        # Stage 1: SFT-A on teacher pairs
        context.dataset = self.cumulative_dataset.sample(only_gold=True, t=context.t)
        context.sampling_dataset_function = (
            lambda t=context.t: self.cumulative_dataset.sample(only_gold=True, t=t)
        )
        self.phases["sft_a"].execute(context)

        # Stage 2: Exploration phase
        context.dataset = self.cumulative_dataset.at(context.t)  # Only golden pairs
        self.phases["exploration"].execute(context)

        # Stage 3: SFT-B on combined dataset
        context.dataset = self.cumulative_dataset.sample(only_gold=False, t=context.t)
        context.sampling_dataset_function = (
            lambda t=context.t: self.cumulative_dataset.sample(only_gold=False, t=t)
        )
        self.phases["sft_b"].execute(context)

    def _execute_final_phase(self, context: PhaseContext, max_chain_length: int):
        """Execute final fine-tuning on complete dataset"""
        context.t = max_chain_length
        context.dataset = self.cumulative_dataset.sample_from(
            self.cumulative_dataset.composite
        )
        composite_dataset = self.cumulative_dataset.composite
        context.sampling_dataset_function = (
            lambda d=composite_dataset: self.cumulative_dataset.sample_from(d)
        )
        self.phases["final"].execute(context)

    def _log_pairs_sample(self, dataset: DiligentDataset, title: str, k: int = 3):
        self.loggers.title(f"{title} (first {k})")
        for prefix, action in islice(dataset.pairs, k):
            path_str = " | ".join(n.action.info_str for n in prefix.nodes)
            gold_str = action.info_str
            self.loggers.info(f"\n(PATH):\t{path_str}\nGOLD:\t{gold_str}")
