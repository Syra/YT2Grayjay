import json
from datetime import datetime
import os
import zipfile

# Define paths
input_path = "D:/python/watch-history.json"
output_dir = "D:/python/"
output_file = os.path.join(output_dir, "history")
zip_path = os.path.join(output_dir, "output.zip")
stores_dir = os.path.join(output_dir, "stores")

# Create the "stores" subdirectory if it doesn't exist
os.makedirs(stores_dir, exist_ok=True)

# Load the JSON file
with open(input_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert each entry
output = []
for entry in data:
    if "titleUrl" in entry and "time" in entry and "title" in entry:
        video_url = entry["titleUrl"]
        try:
            # Extract video ID from URL
            if "v=" in video_url:
                video_id = video_url.split("v=")[1]
                # Handle cases where additional parameters are present
                if "&" in video_id:
                    video_id = video_id.split("&")[0]
            else:
                # Skip entries without a valid video ID
                print(f"Skipping invalid URL: {video_url}")
                continue
        except IndexError:
            # Skip entries where the video ID cannot be extracted
            print(f"Skipping malformed URL: {video_url}")
            continue

        # Convert timestamp to Unix time
        try:
            timestamp = int(datetime.strptime(entry["time"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
        except ValueError:
            # Skip entries with invalid timestamps
            print(f"Skipping invalid timestamp: {entry['time']}")
            continue

        title = entry["title"]
        # Assume the video was fully watched (set duration to a placeholder, e.g., 600 seconds)
        duration = 60000  # You can adjust this value as needed
        # Format the entry as a single string
        entry_string = f"{video_url}|||{timestamp}|||{duration}|||{title}"
        output.append(entry_string)

# Save the output as a JSON array in the "stores" subdirectory
history_path = os.path.join(stores_dir, "history")
with open(history_path, 'w', encoding='utf-8') as file:
    json.dump(output, file)

# Create the "exportinfo" file in the root of the zip
exportinfo_path = os.path.join(output_dir, "exportinfo")
with open(exportinfo_path, 'w', encoding='utf-8') as file:
    file.write('{"version":"1"}')

# Create the zip file
with zipfile.ZipFile(zip_path, 'w') as zipf:
    # Add the "history" file from the "stores" subdirectory
    zipf.write(history_path, arcname=os.path.join("stores", "history"))
    # Add the "exportinfo" file to the root of the zip
    zipf.write(exportinfo_path, arcname="exportinfo")

# Clean up temporary files
os.remove(history_path)
os.remove(exportinfo_path)
os.rmdir(stores_dir)

print(f"Conversion complete! Zip file created at {zip_path}.")
