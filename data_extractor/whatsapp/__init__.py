"""Parser utils.
   The main part is extracted from https://github.com/lucasrodes/whatstk.git
"""
__version__ = '0.2.0'

import os
import re
from datetime import datetime
import pandas as pd
import hashlib
import zipfile


URL_PATTERN = r'(https?://\S+)'
LOCATION_PATTERN = r'(Location: https?://\S+)'
ATTACH_FILE_PATTERN = r'(<attached: \S+>)'
FILE_RE = re.compile(r".*chat.*.txt$")
HIDDEN_FILE_RE = re.compile(r".*__MACOSX*")

hformats = ['%m/%d/%y, %H:%M - %name:','[%d/%m/%y, %H:%M:%S] %name:','%d-%m-%y %H:%M - %name:']



class ColnamesDf:
    """Access class constants using variable ``utils.COLNAMES_DF``.
    """
    DATE = 'date'
    """Date column"""

    USERNAME = 'username'
    """Username column"""

    MESSAGE = 'message'
    """Message column"""

    MESSAGE_LENGTH = 'message_length'
    """Message length column"""

    FirstMessage = 'first_message_date'
    """Date of first message column"""

    LastMessage = 'last_message_date'
    """Date of last message column"""

    MESSAGE_NO = 'message_no'
    """Number of Message  column"""

    WORDS_NO = 'total_words_no'
    """Total number of words  column"""

    REPLY_2USER = 'reply_2_user'
    """Who replies to the user the most column"""

    MAX_REPLY_2 = 'max_reply_2'
    """User replies to who the most column"""

    USER_REPLY2 = 'user_reply2'
    """User replies to who the most column"""

    URL_NO = 'url_no'
    """Number of URLs column"""

    LOCATION_NO = 'location_no'
    """Number of locations column"""

    FILE_NO = 'file_no'
    """Number of files column"""

    OUT_DEGREE = 'out_degree'
    """Total number of sent message column"""

    IN_DEGREE = 'in_degree'
    """Total number of received message column"""

    EMOJI_NO = 'emoji_no'
    """Total number of emojies column"""

    EMOJI_Fav = 'emoji_fav'
    """Favorite emojies column"""


COLNAMES_DF = ColnamesDf()

# *** parsing functions ***
regex_simplifier = {
    '%Y': r'(?P<year>\d{2,4})',
    '%y': r'(?P<year>\d{2,4})',
    '%m': r'(?P<month>\d{1,2})',
    '%d': r'(?P<day>\d{1,2})',
    '%H': r'(?P<hour>\d{1,2})',
    '%I': r'(?P<hour>\d{1,2})',
    '%M': r'(?P<minutes>\d{2})',
    '%S': r'(?P<seconds>\d{2})',
    '%P': r'(?P<ampm>[AaPp].? ?[Mm].?)',
    '%p': r'(?P<ampm>[AaPp].? ?[Mm].?)',
    '%name': fr'(?P<{COLNAMES_DF.USERNAME}>[^:]*)'
}


def generate_regex(log_error, hformat):
    r"""Generate regular expression from hformat.

    Args:
        log_error (list): Includes list of error messages.
        hformat (str): Simplified syntax for the header, e.g. ``'%y-%m-%d, %H:%M:%S - %name:'``.

    Returns:
        str: Regular expression corresponding to the specified syntax.

    """
    items = re.findall(r'\%\w*', hformat)

    for i in items:
        try:
            hformat = hformat.replace(i, regex_simplifier[i])
        except KeyError:
            log_error(f"Could find regular expression for : {i}")

    hformat = hformat + ' '
    hformat_x = hformat.split('(?P<username>[^:]*)')[0]
    return hformat, hformat_x


def add_schema(df):
    """Add default chat schema to df.
    Args:
        df (pandas.DataFrame): Chat dataframe.
    Returns:
        pandas.DataFrame: Chat dataframe with correct dtypes.
    """
    df = df.astype({
        COLNAMES_DF.DATE: pd.StringDtype(),
        COLNAMES_DF.USERNAME: pd.StringDtype(),
        COLNAMES_DF.MESSAGE: pd.StringDtype()
    })
    return df


