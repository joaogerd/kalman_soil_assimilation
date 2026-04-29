"""Soil-layer definitions used by soil-moisture assimilation workflows."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SoilLayer:
    """Vertical soil-layer metadata.

    Parameters
    ----------
    name : str
        Layer name or identifier.
    top_depth_m : float
        Depth at the top of the layer, in meters.
    bottom_depth_m : float
        Depth at the bottom of the layer, in meters.
    variable_name : str, optional
        Model variable associated with this layer.
    units : str, optional
        Units used by the layer variable.
    """

    name: str
    top_depth_m: float
    bottom_depth_m: float
    variable_name: str = "soil_moisture"
    units: str = "m3 m-3"

    def __post_init__(self) -> None:
        if self.bottom_depth_m <= self.top_depth_m:
            raise ValueError("bottom_depth_m must be greater than top_depth_m")
        if self.top_depth_m < 0.0:
            raise ValueError("top_depth_m must be non-negative")

    @property
    def thickness_m(self) -> float:
        """Layer thickness in meters."""
        return self.bottom_depth_m - self.top_depth_m


@dataclass(frozen=True)
class SoilLayerCollection:
    """Ordered collection of soil layers."""

    layers: tuple[SoilLayer, ...]

    def __post_init__(self) -> None:
        if not self.layers:
            raise ValueError("at least one soil layer is required")
        for previous, current in zip(self.layers[:-1], self.layers[1:]):
            if current.top_depth_m < previous.bottom_depth_m:
                raise ValueError("soil layers must be ordered and non-overlapping")

    def __len__(self) -> int:
        return len(self.layers)

    def names(self) -> list[str]:
        """Return layer names."""
        return [layer.name for layer in self.layers]
