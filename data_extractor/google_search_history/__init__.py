__version__ = '0.1.0'

import json
import datetime as DT
import numpy as np
import pandas as pd
import re


def process(file_data):
    """Return relevant data from browser history pre and post specific date
    Args:
        file_data: BrowserHistory.json file
        date: dictionary with date cut-offs

    Returns:
        pd.DataFrame: dataframe with relevant info
    """

    with open(file_data, encoding='utf-8-sig') as f:
        data = json.load(f)

    date = {'ingang_avondklok': np.datetime64(DT.datetime(2021, 1, 23, 21)).view('<i8'),
            'einde_avondklok': np.datetime64(DT.datetime(2021, 4, 28, 4, 30)).view('<i8')}

    newssites = 'news.google.com|nieuws.nl|nos.nl|www.rtlnieuws.nl|nu.nl|at5.nl|ad.nl|bd.nl|telegraaf.nl|volkskrant.nl' \
        '|parool.nl|metronieuws.nl|nd.nl|nrc.nl|rd.nl|trouw.nl'

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

    results = pd.DataFrame(results)

    return {
        "summary": f"The following files where read: {file_data}.",
        "data": results.groupby(['Moment', 'Website']).size().reset_index(name='Aantal')
    }


if __name__ == '__main__':

    result = process("tests/data/BrowserHistory.json")
    print(result)
