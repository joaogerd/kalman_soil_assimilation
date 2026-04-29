import numpy as np
import pytest

from kalman_soil.core import (
    GridMetadata,
    ObservationSet,
    SoilLayer,
    SoilLayerCollection,
    SoilMoistureState,
    UncertaintySpec,
)


def test_soil_layer_thickness():
    layer = SoilLayer(name="layer_1", top_depth_m=0.0, bottom_depth_m=0.1)
    assert layer.thickness_m == pytest.approx(0.1)


def test_soil_layer_rejects_invalid_depths():
    with pytest.raises(ValueError):
        SoilLayer(name="invalid", top_depth_m=0.2, bottom_depth_m=0.1)


def test_soil_state_requires_layer_dimension_match():
    layers = SoilLayerCollection((SoilLayer("l1", 0.0, 0.1), SoilLayer("l2", 0.1, 0.4)))
    grid = GridMetadata(name="test_grid", grid_type="regular_latlon")
    values = np.zeros((3, 2))

    state = SoilMoistureState(values=values, layers=layers, grid=grid)

    assert state.n_layers == 2


def test_soil_state_rejects_wrong_layer_dimension():
    layers = SoilLayerCollection((SoilLayer("l1", 0.0, 0.1),))
    grid = GridMetadata(name="test_grid", grid_type="regular_latlon")
    values = np.zeros((3, 2))

    with pytest.raises(ValueError):
        SoilMoistureState(values=values, layers=layers, grid=grid)


def test_observation_set_size():
    values = np.array([0.2, 0.3])
    errors = np.array([0.05, 0.05])
    lon = np.array([-45.0, -46.0])
    lat = np.array([-23.0, -24.0])

    observations = ObservationSet(values=values, errors=errors, lon=lon, lat=lat)

    assert observations.size == 2


def test_observation_set_rejects_shape_mismatch():
    with pytest.raises(ValueError):
        ObservationSet(
            values=np.array([0.2, 0.3]),
            errors=np.array([0.05]),
            lon=np.array([-45.0, -46.0]),
            lat=np.array([-23.0, -24.0]),
        )


def test_uncertainty_rejects_negative_values():
    with pytest.raises(ValueError):
        UncertaintySpec(background_error=-0.1, observation_error=0.05)
