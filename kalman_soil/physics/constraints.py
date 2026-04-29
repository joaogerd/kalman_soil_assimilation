"""Physical constraints for soil-moisture fields."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SoilMoistureBounds:
    """Physical bounds for soil moisture.

    Parameters
    ----------
    minimum : float
        Minimum allowed soil moisture value.
    maximum : float
        Maximum allowed soil moisture value.
    units : str, optional
        Units of the bounds.
    """

    minimum: float
    maximum: float
    units: str = "m3 m-3"

    def __post_init__(self) -> None:
        if self.minimum < 0.0:
            raise ValueError("minimum must be non-negative")
        if self.maximum <= self.minimum:
            raise ValueError("maximum must be greater than minimum")


@dataclass(frozen=True)
class ConstraintReport:
    """Summary of physical-constraint corrections."""

    n_total: int
    n_below_minimum: int
    n_above_maximum: int
    n_masked: int

    @property
    def n_corrected(self) -> int:
        """Number of values changed by bound constraints."""
        return self.n_below_minimum + self.n_above_maximum


def apply_soil_moisture_bounds(
    values: np.ndarray,
    bounds: SoilMoistureBounds,
    land_mask: np.ndarray | None = None,
    masked_value: float = np.nan,
) -> tuple[np.ndarray, ConstraintReport]:
    """Apply physical bounds and optional land mask to soil-moisture values.

    Parameters
    ----------
    values : np.ndarray
        Input soil-moisture values.
    bounds : SoilMoistureBounds
        Minimum and maximum allowed values.
    land_mask : np.ndarray | None, optional
        Boolean mask where ``True`` represents land points. If provided, it must
        be broadcast-compatible with ``values``.
    masked_value : float, optional
        Value assigned to non-land points.

    Returns
    -------
    tuple[np.ndarray, ConstraintReport]
        Corrected values and a report describing the corrections.
    """
    input_values = np.asarray(values, dtype=float)
    corrected = input_values.copy()

    below = corrected < bounds.minimum
    above = corrected > bounds.maximum

    corrected = np.where(below, bounds.minimum, corrected)
    corrected = np.where(above, bounds.maximum, corrected)

    n_masked = 0
    if land_mask is not None:
        mask = np.asarray(land_mask, dtype=bool)
        try:
            non_land = ~np.broadcast_to(mask, corrected.shape)
        except ValueError as exc:
            raise ValueError("land_mask must be broadcast-compatible with values") from exc
        corrected = np.where(non_land, masked_value, corrected)
        n_masked = int(np.count_nonzero(non_land))

    report = ConstraintReport(
        n_total=int(corrected.size),
        n_below_minimum=int(np.count_nonzero(below)),
        n_above_maximum=int(np.count_nonzero(above)),
        n_masked=n_masked,
    )
    return corrected, report
