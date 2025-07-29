import base64
import json
import os
from datetime import datetime, timezone

class TakeoutEntry:
    def __init__(self, url, time, title):
        self.header = "YouTube"
        self.title = title
        self.titleUrl = url
        self.time = datetime.fromtimestamp(time, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        self.products = ["YouTube"]
        self.activityControls = ["YouTube watch history"]
    
    def to_dict(self):
        return {
            "header": self.header,
            "title": self.title,
            "titleUrl": self.titleUrl,
            "time": self.time,
            "products": self.products,
            "activityControls": self.activityControls
        }


def convert(filename):
    with open(filename, 'r') as file:
        base64_string = file.read()

    json_string = base64.b64decode(base64_string).decode('utf-8')
    data = json.loads(json_string)

    output = []
    for entry in data:
        if "strIdent" in entry and "intTimestamp" in entry and "strTitle" in entry:
            video_id = entry["strIdent"]
            timestamp = entry["intTimestamp"] / 1000
            title = entry["strTitle"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            TE = TakeoutEntry(video_url, timestamp, title)
            output.append(TE)

    return output


if __name__ == "__main__":
    input_file = "watchmarker.database"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print("Please make sure the watchmarker.database file is in the current directory.")
        exit(1)
    
    # Convert watchmarker.database file
    result = convert(input_file)
    
    # Convert TakeoutEntry objects to dictionaries for JSON serialization
    output_data = [entry.to_dict() for entry in result]
    
    # Save to watchmarker_takeout.json
    with open("watchmarker_takeout.json", 'w', encoding='utf-8') as output_file:
        json.dump(output_data, output_file, indent=2, ensure_ascii=False)
    
    print(f"Successfully converted {len(result)} entries from watchmarker.database to watchmarker_takeout.json")

