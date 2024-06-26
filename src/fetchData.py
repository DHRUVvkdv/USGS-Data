# Import necessary libraries
import requests  # For making HTTP requests
import json  # For parsing JSON data
import os  # For file and directory operations
from datetime import datetime  # For handling dates and times
import sys  # For system-specific parameters and functions
import argparse  # For parsing command-line arguments

# Function to load configuration from a JSON file
def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Load configurations at the module level
sensor_info = load_config('../config/sensor_info.json')
site_info = load_config('../config/site_info.json')

# Function to fetch USGS data
def fetch_usgs_data(site_id, agency_cd, period, parameter_cd):
    # Construct the URL for the USGS API
    url = f"https://nwis.waterservices.usgs.gov/nwis/iv/?sites={site_id}&agencyCd={agency_cd}&period=P{period}D&parameterCd={parameter_cd}&format=json"
    
    # Send a GET request to the API
    response = requests.get(url)
    data = json.loads(response.text)
    
    # Prepare the output directory
    current_date = datetime.now().strftime("%Y-%m-%d")
    site = get_site_short_name(site_id)
    parameter = get_parameter_short_name(parameter_cd)
    output_dir = f"../data/raw/{site}/{parameter}/{current_date}_{period}d"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Extract the values from the response
        values = data['value']['timeSeries'][0]['values'][0]['value']
        # Save the data to a JSON file
        with open(f"{output_dir}/data.json", "w") as f:
            json.dump(values, f, indent=4)
        print(f"Data saved to {output_dir}/data.json")
    except (KeyError, IndexError):
        print(f"Error: Unable to extract values from the response for parameter {parameter_cd}.")
        return None

    return data

# Function to get parameter code from short name
def get_parameter_code(parameter_short_name):
    for sensor, info in sensor_info.items():
        if sensor == parameter_short_name:
            return info['parameterCode']
    return None

# Function to get site ID from short name
def get_site_id(site_short_name):
    for site, info in site_info.items():
        if site == site_short_name:
            return info['siteId']
    return None

# Function to get parameter short name from code
def get_parameter_short_name(parameter_code):
    for sensor, info in sensor_info.items():
        if info['parameterCode'] == parameter_code:
            return sensor
    return None

# Function to get site short name from ID
def get_site_short_name(site_id):
    for site, info in site_info.items():
        if info['siteId'] == site_id:
            return site
    return None

# Main function
def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Fetch USGS water data.')
    parser.add_argument('site', help='Site short name (e.g., lr, tc1, tc2)')
    parser.add_argument('parameters', nargs='+', help='Parameter short names (e.g., g d cos do)')
    parser.add_argument('--period', type=int, default=1, help='Number of days to fetch data for (default: 1)')
    args = parser.parse_args()

    # Get site ID from short name
    site_id = get_site_id(args.site)
    if not site_id:
        print(f"Error: Invalid site short name '{args.site}'.")
        sys.exit(1)

    # Check if all parameters exist for the given site
    available_parameters = site_info[args.site]['availableParameters']
    invalid_parameters = [p for p in args.parameters if p not in available_parameters]
    if invalid_parameters:
        print(f"Error: The following parameters are not available for site '{args.site}': {', '.join(invalid_parameters)}")
        sys.exit(1)

    # Check if all parameters are valid
    invalid_parameters = [p for p in args.parameters if not get_parameter_code(p)]
    if invalid_parameters:
        print(f"Error: The following parameters are invalid: {', '.join(invalid_parameters)}")
        sys.exit(1)

    agency_cd = "USGS"

    # Fetch data for each parameter
    for parameter_short_name in args.parameters:
        parameter_cd = get_parameter_code(parameter_short_name)
        fetch_usgs_data(site_id, agency_cd, args.period, parameter_cd)

# Entry point of the script
if __name__ == "__main__":
    main()