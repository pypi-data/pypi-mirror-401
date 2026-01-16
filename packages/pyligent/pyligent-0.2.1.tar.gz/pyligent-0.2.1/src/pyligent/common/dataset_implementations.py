"""
Optimized dataset implementations with replay buffer support.

Provides BasicDataset with optional uniqueness checking and
ReplayCumulativeDataset with efficient replay buffer sampling.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
from loguru import logger

from pyligent.core.dataset import (
    CumulativeDiligentDataset,
    DiligentDataset,
    DiligentDatasetItem,
)

# ============================================================================
# BASIC DATASET
# ============================================================================


class BasicDataset(DiligentDataset):
    """Dataset with optional uniqueness constraint on pairs."""

    __slots__ = ("check_unique", "_pairs_set")

    def __init__(
        self,
        gold_pairs: list[DiligentDatasetItem] | None = None,
        exploration_pairs: list[DiligentDatasetItem] | None = None,
        check_unique: bool = True,
    ) -> None:
        super().__init__(gold_pairs, exploration_pairs)
        self.check_unique = check_unique
        self._pairs_set: set[tuple[int, int]] = set()

    def _pair_key(self, pair: DiligentDatasetItem) -> tuple[int, int]:
        """Generate hash-based key for pair deduplication."""
        ctx, act = pair
        return (ctx.hash_value, act.hash_value)

    def _add(self, target_list: list, item: DiligentDatasetItem) -> bool:
        """Add item with optional uniqueness check."""
        if self.check_unique:
            key = self._pair_key(item)
            if key in self._pairs_set:
                return False
            self._pairs_set.add(key)

        target_list.append(item)
        return True


# ============================================================================
# REPLAY BUFFER DATASET
# ============================================================================


class ReplayCumulativeDataset(CumulativeDiligentDataset):
    """
    Dataset with replay buffer for experience mixing.

    Samples historical data from previous time steps and mixes
    with current data based on configurable replay ratios.
    """

    __slots__ = (
        "replay_ratio_gold",
        "replay_ratio_exploration",
        "allow_duplicates_on_sampling",
        "_rng",
    )

    def __init__(
        self,
        replay_ratio_gold: float,
        replay_ratio_exploration: float,
        allow_duplicates_on_sampling: bool,
        seed: Optional[int] = None,
        child_class: type[DiligentDataset] = DiligentDataset,
        **child_kwargs,
    ) -> None:
        super().__init__(child_class, **child_kwargs)
        self.replay_ratio_gold = replay_ratio_gold
        self.replay_ratio_exploration = replay_ratio_exploration
        self.allow_duplicates_on_sampling = allow_duplicates_on_sampling
        self._rng = np.random.default_rng(seed)

        if seed is None:
            logger.warning("[REPLAY] Seed is unset!")

        if self.allow_duplicates_on_sampling:
            logger.warning("[REPLAY] Duplicates are allowed during sampling!")

    def _sample_pairs(
        self, only_gold: bool, t: int, size: int
    ) -> list[DiligentDatasetItem]:
        """
        Sample pairs from historical datasets (depth < t).

        Args:
            only_gold: If True, sample only gold pairs
            t: Current time step
            size: Number of pairs to sample

        Returns:
            Sampled pairs from replay buffer
        """
        all_pairs = []

        for depth, dataset in self._t_dataset.items():
            if depth >= t:
                continue

            pairs_to_add = dataset.gold_pairs if only_gold else dataset.pairs
            all_pairs.extend(pairs_to_add)

        if not all_pairs:
            return []

        # Sample with replacement if size exceeds available pairs
        replace = self.allow_duplicates_on_sampling and size > len(all_pairs)
        if not self.allow_duplicates_on_sampling:
            size = min(size, len(all_pairs))

        replay_indices = self._rng.choice(
            len(all_pairs),
            size=size,
            replace=replace,
        )

        return [all_pairs[idx] for idx in replay_indices]

    def sample(self, only_gold: bool, t: int) -> DiligentDataset:
        """
        Sample dataset with replay mixing.

        Args:
            only_gold: If True, return only gold pairs
            t: Time step to sample from

        Returns:
            Dataset combining current and replayed historical data
        """
        current_dataset = self.at(t)

        # Create copy
        current_dataset_copy = (
            current_dataset.convert_to_only_golds()
            if only_gold
            else current_dataset.copy()
        )
        original_size = len(current_dataset_copy)

        # Determine replay ratio and sample size
        replay_ratio = (
            self.replay_ratio_gold if only_gold else self.replay_ratio_exploration
        )
        sample_size = int(replay_ratio * original_size)

        # Sample historical pairs
        sampled_pairs = self._sample_pairs(
            only_gold=only_gold,
            t=t,
            size=sample_size,
        )

        # Add sampled pairs
        if self.allow_duplicates_on_sampling:
            # There can be duplicity check, so downcast to basic implementation
            current_dataset_copy = current_dataset_copy.downcast()

        current_dataset_copy.add_gold_pairs(sampled_pairs)

        logger.debug(
            f"[REPLAY] Resulting {len(current_dataset_copy)} = "
            f"Sampled {len(sampled_pairs)} + Original {original_size}"
        )

        return current_dataset_copy


# ============================================================================
# RANDOM SAMPLING DATASET
# ============================================================================


class RandomSamplingCumulativeDataset(CumulativeDiligentDataset):
    """
    Dataset with random sampling of data
    """

    __slots__ = (
        "max_sample_pairs",
        "allow_duplicates_on_sampling",
        "_rng",
    )

    def __init__(
        self,
        max_sample_pairs: Optional[int | float],
        allow_duplicates_on_sampling: bool,
        seed: Optional[int] = None,
        child_class: type[DiligentDataset] = DiligentDataset,
        **child_kwargs,
    ) -> None:
        super().__init__(child_class, **child_kwargs)
        self.max_sample_pairs = max_sample_pairs
        self.allow_duplicates_on_sampling = allow_duplicates_on_sampling
        self._rng = np.random.default_rng(seed)

        if seed is None:
            logger.warning("[RANDOM] Seed is unset!")

        if self.allow_duplicates_on_sampling:
            logger.warning("[RANDOM] Duplicates are allowed during sampling!")

    def _sample_pairs(
        self, dataset: DiligentDataset, size: int
    ) -> list[DiligentDatasetItem]:
        """
        Sample pairs from historical datasets (depth < t).

        Args:
            only_gold: If True, sample only gold pairs
            t: Current time step
            size: Number of pairs to sample

        Returns:
            Sampled pairs
        """
        all_pairs = dataset.pairs

        if not all_pairs:
            return []

        # Sample with replacement if size exceeds available pairs
        replace = self.allow_duplicates_on_sampling and size > len(all_pairs)
        if not self.allow_duplicates_on_sampling:
            size = min(size, len(all_pairs))

        replay_indices = self._rng.choice(
            len(all_pairs),
            size=size,
            replace=replace,
        )

        return [all_pairs[idx] for idx in replay_indices]

    def _get_sample_size(self, original_size: int) -> int:
        if self.max_sample_pairs is None:
            return original_size
        if isinstance(self.max_sample_pairs, int):
            return self.max_sample_pairs
        return int(self.max_sample_pairs * original_size)

    def sample(self, only_gold: bool, t: int) -> DiligentDataset:
        """
        Sample dataset with replay mixing.

        Args:
            only_gold: If True, return only gold pairs
            t: Time step to sample from

        Returns:
            Dataset with sampled items
        """
        if not self.max_sample_pairs:
            return super().sample(only_gold=only_gold, t=t)

        dataset = self.at(t)
        current_dataset = dataset.convert_to_only_golds() if only_gold else dataset
        original_size = len(current_dataset)

        sample_size = self._get_sample_size(original_size)

        # Sample historical pairs
        sampled_pairs = self._sample_pairs(
            dataset=current_dataset,
            size=sample_size,
        )

        # Add sampled pairs
        sampled_dataset = DiligentDataset(gold_pairs=sampled_pairs)

        logger.debug(
            f"[RANDOM] Sampled {len(sampled_dataset)} from total {original_size}"
        )

        return sampled_dataset

    def sample_from(self, dataset: DiligentDataset) -> DiligentDataset:
        if not self.max_sample_pairs:
            return dataset

        original_size = len(dataset)
        sample_size = self._get_sample_size(original_size)

        # Sample historical pairs
        sampled_pairs = self._sample_pairs(
            dataset=dataset,
            size=sample_size,
        )

        # Add sampled pairs
        # NOTE: Suppose we do not care about gold/exploration pairs
        sampled_dataset = DiligentDataset(gold_pairs=sampled_pairs)

        logger.debug(
            f"[RANDOM] Sampled {len(sampled_dataset)} from total {original_size}"
        )

        return sampled_dataset
