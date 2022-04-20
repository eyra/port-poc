from data_extractor.whatsapp import process
from data_extractor.whatsapp import _get_df_participants
from data_extractor.whatsapp import _add_total_words_no
from data_extractor.whatsapp import _get_response_matrix
from data_extractor.whatsapp import _add_replies2user
from data_extractor.whatsapp import _add_userreplies2
from data_extractor.whatsapp import _add_pattern_no
from data_extractor.whatsapp import _add_out_degree
from data_extractor.whatsapp import _add_in_degree


from data_extractor.whatsapp import ColnamesDf
COLNAMES_DF = ColnamesDf()


from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal


DATA_PATH = Path(__file__).parent / "data"
df_expected = pd.read_csv(DATA_PATH.joinpath("chat_expected.csv").open("rb"))
df_chat = pd.read_csv(DATA_PATH.joinpath("chat_df.csv").open("rb"))
# df = process(DATA_PATH.joinpath("whatsapp_chat.zip").open("rb"))
df_participants = pd.read_csv(DATA_PATH.joinpath("participants_df.csv").open("rb"))
print(df_participants.columns)


def test_process():
    result = process(DATA_PATH.joinpath("whatsapp_chat.zip").open("rb"))
    assert len(result) == 1
    assert result[0]["id"] == 'overview'
    assert result[0]["title"] == 'The following files where read:'
    assert_frame_equal(result[0]["data_frame"], df_expected)  # test result is False because the username column is hashed based on different salt


def test_get_df_participants():
    result = _get_df_participants(df_chat)
    assert_series_equal(result['message_no'], df_expected['message_no'])


def test_add_total_words_no():
    result = _add_total_words_no(df_chat, df_participants)
    result.rename("total_words_no", inplace=True)
    assert_series_equal(result, df_expected['total_words_no'])


def test_add_replies2user():
    response_matrix = _get_response_matrix(df_chat)
    result = _add_replies2user(response_matrix, df_participants)
    result.rename("reply_2_user", inplace=True)
    assert_series_equal(result, df_expected['reply_2_user'])


# def test_add_userreplies2():
#     response_matrix = _get_response_matrix(df_chat)
#     result = _add_userreplies2(response_matrix, df_participants)
#     result.rename("user_reply2", inplace=True)
#     assert_series_equal(result, df_expected['user_reply2'])

def test_add_pattern_no():
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


def test_add_out_degree():
    response_matrix = _get_response_matrix(df_chat)
    result = _add_out_degree(response_matrix, df_participants)
    print(result)


def test_add_in_degree():
    response_matrix = _get_response_matrix(df_chat)
    result = _add_in_degree(response_matrix, df_participants)
    result.rename("in_degree", inplace=True)
    assert_series_equal(result, df_expected['in_degree'])


if __name__ == '__main__':
    # test_process()
    test_get_df_participants()
    test_add_total_words_no()
    # test_add_replies2user()
    # test_add_userreplies2() # To be fixed...
    test_add_pattern_no()
    # test_add_out_degree() # To be fixed...
    test_add_in_degree()

# TODO: Consider Salt in the hashing function to be a fix string for reproducibility
# TODO: Keep both username and username_anonym because test_add_total_words_no() uses usernames internally
# TODO: Access for push
# TODO: unhash reply_2user in df_expected and test test__add_replies2user() again
