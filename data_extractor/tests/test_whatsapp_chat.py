from whatsapp_chat import process
from whatsapp_chat import anonymize_participants
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal


DATA_PATH = Path(__file__).parent / "data"

EXPECTED = [
    {'username': 'user1', 'total_words_no': 20, 'url_no': 1, 'location_no': 1, 'file_no': 0, 'message_no': 3,
     'first_message_date': '2022-03-16 15:20:25', 'last_message_date': '2022-03-24 20:19:38', 'out_degree': 2,
     'in_degree': 3, 'user_reply2': 'user2', 'reply_2_user': 'user2'},

    {'username': 'user2', 'total_words_no': 18, 'url_no': 2, 'location_no': 0, 'file_no': 0, 'message_no': 3,
     'first_message_date': '2022-03-16 15:25:38', 'last_message_date': '2022-03-26 18:52:15', 'out_degree': 3,
     'in_degree': 3, 'user_reply2': 'user1', 'reply_2_user': 'user1'},

    {'username': 'user3', 'total_words_no': 1, 'url_no': 0, 'location_no': 0, 'file_no': 0, 'message_no': 1,
     'first_message_date': '2022-03-16 15:26:48', 'last_message_date': '2022-03-16 15:26:48', 'out_degree': 1,
     'in_degree': 1, 'user_reply2': 'user2', 'reply_2_user': 'user2'},

    {'username': 'user4', 'total_words_no': 21, 'url_no': 0, 'location_no': 0, 'file_no': 0, 'message_no': 2,
     'first_message_date': '2020-07-14 22:05:54', 'last_message_date': '2022-03-20 20:08:51', 'out_degree': 2,
     'in_degree': 1, 'user_reply2': 'user1', 'reply_2_user': 'user1'}
]


def test_process():
    """ Test process function.
        compares the expected dataframe with the output of the process function to check if all the columns are match.
        Raises
        -------
        AssertionError: When provided expected dataframe could not match the participants dataframe
        """

    df_expected = pd.DataFrame(EXPECTED)
    df_expected = anonymize_participants(df_expected)
    df_expected['message_no'] = df_expected['message_no'].astype('int64')
    df_expected['url_no'] = df_expected['url_no'].astype('int32')
    df_expected['location_no'] = df_expected['location_no'].astype('int32')
    df_expected['file_no'] = df_expected['file_no'].astype('int32')

    # result = process(DATA_PATH.joinpath("whatsapp_chat.zip"))
    result = process(DATA_PATH.joinpath("_chat.txt"))
    assert len(result) == 1
    df_result = result[0]["data_frame"]
    assert_frame_equal(df_result, df_expected)


