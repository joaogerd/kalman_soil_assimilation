import numpy as np
import pytest

from kalman_soil.kalman_filter import KalmanFilter


def test_minimal_example_state_is_preserved():
    kf = KalmanFilter(state_dim=2, obs_dim=1)
    kf.set_observation_matrix(np.array([[1.0, 0.5]]))
    kf.set_state_transition(np.eye(2))
    kf.set_process_covariance(np.eye(2) * 0.01)
    kf.set_observation_covariance(np.eye(1) * 0.1)

    kf.predict()
    kf.update(np.array([[0.9]]))

    np.testing.assert_allclose(
        kf.get_state(),
        np.array([[0.66715596], [0.33357798]]),
        rtol=1e-7,
        atol=1e-7,
    )


def test_invalid_dimensions_are_rejected():
    with pytest.raises(ValueError):
        KalmanFilter(state_dim=0, obs_dim=1)
    with pytest.raises(ValueError):
        KalmanFilter(state_dim=1, obs_dim=0)


def test_observation_matrix_shape_is_validated():
    kf = KalmanFilter(state_dim=2, obs_dim=1)
    with pytest.raises(ValueError):
        kf.set_observation_matrix(np.ones((2, 2)))


def test_update_rejects_wrong_observation_shape():
    kf = KalmanFilter(state_dim=2, obs_dim=1)
    with pytest.raises(ValueError):
        kf.update(np.ones((2, 1)))


def test_covariance_remains_symmetric_after_update():
    kf = KalmanFilter(state_dim=2, obs_dim=1)
    kf.set_observation_matrix(np.array([[1.0, 0.5]]))
    kf.predict()
    kf.update(np.array([[0.9]]))

    np.testing.assert_allclose(kf.get_covariance(), kf.get_covariance().T, atol=1e-12)


def test_high_observation_error_keeps_state_close_to_background():
    kf = KalmanFilter(state_dim=1, obs_dim=1)
    kf.set_state([[0.2]])
    kf.set_covariance([[0.01]])
    kf.set_observation_matrix([[1.0]])
    kf.set_observation_covariance([[1.0e6]])
    kf.set_process_covariance([[0.0]])

    kf.predict()
    kf.update([[0.9]])

    assert kf.get_state()[0, 0] == pytest.approx(0.2, abs=1e-6)


def test_low_observation_error_moves_state_toward_observation():
    kf = KalmanFilter(state_dim=1, obs_dim=1)
    kf.set_state([[0.2]])
    kf.set_covariance([[1.0]])
    kf.set_observation_matrix([[1.0]])
    kf.set_observation_covariance([[1.0e-8]])
    kf.set_process_covariance([[0.0]])

    kf.predict()
    kf.update([[0.9]])

    assert kf.get_state()[0, 0] == pytest.approx(0.9, abs=1e-6)
