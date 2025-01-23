import json
from datetime import datetime

# Load the JSON file
with open('d:/python/watch-history.json', 'r', encoding='utf-8') as file:
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
        duration = 600  # You can adjust this value as needed
        # Format the entry as a single string
        entry_string = f"{video_url}|||{timestamp}|||{duration}|||{title}"
        output.append(entry_string)

# Save the output as a JSON array
with open('d:/python/history', 'w', encoding='utf-8') as file:
    json.dump(output, file, indent=4)  # Use indent=4 for pretty-printing (optional)

print("Conversion complete! Check 'converted-history.json'.")
