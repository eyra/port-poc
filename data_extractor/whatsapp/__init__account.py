__version__ = '0.2.0'

import zipfile
import re
import pandas as pd
import json

HIDDEN_FILE_RE = re.compile(r".*__MACOSX*")
FILE_RE = re.compile(r".*.json$")


class ColnamesDf:
    GROUPS = 'groups'
    """Groups column"""

    CONTACTS = 'contacts'
    """Contacts column"""


COLNAMES_DF = ColnamesDf()


def format_results(df):
    results = []
    results.append(
        {
        "id": "Whatsapp account info",
        "title": "The account information file is read:",
        "data_frame": df
        }
    )
    return results


def format_errors(errors):
    data_frame = pd.DataFrame()
    data_frame["Messages"] = pd.Series(errors, name="Messages")
    return {"id": "extraction_log", "title": "Extraction log", "data_frame": data_frame}


def extract_data(log_error, data):
    # data = pd.read_csv('whatsapp/df_chat.csv')
    # return 1,1
    groups_no = 0
    contacts_no = 0
    try:
        groups_no = len(data[COLNAMES_DF.GROUPS])
    except (TypeError, KeyError) as e:
        print("No group is available")
    try:
        contacts_no = len(data[COLNAMES_DF.CONTACTS])
    except (TypeError, KeyError) as e:
        print("No contact is available")

    if (groups_no == 0) and (contacts_no == 0):
        log_error("Neither group nor contact is available")
    return groups_no, contacts_no


def parse_records(log_error, f):
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        log_error(f"Could not parse: {f.name}")
    else:
        return data


def parse_zipfile(log_error, zfile):
    for name in zfile.namelist():
        if HIDDEN_FILE_RE.match(name):
            continue
        if not FILE_RE.match(name):
            continue
        return parse_records(log_error, zfile.open(name))
    log_error("No Json file is available")


def process(file_data):
    errors = []
    log_error = errors.append
    zfile = zipfile.ZipFile(file_data)
    data = parse_zipfile(log_error, zfile)

    if data is not None:
        groups_no, contacts_no = extract_data(log_error, data)

    if errors:
        return [format_errors(errors)]

    d = {'number_of_groups': [groups_no], 'number_of_contacts': [contacts_no]}
    df = pd.DataFrame(data=d)
    formatted_results = format_results(df)

    return formatted_results

