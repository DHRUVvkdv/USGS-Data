import requests
import json
import os
from datetime import datetime

# Define a function to fetch data from USGS NWIS
def fetch_usgs_data(site_id, agency_cd, period, parameter_cd):
  # Construct the URL
  url = f"https://nwis.waterservices.usgs.gov/nwis/iv/?sites={site_id}&agencyCd={agency_cd}&period={period}&parameterCd={parameter_cd}&format=json"
  
  # Send a GET request
  response = requests.get(url)
  
  # Parse the JSON response
  data = json.loads(response.text)
  
  # Get the current date
  current_date = datetime.now().strftime("%Y-%m-%d")
  
  # Create the output directory if it doesn't exist
  output_dir = f"../data/raw/{parameter_cd}/{current_date}_{period}"
  os.makedirs(output_dir, exist_ok=True)
  
  # Save the data to a file
  with open(f"{output_dir}/data.json", "w") as f:
    json.dump(data, f, indent=4)
  
  print(f"Data saved to {output_dir}/data.json")

# Get user input for the parameters
site_id = input("Enter site ID: ")
agency_cd = input("Enter agency code (e.g. USGS): ")
period = input("Enter period (e.g. P365D): ")
parameter_cd = input("Enter parameter code (e.g. 00060): ")

# Fetch and save the data
fetch_usgs_data(site_id, agency_cd, period, parameter_cd)