"""High-level assimilation routines."""

from dataclasses import dataclass

import numpy as np

from kalman_soil.core import ObservationSet, SoilMoistureState, UncertaintySpec
from kalman_soil.kalman_filter import KalmanFilter
from kalman_soil.physics import ConstraintReport, SoilMoistureBounds, apply_soil_moisture_bounds


@dataclass(frozen=True)
class ColumnAssimilationResult:
    """Result from a single-column soil-moisture assimilation."""

    background: SoilMoistureState
    analysis: SoilMoistureState
    innovation: np.ndarray
    kalman_gain: np.ndarray
    constraint_report: ConstraintReport

    @property
    def increment(self) -> np.ndarray:
        """Analysis minus background increment."""
        return self.analysis.values - self.background.values


def assimilate_soil_column(
    background: SoilMoistureState,
    observations: ObservationSet,
    observation_matrix: np.ndarray,
    uncertainty: UncertaintySpec,
    bounds: SoilMoistureBounds | None = None,
) -> ColumnAssimilationResult:
    """Assimilate one soil column using a linear Kalman Filter.

    Parameters
    ----------
    background : SoilMoistureState
        Background state for one soil column. The values must have one value per
        soil layer.
    observations : ObservationSet
        Observation set. The current prototype supports one observation value.
    observation_matrix : np.ndarray
        Linear observation matrix with shape ``(1, n_layers)``.
    uncertainty : UncertaintySpec
        Background, observation and process uncertainty scales.
    bounds : SoilMoistureBounds | None, optional
        Optional physical bounds applied to the analysis.

    Returns
    -------
    ColumnAssimilationResult
        Background, analysis, innovation, gain and constraint report.
    """
    background_values = np.asarray(background.values, dtype=float).reshape(-1)
    n_layers = background.n_layers

    if background_values.shape != (n_layers,):
        raise ValueError("background values must represent exactly one soil column")
    if observations.size != 1:
        raise ValueError("this prototype supports exactly one observation")

    h_matrix = np.asarray(observation_matrix, dtype=float)
    if h_matrix.shape != (1, n_layers):
        raise ValueError(f"observation_matrix must have shape {(1, n_layers)}")

    observation_value = float(np.asarray(observations.values).reshape(-1)[0])
    observation_error = float(np.asarray(observations.errors).reshape(-1)[0])
    if observation_error < 0.0:
        raise ValueError("observation error must be non-negative")

    kf = KalmanFilter(state_dim=n_layers, obs_dim=1)
    kf.set_state(background_values.reshape(-1, 1))
    kf.set_covariance(np.eye(n_layers) * uncertainty.background_error**2)
    kf.set_state_transition(np.eye(n_layers))
    kf.set_process_covariance(np.eye(n_layers) * uncertainty.process_error**2)
    kf.set_observation_matrix(h_matrix)
    kf.set_observation_covariance(np.array([[max(observation_error, uncertainty.observation_error) ** 2]]))

    kf.predict()

    predicted_observation = h_matrix @ kf.get_state()
    innovation = np.array([[observation_value]]) - predicted_observation
    innovation_covariance = h_matrix @ kf.get_covariance() @ h_matrix.T + np.array(
        [[max(observation_error, uncertainty.observation_error) ** 2]]
    )
    kalman_gain = np.linalg.solve(innovation_covariance, h_matrix @ kf.get_covariance().T).T

    kf.update(np.array([[observation_value]]))

    analysis_values = kf.get_state().reshape(-1)
    if bounds is None:
        constraint_report = ConstraintReport(
            n_total=int(analysis_values.size),
            n_below_minimum=0,
            n_above_maximum=0,
            n_masked=0,
        )
        constrained_values = analysis_values
    else:
        constrained_values, constraint_report = apply_soil_moisture_bounds(analysis_values, bounds)

    analysis = background.copy_with_values(constrained_values)

    return ColumnAssimilationResult(
        background=background,
        analysis=analysis,
        innovation=innovation,
        kalman_gain=kalman_gain,
        constraint_report=constraint_report,
    )
