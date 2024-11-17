import pandas as pd
import os

# Define the input and output directories
input_directory = "NOAA_data"
output_directory = "NOAA_data_cleaned"

# Function to ensure a directory exists
def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to clean a single CSV file
def clean_noaa_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Remove the "attributes" column if not needed
    if "attributes" in df.columns:
        df = df.drop(columns=["attributes"])

    # Scale values for certain data types
    # Precipitation (PRCP), snowfall (SNOW), snow depth (SNWD) are in tenths of mm
    # Temperature values (TMAX, TMIN, TOBS) are in tenths of degrees Celsius
    scale_columns = ["PRCP", "SNOW", "SNWD", "TMAX", "TMIN", "TOBS"]
    df["value"] = df.apply(
        lambda row: row["value"] / 10 if row["datatype"] in scale_columns else row["value"],
        axis=1
    )

    # Rename the "value" column to include units (optional)
    df.rename(columns={"value": "value_scaled"}, inplace=True)

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Sort by date, station, and datatype for better organization
    df = df.sort_values(by=["date", "station", "datatype"])

    return df

# Process all CSV files in the NOAA_data directory
def process_all_files(input_dir, output_dir):
    ensure_directory(output_dir)  # Ensure output directory exists

    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            print(f"Cleaning {filename}...")

            # Clean the file
            cleaned_df = clean_noaa_data(file_path)

            # Save the cleaned file to the output directory
            cleaned_file_path = os.path.join(output_dir, filename)
            cleaned_df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")

# Run the cleaning process
process_all_files(input_directory, output_directory)
