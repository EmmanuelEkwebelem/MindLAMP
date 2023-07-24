import os
import csv
import pandas as pd

# Folder paths and output file
folder_path1 = "AHImindLAMP Additional surveys and analytics"
folder_path2 = "AHI_mindLAMP_Lab Testing Data"
output_file = "Combined.csv"

# Get a list of all CSV files in the first folder and its subfolders
csv_files1 = []
for root, dirs, files in os.walk(folder_path1):
    for file in files:
        if file.endswith(".csv"):
            csv_files1.append(os.path.join(root, file))

# Get a list of all CSV files in the second folder and its subfolders
csv_files2 = []
for root, dirs, files in os.walk(folder_path2):
    for file in files:
        if file.endswith(".csv"):
            csv_files2.append(os.path.join(root, file))

# Combine both lists of CSV files
csv_files = csv_files1 + csv_files2

# Initialize the combined data list with column titles
combined_data = []

# Iterate over each CSV file
for file_path in csv_files:
    folder_name = os.path.basename(os.path.dirname(file_path))

    # Extract user ID and folder type
    if folder_path1 in file_path:
        user_id = folder_name.split()[0]
        folder_category = folder_name.split()[1]
    elif folder_path2 in file_path:
        user_id = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
        folder_category = folder_name

    # Extract CSV date and user designation
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    file_parts = file_name.split("+")
    csv_date = file_parts[0]
    csv_user_designation = file_parts[1] if len(file_parts) > 1 else ""

    # Read the CSV file and append the data rows to the combined data list
    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)

        # Extract unique column titles from the first row
        column_titles = data[0]

        # Iterate over the data rows
        for row in data[1:]:
            # Create a dictionary to hold the row data
            row_data = {
                "UserID": user_id,
                "Category": folder_category,
                "Date": csv_date,
                "UserDesignation": csv_user_designation,
            }

            # Fill in the row data for the columns present in the CSV file
            for i, value in enumerate(row):
                if i < len(column_titles):
                    column_title = column_titles[i]
                    row_data[column_title] = value

            # Append the row data to the combined data list
            combined_data.append(row_data)

# Get the unique column titles from all CSV files
all_column_titles = set().union(*(row.keys() for row in combined_data))

# Prepare the final combined data as a list of dictionaries
final_data = []
for row_data in combined_data:
    # Create a dictionary with empty values for all column titles
    final_row_data = {column_title: "" for column_title in all_column_titles}
    final_row_data.update(row_data)  # Update with the actual row data
    final_data.append(final_row_data)

# Sort the final data rows based on UserID and Date
final_data.sort(key=lambda x: (x['UserID'], x['Date']))

# Convert Unix time to datetime in GMT-04:00 DST time
for row in final_data:
    row['timestamp'] = pd.to_datetime(row['timestamp'], unit='ms').tz_localize('UTC').tz_convert('America/New_York')

# Convert timestamp to 12-hour format with AM/PM
for row in final_data:
    row['timestamp'] = row['timestamp'].strftime('%Y-%m-%d %I:%M:%S %p')

# Convert the final combined data to a Pandas DataFrame
df = pd.DataFrame(final_data)

# Reorder the columns according to the provided list
ordered_column_titles = ['UserID', 'Category', 'Date', 'UserDesignation', 'timestamp', 'type', 'duration', 'value', 'item',
                         'action', 'user_agent', 'page', 'device_token', 'message', 'name', 'level', 'device_type',
                         'activity', 'latitude', 'longitude', 'source', 'accuracy', 'battery_level', 'representation',
                         'unit', 'altitude']
df = df[ordered_column_titles]

# Print the shape of the DataFrame
print("DataFrame shape:", df.shape)

# Save the combined data to a CSV file
df.to_csv(output_file, index=False)
