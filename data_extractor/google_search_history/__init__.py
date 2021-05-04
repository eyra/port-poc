""" Script to extract info from Google Browser History """

__version__ = '0.1.0'

import json
import datetime as DT
import numpy as np
import pandas as pd
import re


def process(data):
    """Return relevant data from browser history pre and post specific date
    Args:
        data: BrowserHistory.json file
    Returns:
        dict: dict with summary and DataFrame with extracted data
    """
    # Enter date of event X (in this case 'avondklok')
    date = {'ingang_avondklok': np.datetime64(DT.datetime(2021, 1, 23, 21)).view('<i8'),
            'einde_avondklok': np.datetime64(DT.datetime(2021, 4, 28, 4, 30)).view('<i8')}
    # Enter news sites
    newssites = 'news.google.com|nieuws.nl|nos.nl|www.rtlnieuws.nl|nu.nl|at5.nl|ad.nl|bd.nl|telegraaf.nl|volkskrant.nl' \
        '|parool.nl|metronieuws.nl|nd.nl|nrc.nl|rd.nl|trouw.nl'
    # Extract moment (pre/during/after event X) and website (news/other)
    results = {'Moment': [], 'Website': []}
    for data_unit in data["Browser History"]:
        if data_unit["time_usec"] < date['ingang_avondklok']:
            results['Moment'].append('Voor avondklok')
        elif data_unit["time_usec"] > date['einde_avondklok']:
            results['Moment'].append('Na avondklok')
        else:
            results['Moment'].append('Tijdens avondklok')
        if re.findall(newssites, data_unit["url"]):
            results['Website'].append('Nieuws')
        else:
            results['Website'].append('Anders')
    # Put results in DataFrame
    results = pd.DataFrame(results)
    # Count number of news vs. other websites per moment
    data_frame = results.groupby(
        ['Moment', 'Website']).size().reset_index(name='Aantal')
    return {
        "summary": f"The following files where read: BrowserHistory.json.",
        "data": data_frame
    }


if __name__ == '__main__':

    with open(file_data, encoding='utf-8-sig') as f:
        data = json.load(f)

    result = process(data)
    print(result)
