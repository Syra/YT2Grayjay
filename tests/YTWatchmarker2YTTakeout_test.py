import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import YTWatchmarker2Takeout

def test_convestion():
    takeout = open('./tests/takeout.json')
    expected_list = json.load(takeout)

    watchmaker = YTWatchmarker2Takeout.convert('./tests/YTWatchmaker.database')

    for expected in expected_list:
        el = next((x for x in watchmaker if x.titleUrl == expected.get("titleUrl")), None)
        assert el is not None
        # Compare only URLs, as watchmaker do not store timestamp of watching.
        # And youtube takeout doesn't always preserve the titles.
        assert el.titleUrl==expected.get("titleUrl")