def parse_line(text, headers, i):
    """Get date, username and message from the i:th intervention.
    Args:
        text (str): Whole log chat text.
        headers (list): All headers.
        i (int): Index denoting the message number.
    Returns:
        dict: i:th date, username and message.
    """
    result_ = headers[i].groupdict()
    if 'ampm' in result_:
        hour = int(result_['hour'])
        mode = result_.get('ampm').lower()
        if hour == 12 and mode == 'am':
            hour = 0
        elif hour != 12 and mode == 'pm':
            hour += 12
    else:
        hour = int(result_['hour'])

    # Check format of year. If year is 2-digit represented we add 2000
    if len(result_['year']) == 2:
        year = int(result_['year']) + 2000
    else:
        year = int(result_['year'])

    if 'seconds' not in result_:
        date = datetime(year, int(result_['month']), int(result_['day']), hour,
                        int(result_['minutes']))
    else:
        date = datetime(year, int(result_['month']), int(result_['day']), hour,
                        int(result_['minutes']), int(result_['seconds']))
    username = result_[COLNAMES_DF.USERNAME]
    message = get_message(text, headers, i)
    line_dict = {
        COLNAMES_DF.DATE: date,
        COLNAMES_DF.USERNAME: username,
        COLNAMES_DF.MESSAGE: message
    }
    return line_dict


def remove_alerts_from_df(r_x, df):
    """Try to get rid of alert/notification messages.
    Args:
        r_x (str): Regular expression to detect whatsapp warnings.
        df (pandas.DataFrame): DataFrame with all interventions.
    Returns:
        pandas.DataFrame: Fixed version of input dataframe.
    """
    df_new = df.copy()
    df_new.loc[:, COLNAMES_DF.MESSAGE] = df_new[COLNAMES_DF.MESSAGE].apply(lambda x: remove_alerts_from_line(r_x, x))
    return df_new


def remove_alerts_from_line(r_x, line_df):
    """Remove line content that is not desirable (automatic alerts etc.).
    Args:
        r_x (str): Regula expression to detect WhatsApp warnings.
        line_df (str): Message sent as string.
    Returns:
        str: Cleaned message string.
    """
    if re.search(r_x, line_df):
        return line_df[:re.search(r_x, line_df).start()]
    else:
        return line_df


def get_message(text, headers, i):
    """Get i:th message from text.
    Args:
        text (str): Whole log chat text.
        headers (list): All headers.
        i (int): Index denoting the message number.
    Returns:
        str: i:th message.
    """
    msg_start = headers[i].end()
    msg_end = headers[i + 1].start() if i < len(headers) - 1 else headers[i].endpos
    msg = text[msg_start:msg_end].strip()
    return msg


def parse_text(text, regex):
    """Parse chat using given regex.

    Args:
        text (str) Whole log chat text.
        regex (str): Regular expression

    Returns:
        pandas.DataFrame: DataFrame with messages sent by users, index is the date the messages was sent.

    Raises:
        RegexError: When provided regex could not match the text.

    """
    result = []
    headers = list(re.finditer(regex, text))
    try:
        for i in range(len(headers)):
            line_dict = parse_line(text, headers, i)
            result.append(line_dict)
    except KeyError:
        print("Could not match the provided regex with provided text. No match was found.")
        return None

    df_chat = pd.DataFrame.from_records(result)
    df_chat = df_chat[[COLNAMES_DF.DATE,COLNAMES_DF.USERNAME, COLNAMES_DF.MESSAGE]]

    # clean username
    df_chat[COLNAMES_DF.USERNAME] = df_chat[COLNAMES_DF.USERNAME].apply(lambda u: u.strip('\u202c'))

    return df_chat


def make_chat_df(log_error, text, hformat):
    """Load chat as a DataFrame.

        Args:
            log_error (list): Includes list of error messages.
            text (str): Text of the chat
            hformat (str): Simplified syntax for the header, e.g. ``'%y-%m-%d, %H:%M:%S - %name:'``.

        Returns:
            DataFrame: a DataFrame with three columns, i.e. 'date', 'username', and 'message'
    """
    # Bracket is reserved character in RegEx, add backslash before them.
    hformat = hformat.replace('[', r'\[').replace(']', r'\]')

    # Generate regex for given hformat
    r, r_x = generate_regex(log_error,hformat=hformat)

    # Parse chat to DataFrame
    try:
        df = parse_text(text, r)
        df = remove_alerts_from_df(r_x, df)
        df = add_schema(df)

        return df
    except:
        print(f"hformat : {hformat} is not match with the given text")
        return None


