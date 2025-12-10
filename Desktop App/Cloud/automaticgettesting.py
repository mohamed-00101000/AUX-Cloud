import requests
import json
import time
from urllib3.exceptions import NewConnectionError
from requests.exceptions import ConnectionError, Timeout, RequestException

# URL to fetch the JSON data from ###########################################
url = "https://projectegypt.online/new/data.json" 

# Define the local file paths
data_file_path = "data.json"  # File path to save fetched JSON data
log_file_path = "error_log_get.txt"  # File path to save logs

# Define the delay between requests (in seconds)
delay = 0.5  # Delay between each request

# Initialize counters
get_count = 0
error_count = 0
start_time = time.time()  # Use time.time() for numerical timestamp

# Function to log messages into a text file
def log_message(message, include_timestamp=True):
    with open(log_file_path, 'a') as log_file:
        if include_timestamp:
            log_file.write(f"{time.ctime()}: {message}\n")
        else:
            log_file.write(f"{message}\n")

# Function to fetch data and save it locally
def fetch_data_with_retries():
    global get_count, error_count, start_time
    try:
        # Send a GET request to fetch the raw JSON data
        response = requests.get(url, timeout=10)  # Timeout after 10 seconds if no response
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Parse the JSON content
        data = response.json()

        # Open the file in write mode and save the data
        with open(data_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Increment the send counter
        get_count += 1
        log_message(f"Successful fetch #{get_count}")
        return True

    except Exception as e:
        # Increment the error counter
        error_count += 1
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        log_message(f"Error #{error_count}")
        log_message(f"Time taken to get an error #{elapsed_time / 60:.2f} minutes")
        start_time = time.time()  # Reset start time to current time
        return False

# Log the start time without prepending a timestamp
log_message(f"Start Time: {time.ctime()}", include_timestamp=False)

# Continuous loop to fetch data periodically
while True:
    if fetch_data_with_retries():
        # Wait for the specified delay before fetching the data again
        time.sleep(delay)
    else:
        # If fetching data failed, log the failure and decide whether to continue
        log_message("Exiting due to repeated failures.")
        