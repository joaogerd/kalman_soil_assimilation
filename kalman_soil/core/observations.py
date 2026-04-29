"""Observation containers for soil-moisture assimilation."""

from dataclasses import dataclass
from datetime import datetime

import numpy as np


@dataclass(frozen=True)
class ObservationSet:
    """Collection of soil-moisture observations.

    Parameters
    ----------
    values : np.ndarray
        Observation values.
    errors : np.ndarray
        Observation error standard deviations or variances, depending on context.
    lon : np.ndarray
        Observation longitudes.
    lat : np.ndarray
        Observation latitudes.
    valid_time : datetime | None, optional
        Observation valid time.
    depth_m : float | None, optional
        Representative observation depth in meters.
    source : str, optional
        Observation source name.
    units : str, optional
        Observation units.
    """

    values: np.ndarray
    errors: np.ndarray
    lon: np.ndarray
    lat: np.ndarray
    valid_time: datetime | None = None
    depth_m: float | None = None
    source: str = "unknown"
    units: str = "m3 m-3"

    def __post_init__(self) -> None:
        if self.values.shape != self.errors.shape:
            raise ValueError("values and errors must have the same shape")
        if self.values.shape != self.lon.shape or self.values.shape != self.lat.shape:
            raise ValueError("values, lon and lat must have the same shape")
        if self.depth_m is not None and self.depth_m < 0.0:
            raise ValueError("depth_m must be non-negative")

    @property
    def size(self) -> int:
        """Number of observations."""
        return int(self.values.size)
