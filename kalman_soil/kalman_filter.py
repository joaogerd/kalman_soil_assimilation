import numpy as np

class KalmanFilter:
    """
    Implementation of a basic Kalman Filter for Soil Moisture Data Assimilation.
    """
    def __init__(self, state_dim, obs_dim):
        """
        Initializes the Kalman Filter.

        :param state_dim: Dimension of the state vector (e.g., soil moisture levels)
        :param obs_dim: Dimension of the observation vector (e.g., temperature, humidity)
        """
        self.state_dim = state_dim
        self.obs_dim = obs_dim
        
        # State vector (e.g., soil moisture in different layers)
        self.x = np.zeros((state_dim, 1))  # Initial state estimate
        
        # State covariance matrix (initial uncertainty)
        self.P = np.eye(state_dim) * 1.0  
        
        # State transition matrix (identity for now)
        self.F = np.eye(state_dim)  
        
        # Observation matrix (to be defined based on observations)
        self.H = np.zeros((obs_dim, state_dim))  
        
        # Observation covariance matrix (measurement noise covariance)
        self.R = np.eye(obs_dim) * 0.1  
        
        # Process noise covariance (uncertainty in state evolution)
        self.Q = np.eye(state_dim) * 0.01  

    def predict(self):
        """
        Performs the prediction step of the Kalman Filter.
        """
        self.x = np.dot(self.F, self.x)  # Predict the next state
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q  # Predict state covariance

    def update(self, z):
        """
        Updates the state estimate with a new observation.
        
        :param z: Observation vector
        """
        y = z - np.dot(self.H, self.x)  # Measurement residual (innovation)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R  # Residual covariance
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  # Kalman Gain

        self.x = self.x + np.dot(K, y)  # Updated state estimate
        I = np.eye(self.state_dim)
        self.P = np.dot(I - np.dot(K, self.H), self.P)  # Updated state covariance

    def set_state_transition(self, F):
        """
        Sets the state transition matrix.
        
        :param F: State transition matrix
        """
        self.F = F

    def set_observation_matrix(self, H):
        """
        Sets the observation matrix.
        
        :param H: Observation matrix
        """
        self.H = H

    def set_process_covariance(self, Q):
        """
        Sets the process noise covariance matrix.
        
        :param Q: Process noise covariance matrix
        """
        self.Q = Q

    def set_observation_covariance(self, R):
        """
        Sets the observation noise covariance matrix.
        
        :param R: Observation noise covariance matrix
        """
        self.R = R

    def get_state(self):
        """
        Returns the current state estimate.
        """
        return self.x

    def get_covariance(self):
        """
        Returns the current state covariance matrix.
        """
        return self.P

if __name__ == "__main__":
    # Example usage
    state_dim = 2  # Soil moisture in two layers
    obs_dim = 1    # Temperature as observation

    kf = KalmanFilter(state_dim, obs_dim)
    
    # Define a sample observation matrix (temperature influence on soil moisture)
    kf.set_observation_matrix(np.array([[1.0, 0.5]]))  
    
    # Define a sample state transition matrix
    kf.set_state_transition(np.array([[1, 0], [0, 1]]))  
    
    # Define noise covariance matrices
    kf.set_process_covariance(np.eye(state_dim) * 0.01)  
    kf.set_observation_covariance(np.eye(obs_dim) * 0.1)  
    
    # Sample observation
    z = np.array([[0.9]])  
    
    # Prediction and update
    kf.predict()
    kf.update(z)
    
    # Print updated state
    print("Updated state:", kf.get_state())

