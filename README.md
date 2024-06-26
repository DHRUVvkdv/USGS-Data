This script is written to help get data from USGS website about water quality.
The data from three sites can be gathered for now, which are given below.

# USGS-Data

| Short Form | Description                       |
| ---------- | --------------------------------- |
| d          | Discharge (ft3/s)                 |
| g          | Gage height (ft)                  |
| cos        | Count of samples (number)         |
| do         | Dissolved oxygen (mg/l)           |
| ph         | pH (standard units)               |
| p          | Precipitation (in)                |
| sc         | Specific conductance (uS/cm @25C) |
| ta         | Temperature, air (deg C)          |
| tw         | Temperature, water (deg C)        |
| t          | Turbidity (FNU)                   |

| Short Form | Description | Parameters Available |
| ---------- | ------------------------ | |
| lr | Lick Run | ["g", "d", "cos", "do", "pst", "ph", "p", "sc", "ta", "tw", "t"] |
| tc1 | Tinker Creek Columbia St | ["g", "d", "do", "ph", "sc", "tw", "t"] |
| tc2 | Tinker Creek Glade Creek | ["g", "d", "do", "ph", "sc", "tw", "t"] |

Usage:

Example:
python3 fetchData.py tc2 sc --period 1
