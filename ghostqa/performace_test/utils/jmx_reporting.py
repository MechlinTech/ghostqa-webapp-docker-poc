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
    metrics["errorPct"] = float(metrics["errorCount"] / metrics["sampleCount"] * 100)

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
    metrics["throughput"] = float(metrics["sampleCount"] / (data["elapsed"].max() / 1000))

    # Calculate received and sent KBytes per second
    metrics["receivedKBytesPerSec"] = float(data["bytes"].sum() / (data["elapsed"].max() / 1000))
    metrics["sentKBytesPerSec"] = float(data["sentBytes"].sum() / (data["elapsed"].max() / 1000))

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
        "errorPct": float(len(df[df["success"] == False]) / df.shape[0] * 100),
        "meanResTime": float(df["elapsed"].mean()),
        "medianResTime": float(df["elapsed"].median()),
        "minResTime": float(df["elapsed"].min()),
        "maxResTime": float(df["elapsed"].max()),
        "pct1ResTime": float(df["elapsed"].quantile(0.01)),
        "pct2ResTime": float(df["elapsed"].quantile(0.02)),
        "pct3ResTime": float(df["elapsed"].quantile(0.03)),
        "throughput": float(df.shape[0] / (df["elapsed"].max() / 1000)),
        "receivedKBytesPerSec": float(df["bytes"].sum() / (df["elapsed"].max() / 1000)),
        "sentKBytesPerSec": float(df["sentBytes"].sum() / (df["elapsed"].max() / 1000))
    }

    # Add total metrics to the results dictionary
    results["Total"] = total_metrics
    
    # Serialize results to JSON
    return results

def csv_to_json(csv_file_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
        # Replace NaN values with None
    df.replace({np.nan: None}, inplace=True)
    # Convert DataFrame to JSON
    json_data = df.to_dict(orient='records')
    with open("example.json", 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    return json_data