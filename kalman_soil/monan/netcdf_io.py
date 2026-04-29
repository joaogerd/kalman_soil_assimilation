"""Small NetCDF helpers for MONAN initial-condition prototyping."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import xarray as xr


@dataclass(frozen=True)
class NetCDFVariableInfo:
    """Summary of a variable stored in a NetCDF file."""

    name: str
    dims: tuple[str, ...]
    shape: tuple[int, ...]
    dtype: str
    attrs: dict[str, Any]


def inspect_netcdf(path: str | Path) -> dict[str, NetCDFVariableInfo]:
    """Inspect variables in a NetCDF file.

    Parameters
    ----------
    path : str | Path
        NetCDF file path.

    Returns
    -------
    dict[str, NetCDFVariableInfo]
        Mapping from variable name to variable metadata.
    """
    with xr.open_dataset(path) as dataset:
        return {
            name: NetCDFVariableInfo(
                name=name,
                dims=tuple(variable.dims),
                shape=tuple(variable.shape),
                dtype=str(variable.dtype),
                attrs=dict(variable.attrs),
            )
            for name, variable in dataset.data_vars.items()
        }


def read_variable(path: str | Path, variable_name: str) -> xr.DataArray:
    """Read a variable from a NetCDF file into memory."""
    with xr.open_dataset(path) as dataset:
        if variable_name not in dataset:
            raise KeyError(f"variable not found: {variable_name}")
        return dataset[variable_name].load()


def write_updated_variable(
    input_path: str | Path,
    output_path: str | Path,
    variable_name: str,
    values: np.ndarray,
) -> None:
    """Write a copy of a NetCDF file with one variable updated.

    The output file preserves dataset-level metadata, coordinates and variables
    handled by xarray. The replacement values must have the same shape as the
    target variable.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    with xr.open_dataset(input_path) as dataset:
        if variable_name not in dataset:
            raise KeyError(f"variable not found: {variable_name}")

        target = dataset[variable_name]
        new_values = np.asarray(values, dtype=target.dtype)
        if new_values.shape != target.shape:
            raise ValueError(
                f"values for {variable_name} must have shape {target.shape}, got {new_values.shape}"
            )

        updated = dataset.copy(deep=True)
        updated[variable_name] = xr.DataArray(
            new_values,
            dims=target.dims,
            coords={dim: target.coords[dim] for dim in target.dims if dim in target.coords},
            attrs=dict(target.attrs),
            name=variable_name,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        updated.to_netcdf(output_path)
