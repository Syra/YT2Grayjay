import base64
import json
from datetime import datetime, timezone

class TakeoutEntry:
    def __init__(self, url, time, title):
        self.header = "YouTube"
        self.title = title
        self.titleUrl = url
        self.time = datetime.fromtimestamp(time, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        self.products = ["YouTube"]
        self.activityControls = ["YouTube watch history"]


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

