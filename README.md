# Kalman Soil Assimilation

## Overview
Kalman Soil Assimilation is a Python package for soil moisture data assimilation using the Kalman Filter in the MONAN model. This project aims to improve soil moisture representation by integrating satellite observations and in-situ measurements using advanced data assimilation techniques.

## Features
- Implementation of the Kalman Filter (KF) for soil moisture assimilation
- Modular design to support future extensions (Extended Kalman Filter, Ensemble Kalman Filter)
- Integration with satellite data (e.g., SMAP, ASCAT, GLDAS)
- Easy-to-use API for integrating with MONAN simulations

## Installation
To install the package, clone the repository and install the dependencies:
```bash
git clone https://github.com/YOUR_USERNAME/kalman_soil_assimilation.git
cd kalman_soil_assimilation
pip install -r requirements.txt
```

## Usage
Example usage of the Kalman Filter:
```python
from kalman_soil.kalman_filter import KalmanFilter
import numpy as np
 # This filter estimates soil moisture in two layers using temperature as an observation.
                                                                                  
 state_dim = 2  # Soil moisture in two layers
 obs_dim = 1    # Temperature as observation
                                                                                  
 kf = KalmanFilter(state_dim, obs_dim)
 
 # Define a sample observation matrix (temperature influence on soil moisture layers)
 # The first layer is more influenced than the second
 kf.set_observation_matrix(np.array([[1.0, 0.5]]))  
 
 # Define a sample state transition matrix
 # Identity matrix means no dynamic evolution of state
 kf.set_state_transition(np.array([[1, 0], [0, 1]]))  
 
 # Define noise covariance matrices
 kf.set_process_covariance(np.eye(state_dim) * 0.01)  
 kf.set_observation_covariance(np.eye(obs_dim) * 0.1)  
 
 # Sample observation (temperature measurement)
 z = np.array([[0.9]])  
 
 # Prediction and update
 kf.predict()
 kf.update(z)
 
 # Print updated state
 print("Updated state (soil moisture estimates for two layers):", kf.get_state())


```

## Roadmap
- [x] Implement basic Kalman Filter (KF)
- [ ] Extend to Extended Kalman Filter (EKF)
- [ ] Integrate satellite data (SMAP, ASCAT, GLDAS)
- [ ] Validate against MONAN simulations

## License
This project is licensed under the **Creative Commons Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0)**.
See the full license text [here](https://creativecommons.org/licenses/by-nc/3.0/legalcode).

## Contributing
Contributions are welcome! Please open an issue or submit a pull request with improvements.

## Contact
For any inquiries, feel free to reach out via GitHub issues or email.

---
**Author:** João Gerd Zell de Mattos


