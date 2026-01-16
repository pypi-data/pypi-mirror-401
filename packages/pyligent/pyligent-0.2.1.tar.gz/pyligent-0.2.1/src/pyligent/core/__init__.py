"""pyligent.core (lazy exports to avoid circular imports)."""

__all__ = [
    "DiligentDataset",
    "SamplingDatasetFunction",
    "Pipeline",
    "PipelineConfig",
    "Solver",
    "Validator",
]


def __getattr__(name: str):
    if name in {"DiligentDataset", "SamplingDatasetFunction"}:
        from .dataset import DiligentDataset, SamplingDatasetFunction

        return {
            "DiligentDataset": DiligentDataset,
            "SamplingDatasetFunction": SamplingDatasetFunction,
        }[name]
    if name in {"Pipeline", "PipelineConfig"}:
        from .pipeline import Pipeline, PipelineConfig

        return {"Pipeline": Pipeline, "PipelineConfig": PipelineConfig}[name]
    if name == "Solver":
        from .solver import Solver

        return Solver
    if name == "Validator":
        from .validator import Validator

        return Validator
    raise AttributeError(name)