def parse_chat(log_error, data):
    """Parse chat and test it with defined hformats

    Args:
        log_error (list): Includes list of error messages.
        data (str): Data read from the chat file
    Returns:
        DataFrame: a DataFrame with three columns, i.e. 'date', 'username', and 'message'

    """
    for hformat in hformats:
        # Build dataframe
        df = make_chat_df(log_error, data, hformat)
        if df is not None:
             return df
    log_error("hformats did not match the provided text. No match was found")
    return None


def decode_chat(log_error, f, filename):
    """Parse the given zip file.

            Args:
                log_error (list): Includes list of error messages.
                f (bytes): bytes of the file name in the zip file
                filename (str): Name of a file compressed in the zip file.

            Returns:
                DataFrames: A dataFrame which includes the content of the given chat file.
    """
    try:
        data = f.decode("utf-8")
    except:
        log_error(f"Could not decode to utf-8: {filename}")
    else:
        return parse_chat(log_error, data)


def parse_zipfile(log_error, zfile):
    """Parse the given zip file.

        Args:
            log_error (list): Includes list of error messages.
            zfile (ZipFile object): Regular expression

        Returns:
            list: A list of DataFrames which include the content of chat files.
    """
    results = []
    for name in zfile.namelist():
        if HIDDEN_FILE_RE.match(name):
            continue
        if not FILE_RE.match(name):
            continue
        chats = decode_chat(log_error,zfile.read(name),name)
        results.append(chats)
    if len(results)==0:
        log_error("No valid chat file is available")
    return results

# *** test related function ***


def input_df(data_path):
    """Create inputs df_chats and df_participants, used for test purposes

            Args:
                data_path (str): File path of zip file

            Returns:
                DataFrames: df_chats and df_participants
    """

    errors = []
    log_error = errors.append
    fp = os.path.join(data_path, "whatsapp_chat.zip")
    zfile = zipfile.ZipFile(fp)
    chats = parse_zipfile(log_error, zfile)
    participants = extract_participants_features(chats, anonymize=False)
    return chats[0], participants[0]

# *** analysis functions ***


def get_response_matrix(df_chat):
    """Create a response matrix for the usernames mentioned in the given dataframe.

        Args:
            df_chat (Dataframe): A dataframe including chat data

        Returns:
            DataFrame: A DataFrame with senders in the rows and receivers in the columns
    """
    users = set(df_chat[COLNAMES_DF.USERNAME])
    users = sorted(users)

    # Get list of username transitions and initialize dicitonary with counts
    user_transitions = df_chat[COLNAMES_DF.USERNAME].tolist()
    responses = {user: dict(zip(users, [0] * len(users))) for user in users}
    # Fill count dictionary
    for i in range(1, len(user_transitions)):
        sender = user_transitions[i]
        receiver = user_transitions[i - 1]
        if sender != receiver:
            responses[sender][receiver] += 1

    responses = pd.DataFrame.from_dict(responses, orient='index')
    return responses


def make_salt():
    return str.encode('WhatsAppProject@2022')


def anonym_txt(txt, salt):
    #anonymized_txt = hashlib.pbkdf2_hmac('sha256', txt.encode(), salt, 10000).hex()
    anonymized_txt = hashlib.sha256(salt + txt.encode()).hexdigest()
    return anonymized_txt


def anonym_participants(df_participants):
    """Anonymize usernames mentioned in the given dataframe.

                    Args:
                        df_participants (Dataframe): A dataframe including participants data

                    Returns:
                        DataFrame: An anonymized DataFrame
    """
    salt = make_salt()
    df_participants[COLNAMES_DF.USERNAME] = df_participants[COLNAMES_DF.USERNAME].apply(lambda u: anonym_txt(u,salt))
    df_participants[COLNAMES_DF.REPLY_2USER] = df_participants[COLNAMES_DF.REPLY_2USER].apply(lambda u: anonym_txt(u,salt))
    df_participants[COLNAMES_DF.USER_REPLY2] = df_participants[COLNAMES_DF.USER_REPLY2].apply(lambda u: anonym_txt(u,salt))
    return df_participants


