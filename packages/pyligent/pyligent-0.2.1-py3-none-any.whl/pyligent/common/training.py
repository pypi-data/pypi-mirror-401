import argparse
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, Protocol, TypeVar

import yaml
from loguru import logger

from pyligent.common.config import ScriptConfig, save_config, setup_environment
from pyligent.common.utils.logger import setup_logging
from pyligent.core import Pipeline, PipelineConfig, Solver
from pyligent.core.path import GoldPath


def parse_arguments(default_config_path: Optional[str] = None) -> argparse.Namespace:
    """Parse command-line arguments for training scripts."""
    parser = argparse.ArgumentParser(description="Diligent Learner Training")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to user configuration file (overrides default)",
    )
    parser.add_argument(
        "--default",
        type=Path,
        default=Path(default_config_path)
        if default_config_path
        else Path("configs/train/default.yaml"),
        help="Path to default configuration file",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (overrides config)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=None,
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--save-steps",
        type=int,
        default=None,
        help="Checkpoint save steps (overrides config)",
    )
    parser.add_argument(
        "--mistakes-file",
        type=Path,
        default=None,
        help="Path to mistakes file for exclusion",
    )
    return parser.parse_args()


def save_training_artifacts(
    solver: Solver,
    cumulative_dataset,
    config: ScriptConfig,
    gen_cfg: dict,
    gold_paths: list[GoldPath],
    output_dir: Path,
):
    """Save training artifacts to output directory."""
    logger.log("SECTION", "Saving Training Artifacts")

    # Save final model
    logger.info("Saving final model...")
    model_save_path = output_dir / "final_model"
    try:
        solver.save(
            output_dir=model_save_path,
            metadata={
                "num_train_examples": len(gold_paths),
                "final_dataset_size": len(cumulative_dataset),
                "epochs_a": config.training.epochs_a,
                "epochs_b": config.training.epochs_b,
                "epochs_final": config.training.epochs_final,
                "B": config.exploration.B,
                "Tmax": config.exploration.Tmax,
                "c_leaf": config.exploration.c_leaf,
            },
        )

    except Exception as e:
        logger.warning(f"Failed to save model: {e}")

    # Save composite dataset (optional; can be large)
    if config.logging.save_composite_dataset:
        logger.info("Saving composite dataset...")
        try:
            composite_dataset = cumulative_dataset.composite
            with open(output_dir / "composite_dataset.txt", "w", encoding="utf-8") as f:
                for ctx, action in composite_dataset:
                    f.write(f"Context: {ctx}\n")
                    f.write(f"Action: {action}\n")
                    f.write("-" * 80 + "\n")
        except Exception as e:
            logger.warning(f"Failed to save composite dataset: {e}")
    else:
        logger.info("Skipping composite dataset dump (save_composite_dataset=false).")

    # Save generation config
    try:
        with open(output_dir / "generation_config.yaml", "w", encoding="utf-8") as f:
            yaml.dump(gen_cfg, f, default_flow_style=False)
    except Exception as e:
        logger.warning(f"Failed to save generation config: {e}")

    # Save gold paths summary (optional)
    if config.logging.save_gold_paths_summary:
        logger.info("Saving gold paths summary...")
        try:
            with open(output_dir / "gold_paths_summary.txt", "w", encoding="utf-8") as f:
                f.write(f"Total gold paths: {len(gold_paths)}\n")
                for i, gp in enumerate(gold_paths[:10], 1):
                    f.write(f"\nGold Path {i}:\n")
                    f.write(f"Length: {len(gp)} nodes\n")
                    f.write(f"First action: {gp.nodes[0].action}\n")
                    if len(gp) > 1:
                        f.write(f"Last action: {gp.nodes[-1].action}\n")
        except Exception as e:
            logger.warning(f"Failed to save gold paths summary: {e}")
    else:
        logger.info("Skipping gold paths summary (save_gold_paths_summary=false).")

    logger.info(f"All artifacts saved to {output_dir}\n")


