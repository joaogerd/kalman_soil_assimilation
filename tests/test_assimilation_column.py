import numpy as np
import pytest

from kalman_soil.assimilation import assimilate_soil_column
from kalman_soil.core import (
    GridMetadata,
    ObservationSet,
    SoilLayer,
    SoilLayerCollection,
    SoilMoistureState,
    UncertaintySpec,
)
from kalman_soil.operators import SurfaceSoilMoistureOperator
from kalman_soil.physics import SoilMoistureBounds


def make_background(values):
    layers = SoilLayerCollection(
        (
            SoilLayer("l1", 0.0, 0.1),
            SoilLayer("l2", 0.1, 0.4),
        )
    )
    grid = GridMetadata(name="column", grid_type="single_column")
    return SoilMoistureState(values=np.asarray(values, dtype=float), layers=layers, grid=grid)


def make_observation(value, error=0.05):
    return ObservationSet(
        values=np.array([value]),
        errors=np.array([error]),
        lon=np.array([0.0]),
        lat=np.array([0.0]),
        depth_m=0.05,
        source="synthetic",
    )


def test_column_assimilation_moves_surface_layer_toward_observation():
    background = make_background([0.2, 0.3])
    observation = make_observation(0.5, error=0.02)
    h_matrix = SurfaceSoilMoistureOperator().matrix(background.layers)
    uncertainty = UncertaintySpec(background_error=0.1, observation_error=0.02)

    result = assimilate_soil_column(background, observation, h_matrix, uncertainty)

    assert result.analysis.values[0] > background.values[0]
    assert result.analysis.values[0] < 0.5
    assert result.increment[0] > 0.0
    assert result.innovation.shape == (1, 1)
    assert result.kalman_gain.shape == (2, 1)


def test_column_assimilation_preserves_unobserved_layer_without_cross_covariance():
    background = make_background([0.2, 0.3])
    observation = make_observation(0.5, error=0.02)
    h_matrix = SurfaceSoilMoistureOperator().matrix(background.layers)
    uncertainty = UncertaintySpec(background_error=0.1, observation_error=0.02)

    result = assimilate_soil_column(background, observation, h_matrix, uncertainty)

    assert result.analysis.values[1] == pytest.approx(background.values[1])


def test_column_assimilation_applies_physical_bounds():
    background = make_background([0.2, 0.3])
    observation = make_observation(1.5, error=0.001)
    h_matrix = SurfaceSoilMoistureOperator().matrix(background.layers)
    uncertainty = UncertaintySpec(background_error=1.0, observation_error=0.001)
    bounds = SoilMoistureBounds(minimum=0.0, maximum=0.6)

    result = assimilate_soil_column(background, observation, h_matrix, uncertainty, bounds=bounds)

    assert result.analysis.values[0] == pytest.approx(0.6)
    assert result.constraint_report.n_above_maximum == 1


def test_column_assimilation_rejects_multiple_observations():
    background = make_background([0.2, 0.3])
    observations = ObservationSet(
        values=np.array([0.4, 0.5]),
        errors=np.array([0.05, 0.05]),
        lon=np.array([0.0, 0.0]),
        lat=np.array([0.0, 0.0]),
    )
    h_matrix = SurfaceSoilMoistureOperator().matrix(background.layers)
    uncertainty = UncertaintySpec(background_error=0.1, observation_error=0.05)

    with pytest.raises(ValueError):
        assimilate_soil_column(background, observations, h_matrix, uncertainty)


def test_column_assimilation_rejects_wrong_observation_matrix_shape():
    background = make_background([0.2, 0.3])
    observation = make_observation(0.5)
    uncertainty = UncertaintySpec(background_error=0.1, observation_error=0.05)

    with pytest.raises(ValueError):
        assimilate_soil_column(background, observation, np.ones((2, 2)), uncertainty)
