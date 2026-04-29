"""Grid metadata used by model states and observations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GridMetadata:
    """Horizontal grid metadata.

    Parameters
    ----------
    name : str
        Grid identifier.
    grid_type : str
        Grid type, for example ``regular_latlon`` or ``unstructured``.
    crs : str, optional
        Coordinate reference system description.
    x_name : str, optional
        Name of the x or longitude coordinate.
    y_name : str, optional
        Name of the y or latitude coordinate.
    """

    name: str
    grid_type: str
    crs: str = "EPSG:4326"
    x_name: str = "lon"
    y_name: str = "lat"

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("grid name must not be empty")
        if not self.grid_type:
            raise ValueError("grid_type must not be empty")
