import sys
sys.path.insert(0, '..')

from data_extractor.whatsapp import process
from data_extractor.whatsapp import _get_df_participants
from data_extractor.whatsapp import _add_total_words_no
from data_extractor.whatsapp import _get_response_matrix
from data_extractor.whatsapp import _add_replies2user
from data_extractor.whatsapp import _add_userreplies2
from data_extractor.whatsapp import _add_pattern_no
from data_extractor.whatsapp import _add_out_degree
from data_extractor.whatsapp import _add_in_degree
from data_extractor.whatsapp import _anonymize_participants
from data_extractor.whatsapp import input_df

from pathlib import Path
import pandas as pd
from pandas.testing import assert_series_equal


DATA_PATH = Path(__file__).parent / "data"

EXPECTED = [
    {'username': 'user1', 'message_no': 3, 'total_words_no': 20, 'reply_2_user': 'user2', 'user_reply2': 'user2',
     'url_no': 1, 'location_no': 1, 'file_no': 0, 'out_degree': 2, 'in_degree': 3},
    {'username': 'user2', 'message_no': 3, 'total_words_no': 16, 'reply_2_user': 'user1', 'user_reply2': 'user3',
     'url_no': 2, 'location_no': 0, 'file_no': 0, 'out_degree': 3, 'in_degree': 3},
    {'username': 'user3', 'message_no': 1, 'total_words_no': 1, 'reply_2_user': 'user2', 'user_reply2': 'user3',
     'url_no': 0,
     'location_no': 0, 'file_no': 0, 'out_degree': 1, 'in_degree': 1},
    {'username': 'user4', 'message_no': 2, 'total_words_no': 21, 'reply_2_user': 'user1', 'user_reply2': 'user4',
     'url_no': 0,
     'location_no': 0, 'file_no': 0, 'out_degree': 2, 'in_degree': 1}
]

df_expected = pd.DataFrame(EXPECTED)
df_expected['username'] = _anonymize_participants(df_expected, 'username', str.encode('WhatsAppProject@2022'))
df_expected['reply_2_user'] = _anonymize_participants(df_expected, 'reply_2_user', str.encode('WhatsAppProject@2022'))
df_expected['user_reply2'] = _anonymize_participants(df_expected, 'user_reply2', str.encode('WhatsAppProject@2022'))

df_chat, df_participants = input_df(DATA_PATH)
response_matrix = _get_response_matrix(df_chat)


def test_process():
    result = process(DATA_PATH.joinpath("whatsapp_chat.zip").open("rb"))

    assert len(result) == 1
    assert result[0]["id"] == 'overview'
    assert result[0]["title"] == 'The following files where read:'
    # assert_frame_equal(result[0]["data_frame"], df_expected)


def test_get_df_participants():
    """
    Tests the equivalence of total number of messages sent by each user
    """
    result = _get_df_participants(df_chat)
    result['message_no'] = result['message_no'].astype('int64')

    assert_series_equal(result['message_no'], df_expected['message_no'])


def test_add_total_words_no():
    """
    Tests the equivalence of total number of words for each user. Words are distinguished based on the space
    between the words. so, for example emojis, and URLs are also counted as a word.
    """
    result = _add_total_words_no(df_chat, df_participants)
    result.rename("total_words_no", inplace=True)

    assert_series_equal(result, df_expected['total_words_no'])


# def test_add_replies2user():
#     """
#     Test which participant is first replied to by the current participants
#     """
#     result = _add_replies2user(response_matrix, df_participants)
#     result.rename("reply_2_user", inplace=True)
#
#     assert_series_equal(result, df_expected['reply_2_user'])


# def test_add_userreplies2():
#     result = _add_userreplies2(response_matrix, df_participants)
#     result.rename("user_reply2", inplace=True)
#
#     assert_series_equal(result, df_expected['user_reply2'])


def test_add_pattern_no():
    """
    Location link is counted both for link and location
    """
    url_pattern = r'(https?://\S+)'
    location_pattern = r'(Location: https?://\S+)'
    file_pattern = r'(<attached: \S+>)'
    result_url = _add_pattern_no(df_chat, df_participants, url_pattern)
    result_url.rename("url_no", inplace=True)

    result_loc = _add_pattern_no(df_chat, df_participants, location_pattern)
    result_loc.rename("location_no", inplace=True)

    result_file = _add_pattern_no(df_chat, df_participants, file_pattern)
    result_file.rename("file_no", inplace=True)

    assert_series_equal(result_url, df_expected['url_no'])
    assert_series_equal(result_loc, df_expected['location_no'])
    assert_series_equal(result_file, df_expected['file_no'])


# def test_add_out_degree():
#     """
#     Test the number of participants the current participant replies to
#     """
#     result = _add_out_degree(response_matrix, df_participants)
#     result.rename("out_degree", inplace=True)
#
#     assert_series_equal(result, df_expected['out_degree'])


# def test_add_in_degree():
#     """
#     Test the number of participants respond to the current participant
#     """
#     result = _add_in_degree(response_matrix, df_participants)
#     result.rename("in_degree", inplace=True)
#
#     assert_series_equal(result, df_expected['in_degree'])


# if __name__ == '__main__':
    # test_process()
    # test_get_df_participants()
    # test_add_total_words_no()
    # test_add_replies2user()
    # # test_add_userreplies2() # To be fixed...
    # test_add_pattern_no()
    # # test_add_out_degree() # To be fixed...
    # test_add_in_degree()
