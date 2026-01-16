from pyligent.common.dataset_configs import (
    BasicCumulativeDatasetConfig,
    RandomSamplingCumulativeDatasetConfig,
    ReplayCumulativeDatasetConfig,
)
from pyligent.core.dataset import CumulativeDatasetConfig

DATASET_CONFIG_REGISTRY: dict[str, type[CumulativeDatasetConfig]] = {
    "basic": BasicCumulativeDatasetConfig,
    "replay_buffer": ReplayCumulativeDatasetConfig,
    "random_sampling": RandomSamplingCumulativeDatasetConfig,
}
