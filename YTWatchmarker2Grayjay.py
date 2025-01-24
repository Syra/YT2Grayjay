import base64
import json
import os
import zipfile

# Define paths
input_path = "D:/python/export.txt"  # Path to the base64-encoded file
output_dir = "D:/python/"

zip_path = os.path.join(output_dir, "output.zip")


#leave that alone
stores_dir = os.path.join(output_dir, "stores")
output_file = os.path.join(output_dir, "history")

os.makedirs(stores_dir, exist_ok=True)

# Read the base64-encoded file
try:
    with open(input_path, 'r') as file:
        base64_string = file.read()

    # Decode the base64 string
    json_string = base64.b64decode(base64_string).decode('utf-8')

    #  Parse the JSON string into a Python object
    data = json.loads(json_string)

    # Convert each entry
    output = []
    for entry in data:
        if "strIdent" in entry and "intTimestamp" in entry and "strTitle" in entry:
            video_id = entry["strIdent"]
            timestamp = entry["intTimestamp"] // 1000  # Convert milliseconds to seconds
            title = entry["strTitle"]
            # Assume the video was fully watched (set duration to a placeholder, e.g., 60000 seconds)
            duration = 60000  # You can adjust this value as needed
            # Format the entry as a single string
            video_url = f"https://www.youtube.com/watch?v={video_id}"
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
        zipf.write(history_path, arcname=os.path.join("stores", "history"))
        zipf.write(exportinfo_path, arcname="exportinfo")

    # Clean up temporary files
    os.remove(history_path)
    os.remove(exportinfo_path)
    os.rmdir(stores_dir)

    print(f"Conversion complete! Zip file created at {zip_path}.")

except Exception as e:
    print(f"Error processing the file: {e}")
