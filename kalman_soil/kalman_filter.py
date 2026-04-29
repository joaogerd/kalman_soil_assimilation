"""Basic linear Kalman Filter implementation."""

import numpy as np


class KalmanFilter:
    """Basic linear Kalman Filter for soil-moisture data assimilation.

    Parameters
    ----------
    state_dim : int
        Dimension of the state vector.
    obs_dim : int
        Dimension of the observation vector.
    """

    def __init__(self, state_dim, obs_dim):
        if state_dim <= 0:
            raise ValueError("state_dim must be positive")
        if obs_dim <= 0:
            raise ValueError("obs_dim must be positive")

        self.state_dim = state_dim
        self.obs_dim = obs_dim

        self.x = np.zeros((state_dim, 1))
        self.P = np.eye(state_dim)
        self.F = np.eye(state_dim)
        self.H = np.zeros((obs_dim, state_dim))
        self.R = np.eye(obs_dim) * 0.1
        self.Q = np.eye(state_dim) * 0.01

    def predict(self):
        """Run the prediction step."""
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        self.P = self._symmetrize(self.P)

    def update(self, z):
        """Update the state estimate with a new observation.

        Parameters
        ----------
        z : np.ndarray
            Observation vector with shape ``(obs_dim, 1)``.
        """
        z = self._as_column_vector(z, self.obs_dim, "z")

        innovation = z - self.H @ self.x
        innovation_covariance = self.H @ self.P @ self.H.T + self.R

        # Solve S K.T = H P.T instead of explicitly computing inv(S).
        kalman_gain = np.linalg.solve(
            innovation_covariance,
            self.H @ self.P.T,
        ).T

        self.x = self.x + kalman_gain @ innovation

        identity = np.eye(self.state_dim)
        update_matrix = identity - kalman_gain @ self.H

        # Joseph-form covariance update for better numerical stability.
        self.P = update_matrix @ self.P @ update_matrix.T + kalman_gain @ self.R @ kalman_gain.T
        self.P = self._symmetrize(self.P)

    def set_state_transition(self, F):
        """Set the state transition matrix."""
        self.F = self._as_matrix(F, (self.state_dim, self.state_dim), "F")

    def set_observation_matrix(self, H):
        """Set the linear observation matrix."""
        self.H = self._as_matrix(H, (self.obs_dim, self.state_dim), "H")

    def set_process_covariance(self, Q):
        """Set the process noise covariance matrix."""
        self.Q = self._as_matrix(Q, (self.state_dim, self.state_dim), "Q")

    def set_observation_covariance(self, R):
        """Set the observation noise covariance matrix."""
        self.R = self._as_matrix(R, (self.obs_dim, self.obs_dim), "R")

    def set_state(self, x):
        """Set the current state estimate."""
        self.x = self._as_column_vector(x, self.state_dim, "x")

    def set_covariance(self, P):
        """Set the current state covariance matrix."""
        self.P = self._as_matrix(P, (self.state_dim, self.state_dim), "P")

    def get_state(self):
        """Return the current state estimate."""
        return self.x

    def get_covariance(self):
        """Return the current state covariance matrix."""
        return self.P

    @staticmethod
    def _symmetrize(matrix):
        return 0.5 * (matrix + matrix.T)

    @staticmethod
    def _as_matrix(value, expected_shape, name):
        matrix = np.asarray(value, dtype=float)
        if matrix.shape != expected_shape:
            raise ValueError(f"{name} must have shape {expected_shape}, got {matrix.shape}")
        return matrix

    @staticmethod
    def _as_column_vector(value, expected_size, name):
        vector = np.asarray(value, dtype=float)
        if vector.ndim == 1:
            vector = vector.reshape((-1, 1))
        expected_shape = (expected_size, 1)
        if vector.shape != expected_shape:
            raise ValueError(f"{name} must have shape {expected_shape}, got {vector.shape}")
        return vector


if __name__ == "__main__":
    state_dim = 2
    obs_dim = 1

    kf = KalmanFilter(state_dim, obs_dim)
    kf.set_observation_matrix(np.array([[1.0, 0.5]]))
    kf.set_state_transition(np.eye(state_dim))
    kf.set_process_covariance(np.eye(state_dim) * 0.01)
    kf.set_observation_covariance(np.eye(obs_dim) * 0.1)

    z = np.array([[0.9]])

    kf.predict()
    kf.update(z)

    print("Updated state:", kf.get_state())
