"""
Optimized dataset module for training data management.

Provides abstract base classes for datasets with modular data addition,
sampling, and cumulative dataset management across time steps.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from functools import partial
from typing import Callable, Iterator

from pyligent.core.path import Action, PathContext

DiligentDatasetItem = tuple[PathContext, Action]


class DiligentDataset(ABC):
    """
    Abstract base for training datasets.

    Supports modular data addition and sampling with separate tracking
    of gold (teacher) and exploration pairs.
    """

    __slots__ = ("_gold_pairs", "_exploration_pairs", "_cached_pairs", "_cache_valid")

    def __init__(
        self,
        gold_pairs: list[DiligentDatasetItem] | None = None,
        exploration_pairs: list[DiligentDatasetItem] | None = None,
    ) -> None:
        self._gold_pairs: list[DiligentDatasetItem] = gold_pairs or []
        self._exploration_pairs: list[DiligentDatasetItem] = exploration_pairs or []
        self._cached_pairs: list[DiligentDatasetItem] = []
        self._cache_valid: bool = False

    def _invalidate_cache(self) -> None:
        """Invalidate pairs cache when data is modified."""
        self._cache_valid = False

    @property
    def pairs(self) -> list[DiligentDatasetItem]:
        """Access combined gold and exploration pairs with caching."""
        if not self._cache_valid:
            self._cached_pairs = self._gold_pairs + self._exploration_pairs
            self._cache_valid = True
        return self._cached_pairs

    @property
    def gold_pairs(self) -> list[DiligentDatasetItem]:
        """Access gold/teacher pairs."""
        return self._gold_pairs

    @property
    def exploration_pairs(self) -> list[DiligentDatasetItem]:
        """Access exploration pairs."""
        return self._exploration_pairs

    def __len__(self) -> int:
        """Total count of gold and exploration pairs."""
        return len(self._gold_pairs) + len(self._exploration_pairs)

    def __getitem__(self, idx: int) -> DiligentDatasetItem:
        """Access pair by index across combined pairs."""
        return self.pairs[idx]

    def __iter__(self) -> Iterator[DiligentDatasetItem]:
        """Iterate over all pairs."""
        return iter(self.pairs)

    def add_gold_pair(self, pair: DiligentDatasetItem) -> None:
        """Add single gold/teacher pair."""
        self._add(self._gold_pairs, pair)
        self._invalidate_cache()

    def add_gold_pairs(self, pairs: list[DiligentDatasetItem]) -> None:
        """Add multiple gold/teacher pairs efficiently."""
        if not pairs:
            return
        for pair in pairs:
            self._add(self._gold_pairs, pair)
        self._invalidate_cache()

    def add_exploration_pair(self, pair: DiligentDatasetItem) -> None:
        """Add single exploration pair."""
        self._add(self._exploration_pairs, pair)
        self._invalidate_cache()

    def add_exploration_pairs(self, pairs: list[DiligentDatasetItem]) -> None:
        """Add multiple exploration pairs efficiently."""
        if not pairs:
            return
        for pair in pairs:
            self._add(self._exploration_pairs, pair)
        self._invalidate_cache()

    def extend(self, other: DiligentDataset) -> None:
        """Merge another dataset."""
        self.add_gold_pairs(other.gold_pairs)
        self.add_exploration_pairs(other.exploration_pairs)

    def convert_to_only_golds(self) -> DiligentDataset:
        """Create new dataset containing only gold pairs."""
        return type(self)(gold_pairs=self._gold_pairs.copy())

    def copy(self) -> DiligentDataset:
        """Create deep copy of dataset."""
        return type(self)(
            gold_pairs=self._gold_pairs.copy(),
            exploration_pairs=self._exploration_pairs.copy(),
        )

    def downcast(self) -> DiligentDataset:
        """Create deep copy of dataset."""
        return DiligentDataset(
            gold_pairs=self._gold_pairs.copy(),
            exploration_pairs=self._exploration_pairs.copy(),
        )

    def _add(self, target_list: list, item: DiligentDatasetItem) -> bool:
        """
        Add item to target list. Override for custom logic.

        Returns:
            bool: True if item was added, False otherwise
        """
        target_list.append(item)
        return True


SamplingDatasetFunction = Callable[[], DiligentDataset]


class CumulativeDiligentDataset(ABC):
    """
    Manages datasets across time steps with lazy initialization.

    Each time step has its own dataset, created on-demand via defaultdict.
    """

    __slots__ = ("_t_dataset", "_child_class", "_child_kwargs")

    def __init__(
        self,
        child_class: type[DiligentDataset] = DiligentDataset,
        **child_kwargs,
    ) -> None:
        self._child_class = child_class
        self._child_kwargs = child_kwargs
        self._t_dataset: dict[int, DiligentDataset] = defaultdict(
            partial(child_class, **child_kwargs)
        )

    def at(self, t: int) -> DiligentDataset:
        """Access dataset at specific time step."""
        return self._t_dataset[t]

    def sample(self, only_gold: bool, t: int) -> DiligentDataset:
        """
        Sample dataset at time step t.

        Args:
            only_gold: If True, return only gold pairs
            t: Time step to sample from
        """
        dataset = self.at(t)
        return dataset.convert_to_only_golds() if only_gold else dataset

    def sample_from(self, dataset: DiligentDataset) -> DiligentDataset:
        return dataset

    def __len__(self) -> int:
        """Total pairs across all time steps."""
        return sum(len(d) for d in self._t_dataset.values())

    @property
    def composite(self) -> DiligentDataset:
        """Merge all time step datasets into single dataset."""
        composite_dataset = self._child_class(**self._child_kwargs)
        for dataset in self._t_dataset.values():
            composite_dataset.extend(dataset)
        return composite_dataset


@dataclass
class CumulativeDatasetConfig(ABC):
    """Base config for dataset implementations (YAML-serializable)."""

    dataset_type: str = ""

    @abstractmethod
    def create_dataset(self) -> CumulativeDiligentDataset:
        """Factory method to instantiate the dataset."""
