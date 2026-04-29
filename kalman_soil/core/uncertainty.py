"""Uncertainty specifications for assimilation experiments."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UncertaintySpec:
    """Simple uncertainty specification.

    Parameters
    ----------
    background_error : float
        Background error scale.
    observation_error : float
        Observation error scale.
    process_error : float, optional
        Process error scale.
    units : str, optional
        Units associated with the uncertainty values.
    """

    background_error: float
    observation_error: float
    process_error: float = 0.0
    units: str = "m3 m-3"

    def __post_init__(self) -> None:
        if self.background_error < 0.0:
            raise ValueError("background_error must be non-negative")
        if self.observation_error < 0.0:
            raise ValueError("observation_error must be non-negative")
        if self.process_error < 0.0:
            raise ValueError("process_error must be non-negative")
