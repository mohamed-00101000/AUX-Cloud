import requests
import json
import time
from urllib3.exceptions import NewConnectionError
from requests.exceptions import ConnectionError, Timeout, RequestException
import sys

# URL to fetch the JSON data from
# base_url  = "http://racingteam.rf.gd/new/data.json" 
base_url = sys.argv[1]
delay = int(sys.argv[2])
print(f"Get base_url: {base_url}, delay: {delay}")

# Define the local file paths
data_file_path = "data.json"  # File path to save fetched JSON data
log_file_path = "error_log_get.txt"  # File path to save logs


# Define the delay between requests (in seconds)
# delay = 1  # Delay between each request

# Initialize counters
get_count = 0
error_count = 0
start_time = time.time()  # Use time.time() for numerical timestamp
# Function to load the existing time from the saved data file

def get_existing_time():
    try:
        with open(data_file_path, 'r') as file:
            saved_data = json.load(file)
            if isinstance(saved_data, list) and len(saved_data) > 0:
                return saved_data[0].get("time", None)  # Return the saved time
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or contains invalid JSON, return None
        return None
    return None

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
        response = requests.get(base_url , timeout=1)  # Timeout after 10 seconds if no response
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        # Parse the JSON content
        data = response.json()

        # Extract time from the new response
        if isinstance(data, list) and len(data) > 0:
            new_time = data[0].get("time", None)

            # Load existing time from file
            existing_time = get_existing_time()

            if existing_time is None or new_time >= existing_time:
                # Write the new data to the file if it's greater
                with open(data_file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                # log_message(f"Data updated with time {new_time}")
                # print(f"Data updated: {new_time}")
            else:
                log_message(f"Skipped update. Existing time: {existing_time}, New time: {new_time}")
                print(f"Skipped update. Existing time: {existing_time}, New time: {new_time}")


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
        time.sleep(delay)
        