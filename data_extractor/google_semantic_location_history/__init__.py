__version__ = '0.1.0'

import json
import collections
import itertools
import re
import zipfile

import pandas as pd

def process(file_data):
    """Return relevant data from zipfile for years and months
    Args:
        file_data: zipfile
        years: list with years
        months: list with months

    Returns:
        pd.DataFrame: dataframe with relevant info
    """
    years = [2020, 2021]
    months = ["JANUARY"]
    results = []
    names = []
    with zipfile.ZipFile(file_data) as zfile:
        for year in years:
            for month in months:
                for name in zfile.namelist():
                    monthfile = f"{year}_{month}.json"
                    if re.search(monthfile, name) is not None:
                        names.append(name)
                        break
                data = json.loads(zfile.read(name).decode("utf8"))
                placevisit_duration = []
                activity_duration = 0.0
                for data_unit in data["timelineObjects"]:
                    if "placeVisit" in data_unit.keys():
                        address = data_unit["placeVisit"]["location"]["address"].split("\n")[0]
                        start_time = data_unit["placeVisit"]["duration"]["startTimestampMs"]
                        end_time = data_unit["placeVisit"]["duration"]["endTimestampMs"]
                        placevisit_duration.append(
                            {address: (int(end_time) - int(start_time))/(1e3*24*60*60)})
                    if "activitySegment" in data_unit.keys():
                        start_time = data_unit["activitySegment"]["duration"]["startTimestampMs"]
                        end_time = data_unit["activitySegment"]["duration"]["endTimestampMs"]
                        activity_duration += (int(end_time) - int(start_time))/(1e3*24*60*60)

                address_list = [list(duration.keys())[0] for duration in placevisit_duration]
                place_duration = sum(
                    [list(duration.values())[0] for duration in placevisit_duration])

                locations = {}
                for address in set(address_list):
                    loc_duration = sum(
                        [duration[address] for duration in placevisit_duration \
                            if address == list(duration.keys())[0]])
                    locations[address] = loc_duration

                sorted_places = collections.OrderedDict(
                    sorted(locations.items(), key=lambda kv: kv[1], reverse=True))
                top_locations = dict(itertools.islice(sorted_places.items(),3))
                number = len(set(address_list))

                results.append({
                    "Year": year,
                    "Month": month,
                    "Locations": top_locations,
                    "Number of Locations": number,
                    "Place Duration": place_duration,
                    "Acitivity Duration": activity_duration})

    return {
        "summary": f"The following files where read: {', '.join(names)}.",
        "data": pd.json_normalize(results)
    }

if __name__ == '__main__':

    result = process("tests/data/takeout-test.zip")
    print(result)