"""Test data extraction from Google Browser History .json file"""

import pandas as pd
from google_search_history import process

DATA = {
    "Browser History": [
        {
            "page_transition": "LINK",
            "title": "title1",
            "url": "https://www.nu.nl/coronavirus/6131452/rivm-afgelopen-week-minder-getest-percentage-positief-stijgt.html",
            "client_id": "client_id1",
            "time_usec": 1611262800000000},
        {
            "page_transition": "LINK",
            "title": "title2",
            "url": "https://www.uu.nl/",
            "client_id": "client_id2",
            "time_usec": 1611349200000000},
        {
            "page_transition": "LINK",
            "title": "title3",
            "url": "https://nos.nl/artikel/2379383-rivm-bezorgd-om-hoge-coronacijfers-onder-40-tot-60-jarigen",
            "client_id": "client_id3",
            "time_usec": 1614373200000000},
        {
            "page_transition": "LINK",
            "title": "title4",
            "url": "https://www.ns.nl/",
            "client_id": "client_id4",
            "time_usec": 1614286800000000},
        {
            "page_transition": "LINK",
            "title": "title5",
            "url": "https://www.nrc.nl/nieuws/2021/05/03/coronablog-4-mei-a4042259",
            "client_id": "client_id5",
            "time_usec": 1619816400000000},
        {
            "page_transition": "LINK",
            "title": "title6",
            "url": "https://www.bol.com/nl/p/jan-van-haasteren-ontbrekende-stukje-puzzel-1000-stukjes/9300000031132593/?bltgh=mjRTtZln6O-wVT40MgZKoA.4_12.13.ProductImage",
            "client_id": "client_id6",
            "time_usec": 1619730000000000}
    ]
}


def test_process():
    result = process(DATA)
    print(result["data"])

    expected = {'Moment': {0: 'Na avondklok', 1: 'Na avondklok', 2: 'Tijdens avondklok', 3: 'Tijdens avondklok', 4: 'Voor avondklok', 5: 'Voor avondklok'}, 'Website': {
        0: 'Anders', 1: 'Nieuws', 2: 'Anders', 3: 'Nieuws', 4: 'Anders', 5: 'Nieuws'}, 'Aantal': {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}}

    assert result["data"].to_dict() == expected
