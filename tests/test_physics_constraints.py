import numpy as np
import pytest

from kalman_soil.physics import SoilMoistureBounds, apply_soil_moisture_bounds


def test_soil_moisture_bounds_clip_values():
    values = np.array([-0.1, 0.2, 0.8])
    bounds = SoilMoistureBounds(minimum=0.0, maximum=0.6)

    corrected, report = apply_soil_moisture_bounds(values, bounds)

    np.testing.assert_allclose(corrected, np.array([0.0, 0.2, 0.6]))
    assert report.n_total == 3
    assert report.n_below_minimum == 1
    assert report.n_above_maximum == 1
    assert report.n_corrected == 2


def test_soil_moisture_bounds_apply_land_mask():
    values = np.array([0.1, 0.2, 0.3])
    land_mask = np.array([True, False, True])
    bounds = SoilMoistureBounds(minimum=0.0, maximum=0.6)

    corrected, report = apply_soil_moisture_bounds(values, bounds, land_mask=land_mask)

    assert np.isnan(corrected[1])
    np.testing.assert_allclose(corrected[[0, 2]], np.array([0.1, 0.3]))
    assert report.n_masked == 1


def test_land_mask_can_broadcast_over_layers():
    values = np.array([[0.1, 0.2], [0.3, 0.4]])
    land_mask = np.array([[True], [False]])
    bounds = SoilMoistureBounds(minimum=0.0, maximum=0.6)

    corrected, report = apply_soil_moisture_bounds(values, bounds, land_mask=land_mask)

    assert np.isnan(corrected[1, 0])
    assert np.isnan(corrected[1, 1])
    assert report.n_masked == 2


def test_invalid_bounds_are_rejected():
    with pytest.raises(ValueError):
        SoilMoistureBounds(minimum=-0.1, maximum=0.6)
    with pytest.raises(ValueError):
        SoilMoistureBounds(minimum=0.6, maximum=0.6)


def test_incompatible_land_mask_is_rejected():
    values = np.ones((2, 2))
    land_mask = np.ones((3,), dtype=bool)
    bounds = SoilMoistureBounds(minimum=0.0, maximum=0.6)

    with pytest.raises(ValueError):
        apply_soil_moisture_bounds(values, bounds, land_mask=land_mask)
