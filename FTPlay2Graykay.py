#Freetube Playlists to Grayjay conversion
import json
import os
import zipfile

# Define paths
input_path = "D:/python/freetube-playlists.db"  # Path to the FreeTube playlist file (NDJSON)
output_dir = "D:/python/"
zip_path = os.path.join(output_dir, "grayjay_playlists.zip")

# Directory and file for the playlists
exports_dir = os.path.join(output_dir, "exports")
playlists_path = os.path.join(exports_dir, "Playlists")

# Create directories if they don’t exist
os.makedirs(exports_dir, exist_ok=True)

try:
    # Read the NDJSON file (each line is a separate JSON object)
    data = []
    with open(input_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file, 1):
            line = line.strip()  # Remove any whitespace or newlines
            if not line:  # Skip empty lines
                continue
            try:
                # Debug: Print the first few characters of each line to confirm format
                print(f"Line {i} (first 50 chars): {line[:50]}")
                playlist = json.loads(line)
                data.append(playlist)
            except json.JSONDecodeError as e:
                print(f"Failed to parse line {i} as JSON: {line}")
                print(f"JSON error: {e}")
                continue

    # Debug: Print the number of playlists parsed
    print(f"Total playlists parsed: {len(data)}")

    # Convert FreeTube playlists to GrayJay format
    grayjay_playlists = []
    for playlist in data:
        if "playlistName" in playlist and "videos" in playlist:
            playlist_name = playlist["playlistName"]
            videos = playlist["videos"]

            # Build the playlist string: name followed by video URLs
            playlist_lines = [playlist_name]
            for video in videos:
                if "videoId" in video:
                    video_url = f"https://www.youtube.com/watch?v={video['videoId']}"
                    playlist_lines.append(video_url)

            # Join with newlines to match GrayJay format
            playlist_string = "\n".join(playlist_lines)
            grayjay_playlists.append(playlist_string)

    # Save the playlists as a JSON array
    with open(playlists_path, 'w', encoding='utf-8') as file:
        json.dump(grayjay_playlists, file, ensure_ascii=False)

    # Create the "exportinfo" file (assuming GrayJay requires it, as in your history script)
    exportinfo_path = os.path.join(output_dir, "exportinfo")
    with open(exportinfo_path, 'w', encoding='utf-8') as file:
        file.write('{"version":"1"}')

    # Create the zip file
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(playlists_path, arcname=os.path.join("exports", "Playlists"))
        zipf.write(exportinfo_path, arcname="exportinfo")

    # Clean up temporary files
    os.remove(playlists_path)
    os.remove(exportinfo_path)
    os.rmdir(exports_dir)

    print(f"Conversion complete! Zip file created at {zip_path}.")

except Exception as e:
    print(f"Error processing the file: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    print(traceback.format_exc())
