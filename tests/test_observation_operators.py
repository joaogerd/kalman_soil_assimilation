import numpy as np
import pytest

from kalman_soil.core import SoilLayer, SoilLayerCollection
from kalman_soil.operators import (
    LayerWeightedOperator,
    RootZoneAverageOperator,
    SurfaceSoilMoistureOperator,
)


def make_layers():
    return SoilLayerCollection(
        (
            SoilLayer("l1", 0.0, 0.1),
            SoilLayer("l2", 0.1, 0.4),
            SoilLayer("l3", 0.4, 1.0),
        )
    )


def test_surface_operator_observes_first_layer():
    h_matrix = SurfaceSoilMoistureOperator().matrix(make_layers())

    np.testing.assert_allclose(h_matrix, np.array([[1.0, 0.0, 0.0]]))


def test_layer_weighted_operator_normalizes_weights():
    h_matrix = LayerWeightedOperator((1.0, 2.0, 1.0)).matrix(make_layers())

    np.testing.assert_allclose(h_matrix, np.array([[0.25, 0.5, 0.25]]))


def test_layer_weighted_operator_rejects_wrong_size():
    with pytest.raises(ValueError):
        LayerWeightedOperator((1.0, 1.0)).matrix(make_layers())


def test_layer_weighted_operator_rejects_negative_weights():
    with pytest.raises(ValueError):
        LayerWeightedOperator((1.0, -1.0, 1.0)).matrix(make_layers())


def test_root_zone_operator_uses_depth_overlap():
    h_matrix = RootZoneAverageOperator(top_depth_m=0.0, bottom_depth_m=0.4).matrix(make_layers())

    np.testing.assert_allclose(h_matrix, np.array([[0.25, 0.75, 0.0]]))


def test_root_zone_operator_handles_partial_overlap():
    h_matrix = RootZoneAverageOperator(top_depth_m=0.05, bottom_depth_m=0.25).matrix(make_layers())

    np.testing.assert_allclose(h_matrix, np.array([[0.25, 0.75, 0.0]]))


def test_root_zone_operator_rejects_no_overlap():
    with pytest.raises(ValueError):
        RootZoneAverageOperator(top_depth_m=2.0, bottom_depth_m=3.0).matrix(make_layers())
