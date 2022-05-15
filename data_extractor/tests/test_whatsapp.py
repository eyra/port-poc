# import sys
# sys.path.insert(0, '..')

from data_extractor.whatsapp import process
from data_extractor.whatsapp import _get_response_matrix
from data_extractor.whatsapp import _anonymize_participants
from data_extractor.whatsapp import input_df
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal


DATA_PATH = Path(__file__).parent / "data"

EXPECTED = [
    {'username': 'user1', 'total_words_no': 20, 'url_no': 1, 'location_no': 1, 'file_no': 0, 'message_no': 3,
     'out_degree': 2, 'in_degree': 3, 'user_reply2': 'user2', 'reply_2_user': 'user2'},

    {'username': 'user2', 'total_words_no': 18, 'url_no': 2, 'location_no': 0, 'file_no': 0, 'message_no': 3,
     'out_degree': 3, 'in_degree': 3, 'user_reply2': 'user3', 'reply_2_user': 'user1'},

    {'username': 'user3', 'total_words_no': 1, 'url_no': 0, 'location_no': 0, 'file_no': 0, 'message_no': 1,
     'out_degree': 1, 'in_degree': 1, 'user_reply2': 'user3', 'reply_2_user': 'user2'},

    {'username': 'user4', 'total_words_no': 21, 'url_no': 0, 'location_no': 0, 'file_no': 0, 'message_no': 2,
     'out_degree': 2, 'in_degree': 1, 'user_reply2': 'user4', 'reply_2_user': 'user1'}
]

df_expected = pd.DataFrame(EXPECTED)
# df_expected['username'] = _anonymize_participants(df_expected, 'username', str.encode('WhatsAppProject@2022'))
# df_expected['reply_2_user'] = _anonymize_participants(df_expected, 'reply_2_user', str.encode('WhatsAppProject@2022'))
# df_expected['user_reply2'] = _anonymize_participants(df_expected, 'user_reply2', str.encode('WhatsAppProject@2022'))
df_expected['message_no'] = df_expected['message_no'].astype('int64')
df_expected['url_no'] = df_expected['url_no'].astype('int32')
df_expected['location_no'] = df_expected['location_no'].astype('int32')
df_expected['file_no'] = df_expected['file_no'].astype('int32')

df_expected = df_expected.loc[:, df_expected.columns != 'url_no']
df_expected = df_expected.loc[:, df_expected.columns != 'location_no']
# df_expected = df_expected.loc[:, df_expected.columns != 'user_reply2']


df_chat, df_participants = input_df(DATA_PATH)
response_matrix = _get_response_matrix(df_chat)
print(response_matrix)


def test_process():
    result = process(DATA_PATH.joinpath("whatsapp_chat.zip").open("rb"))

    assert len(result) == 1
    assert result[0]["id"] == 'overview'
    assert result[0]["title"] == 'The following files where read:'
    df_result = result[0]["data_frame"]
    df_result = df_result.loc[:, df_result.columns != 'url_no']
    df_result = df_result.loc[:, df_result.columns != 'location_no']
    # df_result = df_result.loc[:, df_result.columns != 'user_reply2']

    assert_frame_equal(df_result, df_expected)
    # assert_frame_equal(result[0]["data_frame"], df_expected)


if __name__ == '__main__':
    test_process()
    # print(type(df_expected['message_no']))
    # result = process(DATA_PATH.joinpath("whatsapp_chat.zip").open("rb"))[0]["data_frame"]
    # print(type(result['message_no']))