def setup_output_directory(config: ScriptConfig) -> Path:
    """
    Setup timestamped output directory.

    Args:
        config: Script configuration

    Returns:
        Path to created output directory
    """
    base_output_dir = Path(config.logging.output_dir)
    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = base_output_dir / f"run_{run_timestamp}"
    suffix = 1
    while run_dir.exists():
        run_dir = base_output_dir / f"run_{run_timestamp}_{suffix:02d}"
        suffix += 1

    run_dir.mkdir(parents=True, exist_ok=True)
    config.logging.output_dir = run_dir
    return run_dir


# Protocol for component factory to support covariance
TConfig = TypeVar("TConfig", bound=ScriptConfig)


class ComponentFactory(Protocol[TConfig]):
    """Protocol for component initialization factories."""

    def __call__(
        self, config: TConfig, output_dir: Path
    ) -> tuple[list[GoldPath], Solver, Pipeline, dict]:
        """
        Initialize task-specific components.

        Args:
            config: Task-specific configuration
            output_dir: Output directory for checkpoints

        Returns:
            tuple of (gold_paths, solver, pipeline, gen_cfg)
        """
        ...


def generic_training_loop(
    config: TConfig,
    components_factory: ComponentFactory[TConfig],
    task_name: str = "Training",
) -> None:
    """
    Generic training loop that works for any task.

    Args:
        config: Complete script configuration
        components_factory: Function that initializes task-specific components
        task_name: Name of the task for logging (e.g., "Sudoku", "GSM8K")
    """
    # Setup output directory
    output_dir = setup_output_directory(config)

    # Setup logging
    setup_logging(
        level=config.logging.level,
        log_file=config.logging.output_dir / config.logging.log_file,
    )

    # Setup environment (env vars, warnings)
    setup_environment(config)

    # Persist resolved config
    save_config(config, output_dir / "config.yaml")

    # Log header
    logger.log("SECTION", f"Diligent Learner Training on {task_name} with QLoRA")
    logger.info(f"Model: {config.model.model_name}")
    logger.info(f"QLoRA: {config.model.use_qlora}")
    logger.info(f"BF16: {config.model.bf16}")
    logger.info(f"Output directory: {config.logging.output_dir}")
    logger.info("")

    # Initialize task-specific components
    try:
        gold_paths, solver, pipeline, gen_cfg = components_factory(config, output_dir)
    except Exception as e:
        logger.error(f"Component initialization failed: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Run pipeline
    logger.info("Running Pipeline...")
    logger.info("Training configuration:")
    logger.info(f"\tSFT-A epochs: {config.training.epochs_a}")
    logger.info(f"\tSFT-B epochs: {config.training.epochs_b}")
    logger.info(f"\tFinal epochs: {config.training.epochs_final}")
    logger.info("")

    try:
        # Create pipeline config
        pipeline_config = PipelineConfig(
            gold_paths=gold_paths,
            epochs_a=config.training.epochs_a,
            epochs_b=config.training.epochs_b,
            epochs_final=config.training.epochs_final,
            visualize_dfs=config.logging.visualize_dfs,
            dataset_config=config.dataset,
        )

        # Add eval_hook only if logging level is INFO
        if config.logging.level == "INFO":
            # The actual eval_hook signature depends on the Pipeline implementation
            # If you need custom logging, implement it in the pipeline or use callbacks
            pass

        cumulative_dataset = pipeline.run(pipeline_config)

        logger.log(
            "SECTION",
            "Training completed successfully!\n"
            f"Final dataset size: {len(cumulative_dataset)} examples",
        )

        # Save artifacts
        save_training_artifacts(
            solver,
            cumulative_dataset,
            config,
            gen_cfg,
            gold_paths,
            config.logging.output_dir,
        )

    except Exception as e:
        logger.error(f"Training failed with error: {e}")
        traceback.print_exc()
        sys.exit(1)