def get_participants_features(df_chat):
    """Calculate participant features from the given chat.

                Args:
                    df_chat (Dataframe): A dataframe including chat data

                Returns:
                    DataFrame: A DataFrame which includes participants and their features
    """
    # Calculate the number of words in messages
    df_chat[COLNAMES_DF.WORDS_NO] = df_chat['message'].apply(lambda x: len(x.split()))
    # number of ulrs
    df_chat[COLNAMES_DF.URL_NO] = df_chat["message"].apply(lambda x: len(re.findall(URL_PATTERN, x))).astype(int)
    # number of locations
    df_chat[COLNAMES_DF.LOCATION_NO] = df_chat["message"].apply(
        lambda x: len(re.findall(LOCATION_PATTERN, x))).astype(int)
    # number of files
    df_chat[COLNAMES_DF.FILE_NO] = df_chat["message"].apply(lambda x: len(re.findall(ATTACH_FILE_PATTERN, x))).astype(
        int)
    # number of messages
    df_chat[COLNAMES_DF.MESSAGE_NO] = 1

    df_participants = df_chat.groupby(COLNAMES_DF.USERNAME).agg({
        COLNAMES_DF.WORDS_NO: 'sum',
        COLNAMES_DF.URL_NO: 'sum',
        COLNAMES_DF.LOCATION_NO: 'sum',
        COLNAMES_DF.FILE_NO: 'sum',
        COLNAMES_DF.MESSAGE_NO: 'sum'
    }).reset_index()

    response_matrix = get_response_matrix(df_chat)
    out_degree = response_matrix.sum(axis=1)
    in_degree = response_matrix.T.sum(axis=1)
    user_reply2 = response_matrix.idxmax(axis=1)
    reply2_user = response_matrix.T.idxmax(axis=1)

    response_matrix[COLNAMES_DF.OUT_DEGREE] = out_degree
    response_matrix[COLNAMES_DF.IN_DEGREE] = in_degree
    response_matrix[COLNAMES_DF.USER_REPLY2] = user_reply2
    response_matrix[COLNAMES_DF.REPLY_2USER] = reply2_user
    response_matrix.index.name = COLNAMES_DF.USERNAME
    response_matrix = response_matrix.loc[:,
                      [COLNAMES_DF.OUT_DEGREE, COLNAMES_DF.IN_DEGREE, COLNAMES_DF.USER_REPLY2, COLNAMES_DF.REPLY_2USER]]
    response_matrix = response_matrix.reset_index()

    df_participants = pd.merge(df_participants, response_matrix, how="left", on=COLNAMES_DF.USERNAME, validate="1:1")

    return df_participants


def extract_participants_features(chats, anonymize=True):
    """Parse the given zip file.

            Args:
                chats (list): List of dataframes including chat data
                anonymize (bool): Indicates if usernames should be anonymized

            Returns:
                list: A list of DataFrames which include participant features
    """
    results = []
    for chat in chats:
        df = get_participants_features(chat)
        if anonymize:
            df = anonym_participants(df)
        results.append(df)
    return results

# ***** end of analysis functions *****


def format_results(df_list):
    results = []
    for df in df_list:
        results.append(
            {
            "id": "overview",
            "title": "The following data is extracted from the file:",
            "data_frame": df
            }
        )
    return results


def format_errors(errors):
    data_frame = pd.DataFrame()
    data_frame["Messages"] = pd.Series(errors, name="Messages")
    return {"id": "extraction_log", "title": "Extraction log", "data_frame": data_frame}


def process(file_data):
    errors = []
    log_error = errors.append
    zfile = None
    try:
        zfile = zipfile.ZipFile(file_data)
    except:
        log_error("No zip file is provided")
        return [format_errors(errors)]

    chats = parse_zipfile(log_error, zfile)
    if errors:
        return [format_errors(errors)]
    participants = extract_participants_features(chats)
    formatted_results = format_results(participants)


    return formatted_results

