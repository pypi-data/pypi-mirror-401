from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from loguru import logger

from pyligent.common.dataset_configs import BasicCumulativeDatasetConfig
from pyligent.core.dataset import (
    CumulativeDatasetConfig,
    DiligentDataset,
    SamplingDatasetFunction,
)
from pyligent.core.explorer import Explorer
from pyligent.core.helpers.log_manager import PipelineLoggingManager
from pyligent.core.path import GoldPath, PathContext
from pyligent.core.solver import Solver
from pyligent.core.validator import Validator

EpochType = int | str
EpochKey = Literal["A", "B", "FINAL"]


@dataclass
class PipelineConfig:
    gold_paths: list[GoldPath]
    dataset_config: CumulativeDatasetConfig = field(
        default_factory=BasicCumulativeDatasetConfig
    )
    epochs_a: EpochType = 10
    epochs_b: EpochType = 10
    epochs_final: EpochType = 10
    visualize_dfs: int = 10  # How many DFS visualize (0 - all)

    def __post_init__(self):
        # Try to get en epochs number

        self._epoch_dict: dict[EpochKey, EpochType] = {
            "A": self.epochs_a,
            "B": self.epochs_b,
            "FINAL": self.epochs_final,
        }

        try:
            for v in self._epoch_dict.values():
                self._process_epoch(v, t=1)

        except Exception as e:
            raise ValueError("Error with processing epoch") from e

    def _process_epoch(
        self,
        epoch: EpochType,
        t: int,  # t is explicitly used in eval!
    ) -> int:
        if isinstance(epoch, int):
            return epoch
        return eval(epoch)

    def get_epochs(self, epoch_key: EpochKey, t: int) -> int:
        return self._process_epoch(self._epoch_dict[epoch_key], t=t)


@dataclass
class PhaseResult:
    """Encapsulates the output of a training phase"""

    phase_name: str
    t: int
    metadata: Optional[dict[str, Any]] = None


class TrainingPhase(ABC):
    """Base class for pipeline training phases"""

    @abstractmethod
    def execute(self, context: "PhaseContext") -> PhaseResult:
        """Execute the training phase and return results"""
        pass


@dataclass
class PhaseContext:
    """Shared context passed between phases"""

    solver: Solver
    validator: Validator
    explorer: Explorer
    config: PipelineConfig
    t: int
    gold_paths: list[GoldPath]
    dataset: DiligentDataset
    sampling_dataset_function: SamplingDatasetFunction
    loggers: PipelineLoggingManager


class BuildTeacherDatasetPhase(TrainingPhase):
    """Stage 0: Extract prefix-action pairs from gold paths"""

    def execute(self, context: PhaseContext) -> PhaseResult:
        # Build dataset for current depth t
        for gold_path in context.gold_paths:
            if len(gold_path) >= (context.t + 1):
                prefix = PathContext(
                    gold_path.nodes[: -context.t], gold_length=len(gold_path)
                )
                action = gold_path.nodes[-context.t].action
                context.dataset.add_gold_pair((prefix, action))

        return PhaseResult(
            phase_name="teacher_pairs",
            t=context.t,
            metadata={"source": "gold_paths"},
        )


class SupervisedFinetunePhase(TrainingPhase):
    """Supervised fine-tuning phase (SFT-A or SFT-B)"""

    def __init__(self, phase_name: str, epochs_key: EpochKey, source_description: str):
        self.phase_name = phase_name
        self.epochs_key: EpochKey = epochs_key
        self.source_description = source_description

    def execute(self, context: PhaseContext) -> PhaseResult:
        epochs = context.config.get_epochs(self.epochs_key, t=context.t)

        logger.log(
            "TITLE",
            f"{self.phase_name} on {len(context.dataset)} examples for {epochs} epochs",
        )

        # Execute fine-tuning
        context.solver.finetune(
            context.sampling_dataset_function,
            phase=self.phase_name,
            t=context.t,
            epochs=epochs,
        )

        return PhaseResult(
            phase_name=self.phase_name,
            t=context.t,
            metadata={"epochs": epochs, "source": self.source_description},
        )


class ExplorationPhase(TrainingPhase):
    """Stage 2: DFS exploration with bounded search"""

    def execute(self, context: PhaseContext) -> PhaseResult:
        logger.log("TITLE", f"Exploration on {len(context.dataset)} examples")

        # Reset exploration state (no-op if disabled)
        context.loggers.reset_exploration_phase(context.t)

        results = context.explorer.explore(context.dataset, t=context.t)

        # Visualization (no-op if disabled)
        context.loggers.visualize_exploration(
            dataset=context.dataset,
            results=results,
            step_t=context.t,
            visualize_dfs=context.config.visualize_dfs,
        )

        Explorer.add_to_dataset(context.dataset, results)

        # Log exploration results (no-op if disabled)
        context.loggers.log_phase_pairs(
            phase="SFT-B",
            t=context.t,
            dataset=context.dataset,
            source="exploration",
        )

        return PhaseResult(
            phase_name="exploration",
            t=context.t,
            metadata={
                "num_trajectories": len(results),
                "total_pairs": len(context.dataset),
            },
        )
