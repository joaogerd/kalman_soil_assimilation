import numpy as np
import pytest
import xarray as xr

from kalman_soil.monan import inspect_netcdf, read_variable, write_updated_variable


def create_dataset(path):
    dataset = xr.Dataset(
        data_vars={
            "soil_moisture": (
                ("cell", "soil_layer"),
                np.array([[0.2, 0.3], [0.4, 0.5]], dtype=np.float64),
                {"units": "m3 m-3", "long_name": "soil moisture"},
            ),
            "land_mask": (("cell",), np.array([1, 0], dtype=np.int32)),
        },
        coords={
            "cell": np.array([0, 1]),
            "soil_layer": np.array([0, 1]),
        },
        attrs={"title": "synthetic MONAN-like file"},
    )
    dataset.to_netcdf(path)


def test_inspect_netcdf_reports_variable_metadata(tmp_path):
    path = tmp_path / "input.nc"
    create_dataset(path)

    info = inspect_netcdf(path)

    assert "soil_moisture" in info
    assert info["soil_moisture"].dims == ("cell", "soil_layer")
    assert info["soil_moisture"].shape == (2, 2)
    assert info["soil_moisture"].attrs["units"] == "m3 m-3"


def test_read_variable_loads_data_array(tmp_path):
    path = tmp_path / "input.nc"
    create_dataset(path)

    variable = read_variable(path, "soil_moisture")

    np.testing.assert_allclose(variable.values, np.array([[0.2, 0.3], [0.4, 0.5]]))
    assert variable.attrs["long_name"] == "soil moisture"


def test_write_updated_variable_preserves_metadata(tmp_path):
    input_path = tmp_path / "input.nc"
    output_path = tmp_path / "output.nc"
    create_dataset(input_path)

    new_values = np.array([[0.25, 0.35], [0.45, 0.55]])
    write_updated_variable(input_path, output_path, "soil_moisture", new_values)

    output = xr.open_dataset(output_path)
    try:
        np.testing.assert_allclose(output["soil_moisture"].values, new_values)
        assert output["soil_moisture"].attrs["units"] == "m3 m-3"
        assert output.attrs["title"] == "synthetic MONAN-like file"
        np.testing.assert_array_equal(output["land_mask"].values, np.array([1, 0]))
    finally:
        output.close()


def test_write_updated_variable_rejects_wrong_shape(tmp_path):
    input_path = tmp_path / "input.nc"
    output_path = tmp_path / "output.nc"
    create_dataset(input_path)

    with pytest.raises(ValueError):
        write_updated_variable(input_path, output_path, "soil_moisture", np.ones((3, 2)))


def test_missing_variable_is_rejected(tmp_path):
    path = tmp_path / "input.nc"
    create_dataset(path)

    with pytest.raises(KeyError):
        read_variable(path, "missing")
