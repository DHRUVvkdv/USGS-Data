# USGS Water Quality Data Fetcher

This script is written to help get data from USGS website about water quality. The parameters are listed below. 


## Available Parameters

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

The data from three sites can be gathered for now, which are given below.

## Available Sites

| Short Form | Description              | Parameters Available                                             |
| ---------- | ------------------------ | ---------------------------------------------------------------- |
| lr         | Lick Run                 | ["g", "d", "cos", "do", "pst", "ph", "p", "sc", "ta", "tw", "t"] |
| tc1        | Tinker Creek Columbia St | ["g", "d", "do", "ph", "sc", "tw", "t"]                          |
| tc2        | Tinker Creek Glade Creek | ["g", "d", "do", "ph", "sc", "tw", "t"]                          |

## Usage

To use this script, run it from the command line with the following syntax:

```python
python3 fetchData.py <site> <parameters> [--period <days>]
```

- `<site>`: The short form of the site (lr, tc1, or tc2)
- `<parameters>`: One or more parameter short forms (e.g., g d sc)
- `--period`: (Optional) Number of days to fetch data for (default is 1)

### Example

```python
python3 fetchData.py tc2 sc --period 1
```

This command will fetch specific conductance data for Tinker Creek Glade Creek for the past 1 day.

## Requirements

- Python 3.6 or higher
- `requests` library (install with `pip install requests`)

## Configuration

The script uses two configuration files:

- `../config/sensor_info.json`: Contains information about the parameters
- `../config/site_info.json`: Contains information about the sites

Make sure these files are present and correctly formatted before running the script.

## Output

The fetched data is saved in JSON format in the following directory structure:

```
../data/raw/<site_short_name>/<parameter_short_name>/<current_date>_<period>d/data.json
```

For example:

```
../data/raw/tc2/sc/2023-06-25_1d/data.json
```

## Error Handling

The script will display error messages if:

- An invalid site short name is provided
- Invalid parameters are provided
- Parameters not available for the specified site are requested
- There's an issue fetching or parsing the data from the USGS API

## Note

This script fetches data from the USGS National Water Information System (NWIS). Please ensure you comply with their terms of service when using this data.

# USGS Water Data Fetcher - Detailed Documentation

## 1. Introduction

The USGS Water Data Fetcher is a Python script designed to retrieve water quality data from the United States Geological Survey (USGS) National Water Information System (NWIS). It provides a command-line interface for users to specify the site, parameters, and time period for which they want to fetch data.

## 2. Script Structure

The script is organized into several key components:

1. Import statements
2. Configuration loading
3. Utility functions
4. Data fetching function
5. Main function
6. Command-line interface

## 3. Detailed Component Explanation

### 3.1 Import Statements

The script uses several Python libraries:

- `requests`: For making HTTP requests to the USGS API
- `json`: For parsing JSON data returned by the API
- `os`: For file and directory operations
- `datetime`: For handling dates and times
- `sys`: For system-specific parameters and functions
- `argparse`: For parsing command-line arguments

### 3.2 Configuration Loading

The script uses two JSON configuration files:

1. `sensor_info.json`: Contains information about the parameters (sensors)
2. `site_info.json`: Contains information about the available sites

These files are loaded at the module level using the `load_config()` function.

### 3.3 Utility Functions

Several utility functions are defined to handle data conversion:

- `get_parameter_code(parameter_short_name)`: Converts parameter short name to code
- `get_site_id(site_short_name)`: Converts site short name to ID
- `get_parameter_short_name(parameter_code)`: Converts parameter code to short name
- `get_site_short_name(site_id)`: Converts site ID to short name

These functions allow the script to work with human-readable short names while using the appropriate codes when interacting with the USGS API.

### 3.4 Data Fetching Function

The `fetch_usgs_data(site_id, agency_cd, period, parameter_cd)` function is responsible for:

1. Constructing the URL for the USGS API request
2. Sending the request and retrieving the data
3. Processing the response
4. Saving the data to a JSON file in the appropriate directory

### 3.5 Main Function

The `main()` function orchestrates the script's operation:

1. Parses command-line arguments
2. Validates the provided site and parameters
3. Calls the `fetch_usgs_data()` function for each requested parameter

### 3.6 Command-line Interface

The script uses `argparse` to create a user-friendly command-line interface. Users can specify:

- The site (required)
- One or more parameters (required)
- The time period in days (optional, defaults to 1)

## 7. Extensibility

The script is designed to be easily extensible:

- New sites can be added by updating the `site_info.json` file
- New parameters can be added by updating the `sensor_info.json` file
- The `fetch_usgs_data()` function can be modified to handle different API responses or data formats

## 8. Limitations and Future Improvements

Current limitations:

- Only works with predefined sites and parameters
- Fetches data for a single time period per run

Potential future improvements:

- Support for custom site IDs
- Ability to fetch data for multiple time periods in one run
- Integration with data visualization tools
- Support for other USGS data services

## 9. Conclusion

The USGS Water Data Fetcher provides a convenient way to retrieve water quality data from the USGS NWIS. Its modular design and use of configuration files make it adaptable to various use cases and easy to maintain and extend.

## 10. Contributing

Contributions to improve the USGS Water Data Fetcher are welcome. Please feel free to submit pull requests or open issues on the project's GitHub repository.
