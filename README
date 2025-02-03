# Kalman Soil Assimilation

## Overview
Kalman Soil Assimilation is a Python package for soil moisture data assimilation using the Kalman Filter in the BAM/SSiB model. This project aims to improve soil moisture representation by integrating satellite observations and in-situ measurements using advanced data assimilation techniques.

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

# Initialize Kalman Filter
kf = KalmanFilter(state_dim=2, obs_dim=1)

# Set transition and observation matrices
F = np.array([[1, 0], [0, 1]])
H = np.array([[1, 0]])
Q = np.eye(2) * 0.01
R = np.eye(1) * 0.1

kf.set_state_transition(F)
kf.set_observation_matrix(H)
kf.set_process_covariance(Q)
kf.set_observation_covariance(R)

# Simulated observation
z = np.array([[0.9]])

# Prediction and update
kf.predict()
kf.update(z)

print("Estimated state:", kf.get_state())
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


