from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pyligent.common.dataset_implementations import (
    BasicDataset,
    RandomSamplingCumulativeDataset,
    ReplayCumulativeDataset,
)
from pyligent.core.dataset import (
    CumulativeDatasetConfig,
    CumulativeDiligentDataset,
)

# ============================================================================
# BASIC DATASET
# ============================================================================


@dataclass
class BasicCumulativeDatasetConfig(CumulativeDatasetConfig):
    """Config for basic cumulative dataset."""

    check_unique: bool = True
    dataset_type: str = "basic"

    def create_dataset(self) -> CumulativeDiligentDataset:
        """Create basic cumulative dataset instance."""
        return CumulativeDiligentDataset(
            child_class=BasicDataset,
            check_unique=self.check_unique,
        )


# ============================================================================
# REPLAY BUFFER DATASET
# ============================================================================


@dataclass
class ReplayCumulativeDatasetConfig(CumulativeDatasetConfig):
    """Config for replay buffer dataset."""

    dataset_type: str = "replay_buffer"
    check_unique: bool = False
    replay_ratio_gold: float = 2.0
    replay_ratio_exploration: float = 2.0
    allow_duplicates_on_sampling: bool = False
    seed: Optional[int] = None

    def create_dataset(self) -> CumulativeDiligentDataset:
        """Create replay buffer dataset instance."""
        return ReplayCumulativeDataset(
            replay_ratio_gold=self.replay_ratio_gold,
            replay_ratio_exploration=self.replay_ratio_exploration,
            allow_duplicates_on_sampling=self.allow_duplicates_on_sampling,
            seed=self.seed,
            child_class=BasicDataset,
            check_unique=self.check_unique,
        )


# ============================================================================
# RANDOM SAMPLING DATASET
# ============================================================================


@dataclass
class RandomSamplingCumulativeDatasetConfig(CumulativeDatasetConfig):
    """Config for replay buffer dataset."""

    dataset_type: str = "random_sampling"
    check_unique: bool = False
    max_sample_pairs: Optional[int | float] = None
    allow_duplicates_on_sampling: bool = False
    seed: Optional[int] = None

    def create_dataset(self) -> CumulativeDiligentDataset:
        """Create replay buffer dataset instance."""
        return RandomSamplingCumulativeDataset(
            max_sample_pairs=self.max_sample_pairs,
            allow_duplicates_on_sampling=self.allow_duplicates_on_sampling,
            seed=self.seed,
            child_class=BasicDataset,
            check_unique=self.check_unique,
        )
