import os
import signal
import sys
import time
import json
import pymysql

# Directory to monitor
monitor_dir = "/home/arya/Machine_test"  # Change this to the actual directory path
data_file = "data.json"
# Control flag for monitoring activity
monitoring_active = True

# Function to transform data and load to MySQL
def transform_and_load_to_sql(file_path):
    try:
        # Read and transform the JSON data
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Example transformation (customize this as needed)
        transformed_data = [(item['name'], item['base_price']) for item in data]

        # Connect to MySQL
        connection = pymysql.connect(
            host='localhost',
            user='aryasr@localhost',
            password='Aryasr@006',
            database='WEGMN'
        )
        cursor = connection.cursor()

        # Insert transformed data into MySQL (customize the query as needed)
        insert_query = "INSERT INTO WEGMN_TABLE (name, base_price) VALUES (%s, %s)"
        cursor.executemany(insert_query, transformed_data)
        connection.commit()

        cursor.close()
        connection.close()
        print("Data successfully transformed and loaded into MySQL.")
    except Exception as e:
        print(f"Error during transformation and loading to SQL: {e}")

# Function to monitor directory contents
def monitor_directory(directory, filename):
    print("Monitoring started for directory:", directory)
    old_contents = set(os.listdir(directory))
    try:
        while True:
            if monitoring_active:
                # Get current list of files and directories
                new_contents = set(os.listdir(directory))
                # Check for changes
                if filename in new_contents:
                    # Check if the file is newly added or modified
                    if filename not in old_contents:
                        print(f"{filename} added.")
                        transform_and_load_to_sql(os.path.join(directory, filename))
                    elif os.path.getmtime(os.path.join(directory, filename)) > time.time() - 2:
                        print(f"{filename} modified.")
                        transform_and_load_to_sql(os.path.join(directory, filename))
                old_contents = new_contents
            time.sleep(1)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

# Signal handler for pausing monitoring
def pause_monitoring(sig, frame):
    global monitoring_active
    monitoring_active = False
    print("Monitoring paused. Send SIGUSR2 to resume.")

# Signal handler for resuming monitoring
def resume_monitoring(sig, frame):
    global monitoring_active
    monitoring_active = True
    print("Monitoring resumed.")

# Set signal handlers
signal.signal(signal.SIGUSR1, pause_monitoring)
signal.signal(signal.SIGUSR2, resume_monitoring)

if __name__ == "__main__":
    monitor_directory(monitor_dir, data_file)
