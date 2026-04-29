"""State containers for soil-moisture assimilation."""

from dataclasses import dataclass
from datetime import datetime

import numpy as np

from .grid import GridMetadata
from .layers import SoilLayerCollection


@dataclass(frozen=True)
class SoilMoistureState:
    """Soil-moisture state by grid point and soil layer.

    Parameters
    ----------
    values : np.ndarray
        Soil-moisture values. The last dimension must match the number of soil layers.
    layers : SoilLayerCollection
        Soil-layer metadata.
    grid : GridMetadata
        Horizontal grid metadata.
    valid_time : datetime | None, optional
        Valid time of the state.
    units : str, optional
        Soil-moisture units.
    name : str, optional
        State identifier.
    """

    values: np.ndarray
    layers: SoilLayerCollection
    grid: GridMetadata
    valid_time: datetime | None = None
    units: str = "m3 m-3"
    name: str = "soil_moisture"

    def __post_init__(self) -> None:
        if self.values.ndim < 1:
            raise ValueError("values must have at least one dimension")
        if self.values.shape[-1] != len(self.layers):
            raise ValueError("last dimension of values must match the number of soil layers")

    @property
    def n_layers(self) -> int:
        """Number of soil layers in the state."""
        return len(self.layers)

    def copy_with_values(self, values: np.ndarray) -> "SoilMoistureState":
        """Return a new state with the same metadata and different values."""
        return SoilMoistureState(
            values=values,
            layers=self.layers,
            grid=self.grid,
            valid_time=self.valid_time,
            units=self.units,
            name=self.name,
        )
