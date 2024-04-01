import pandas as pd
import json
import numpy as np
# Read the CSV file into a DataFrame

# Define the function to calculate metrics
def calculate_metrics(data):
    metrics = {}

    # Transaction name (assuming 'label' column contains transaction names)
    transaction_name = data["label"].iloc[0]
    metrics["transaction"] = transaction_name

    # Total sample count
    metrics["sampleCount"] = float(len(data))

    # Error count
    metrics["errorCount"] = float(len(data[data["success"] == False]))

    # Error percentage
    # metrics["errorPct"] = float(metrics["errorCount"] / metrics["sampleCount"] * 100)
    
    try:
        metrics["errorPct"] = float(metrics["errorCount"] / metrics["sampleCount"] * 100)
    except ZeroDivisionError:
        metrics["errorPct"] = 0.0

    # Mean response time
    metrics["meanResTime"] = float(data["elapsed"].mean())

    # Median response time
    metrics["medianResTime"] = float(data["elapsed"].median())

    # Minimum response time
    metrics["minResTime"] = float(data["elapsed"].min())

    # Maximum response time
    metrics["maxResTime"] = float(data["elapsed"].max())

    # Percentile response time (you can adjust the percentiles as needed)
    metrics["pct1ResTime"] = float(data["elapsed"].quantile(0.01))
    metrics["pct2ResTime"] = float(data["elapsed"].quantile(0.02))
    metrics["pct3ResTime"] = float(data["elapsed"].quantile(0.03))

    # Throughput (requests per second)
    # metrics["throughput"] = float(metrics["sampleCount"] / (data["elapsed"].max() / 1000))

    # # Calculate received and sent KBytes per second
    # metrics["receivedKBytesPerSec"] = float(data["bytes"].sum() / (data["elapsed"].max() / 1000))
    # metrics["sentKBytesPerSec"] = float(data["sentBytes"].sum() / (data["elapsed"].max() / 1000))
    # Throughput (requests per second)
    try:
        metrics["throughput"] = float(metrics["sampleCount"] / (data["elapsed"].max() / 1000))
    except ZeroDivisionError:
        metrics["throughput"] = 0.0

    # Calculate received and sent KBytes per second
    try:
        metrics["receivedKBytesPerSec"] = float(data["bytes"].sum() / (data["elapsed"].max() / 1000))
    except ZeroDivisionError:
        metrics["receivedKBytesPerSec"] = 0.0

    try:
        metrics["sentKBytesPerSec"] = float(data["sentBytes"].sum() / (data["elapsed"].max() / 1000))
    except ZeroDivisionError:
        metrics["sentKBytesPerSec"] = 0.0

    return transaction_name, metrics



def get_json_metrics(file_path):
    df = pd.read_csv(file_path)


    # Group data by transaction label and calculate metrics for each group
    grouped_data = df.groupby("label").apply(calculate_metrics)

    # Create a dictionary to store the results
    results = {}

    # Iterate over grouped data and populate the results dictionary
    for transaction_name, metrics in grouped_data:
        results[transaction_name] = metrics

    # Calculate total metrics
    total_metrics = {
        "transaction": "Total",
        "sampleCount": float(df.shape[0]),
        "errorCount": float(len(df[df["success"] == False])),
        # "errorPct": float(len(df[df["success"] == False]) / df.shape[0] * 100),
        "meanResTime": float(df["elapsed"].mean()),
        "medianResTime": float(df["elapsed"].median()),
        "minResTime": float(df["elapsed"].min()),
        "maxResTime": float(df["elapsed"].max()),
        "pct1ResTime": float(df["elapsed"].quantile(0.01)),
        "pct2ResTime": float(df["elapsed"].quantile(0.02)),
        "pct3ResTime": float(df["elapsed"].quantile(0.03))
        # "throughput": float(df.shape[0] / (df["elapsed"].max() / 1000)),
        # "receivedKBytesPerSec": float(df["bytes"].sum() / (df["elapsed"].max() / 1000)),
        # "sentKBytesPerSec": float(df["sentBytes"].sum() / (df["elapsed"].max() / 1000))
    }
    
    try:
        total_metrics["errorPct"] = float(len(df[df["success"] == False]) / df.shape[0] * 100)
    except ZeroDivisionError:
        total_metrics["errorPct"] = 0.0
    
    try:
        total_metrics["throughput"] = float(df.shape[0] / (df["elapsed"].max() / 1000))
    except ZeroDivisionError:
        total_metrics["throughput"] = 0.0
    
    try:
        total_metrics["receivedKBytesPerSec"] = float(df["bytes"].sum() / (df["elapsed"].max() / 1000))
    except ZeroDivisionError:
        total_metrics["receivedKBytesPerSec"] = 0.0
        
    try:
        total_metrics["sentKBytesPerSec"] = float(df["sentBytes"].sum() / (df["elapsed"].max() / 1000))
    except ZeroDivisionError:
        total_metrics["sentKBytesPerSec"] = 0.0

    # Add total metrics to the results dictionary
    results["Total"] = total_metrics
    
    # Serialize results to JSON
    return results

def calculate_bandwidth(df):
    # Calculate bandwidth in bytes per second
    df['bandwidth'] = df['bytes'] / df['elapsed']

    # Fill NaN values with 0
    df['bandwidth'].fillna(0, inplace=True)


def calculate_errors_per_second(df):
    # Convert 'timeStamp' column to datetime format
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')

    # Filter the DataFrame to include only failed requests
    failed_requests = df[df['success'] == False]

    # Calculate errors per second
    errors_per_second = failed_requests.groupby(pd.Grouper(key='timeStamp', freq='1s')).size()

    # Fill NaN values with 0
    errors_per_second.fillna(0, inplace=True)

    # Create a new DataFrame to store errors per second
    errors_df = pd.DataFrame(errors_per_second, columns=['Errors_per_second'])

    # Merge errors_per_second back to the original DataFrame
    df = df.merge(errors_df, how='left', left_on='timeStamp', right_index=True)

def calculate_hits_per_second(df):
    # Convert 'timeStamp' column to datetime format
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')

    # Calculate Hits per second
    df['Hits_per_second'] = df.groupby(pd.Grouper(key='timeStamp', freq='1s')).size()

    # Fill NaN values with 0
    df['Hits_per_second'].fillna(0, inplace=True)
    
def calculate_90th_percentile(df):
    # Convert 'timeStamp' column to datetime format
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')

    # Convert 'elapsed' column to numeric if needed
    df['elapsed'] = pd.to_numeric(df['elapsed'], errors='coerce')

    # Calculate the 90th percentile response time
    df['timeStamp'] = df['timeStamp'].dt.floor('s')  # Round down to nearest second
    percentile_90 = df.groupby('timeStamp')['elapsed'].quantile(0.90)

    # Merge the 90th percentile data into the original DataFrame
    df = df.merge(percentile_90, left_on='timeStamp', right_index=True, suffixes=('', '_90th_percentile'))

    # Rename the column to indicate it contains the 90th percentile response time
    df.rename(columns={'elapsed_90th_percentile': '90th_percentile_response_time'}, inplace=True)

def csv_to_json(csv_file_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
        # Replace NaN values with None
    calculate_hits_per_second(df)
    calculate_errors_per_second(df)
    calculate_bandwidth(df)
    calculate_90th_percentile(df)
    
    df.replace({np.nan: None}, inplace=True)
    # Convert DataFrame to JSON
    json_data = df.to_dict(orient='records')
    with open("example.json", 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    return json_data