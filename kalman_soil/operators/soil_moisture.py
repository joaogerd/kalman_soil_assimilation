"""Linear observation operators for soil-moisture states."""

from dataclasses import dataclass

import numpy as np

from kalman_soil.core import SoilLayerCollection


@dataclass(frozen=True)
class SurfaceSoilMoistureOperator:
    """Operator that observes the first soil layer."""

    def matrix(self, layers: SoilLayerCollection) -> np.ndarray:
        """Return a linear observation matrix for the surface layer."""
        h_matrix = np.zeros((1, len(layers)))
        h_matrix[0, 0] = 1.0
        return h_matrix


@dataclass(frozen=True)
class LayerWeightedOperator:
    """Operator that observes a weighted average of soil layers.

    Parameters
    ----------
    weights : tuple[float, ...]
        Weights applied to each model layer. The weights are normalized before
        building the observation matrix.
    """

    weights: tuple[float, ...]

    def matrix(self, layers: SoilLayerCollection) -> np.ndarray:
        """Return a normalized weighted-average observation matrix."""
        weights = np.asarray(self.weights, dtype=float)
        if weights.shape != (len(layers),):
            raise ValueError("weights must match the number of soil layers")
        if np.any(weights < 0.0):
            raise ValueError("weights must be non-negative")
        total = float(weights.sum())
        if total <= 0.0:
            raise ValueError("at least one weight must be positive")
        return (weights / total).reshape(1, -1)


@dataclass(frozen=True)
class RootZoneAverageOperator:
    """Operator for layer-thickness-weighted root-zone averages.

    Parameters
    ----------
    top_depth_m : float
        Top depth of the observed zone in meters.
    bottom_depth_m : float
        Bottom depth of the observed zone in meters.
    """

    top_depth_m: float = 0.0
    bottom_depth_m: float = 1.0

    def __post_init__(self) -> None:
        if self.top_depth_m < 0.0:
            raise ValueError("top_depth_m must be non-negative")
        if self.bottom_depth_m <= self.top_depth_m:
            raise ValueError("bottom_depth_m must be greater than top_depth_m")

    def matrix(self, layers: SoilLayerCollection) -> np.ndarray:
        """Return a depth-overlap weighted observation matrix."""
        overlaps = []
        for layer in layers.layers:
            overlap_top = max(layer.top_depth_m, self.top_depth_m)
            overlap_bottom = min(layer.bottom_depth_m, self.bottom_depth_m)
            overlap = max(0.0, overlap_bottom - overlap_top)
            overlaps.append(overlap)

        weights = np.asarray(overlaps, dtype=float)
        total = float(weights.sum())
        if total <= 0.0:
            raise ValueError("observed zone does not overlap any soil layer")
        return (weights / total).reshape(1, -1)
