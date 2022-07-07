from data_extractor.whatsapp_chat import process
from data_extractor.whatsapp_chat import anonymize_participants
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal


DATA_PATH = Path(__file__).parent / "data"

EXPECTED = [
    {'username': 'person1', 'Total number of words': 20, 'Number of URLs': 1, 'Number of shared locations': 1, 'file_no': 0, 'Number of messages': 3,
     'Date first message': pd.to_datetime('2022-03-16 15:20:25'), 'Date last message': pd.to_datetime('2022-03-24 20:19:38'),
     'user_reply2': 'person2', 'reply_2_user': 'person2'},

    {'username': 'person2', 'Total number of words': 7, 'Number of URLs': 1, 'Number of shared locations': 0, 'file_no': 0, 'Number of messages': 3,
     'Date first message': pd.to_datetime('2022-03-16 15:25:38'), 'Date last message': pd.to_datetime('2022-03-26 18:52:15'),
     'user_reply2': 'person1', 'reply_2_user': 'person1'},

    {'username': 'person3', 'Total number of words': 1, 'Number of URLs': 0, 'Number of shared locations': 0, 'file_no': 0, 'Number of messages': 1,
     'Date first message': pd.to_datetime('2022-03-16 15:26:48'), 'Date last message': pd.to_datetime('2022-03-16 15:26:48'),
     'user_reply2': 'person2', 'reply_2_user': 'person2'},

    {'username': 'person4', 'Total number of words': 21, 'Number of URLs': 0, 'Number of shared locations': 0, 'file_no': 0, 'Number of messages': 2,
     'Date first message': pd.to_datetime('2020-07-14 22:05:54'), 'Date last message': pd.to_datetime('2022-03-20 20:08:51'),
     'user_reply2': 'person1', 'reply_2_user': 'person1'}
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
    df_expected['Number of messages'] = df_expected['Number of messages'].astype('int64')
    df_expected['Number of URLs'] = df_expected['Number of URLs'].astype('int32')
    df_expected['Number of shared locations'] = df_expected['Number of shared locations'].astype('int32')
    df_expected['file_no'] = df_expected['file_no'].astype('int32')

    results = []
    df_melt = pd.melt(df_expected, id_vars=["username"],
                      value_vars=["Total number of words", "Number of messages", "Date first message", "Date last message",
                                  "Number of URLs", "file_no", "Number of shared locations", "reply_2_user", "user_reply2"],
                      var_name='Description', value_name='Value')

    usernames = df_melt["username"].unique()
    for u in usernames:
        df_user = df_melt[(df_melt["username"] == u) & df_melt["Value"] != 0]
        results.append(df_user)

    expected_results = []
    for df in results:
        user_name = pd.unique(df["username"])[0]
        expected_results.append(
            {
                "id": user_name,  # "overview",
                "title": user_name,  # "The following data is extracted from the file:",
                "data_frame": df[["Description", "Value"]].reset_index(drop=True)
            }
        )

    df_result = process(DATA_PATH.joinpath("_chat.txt"))

    assert_frame_equal(df_result[0]["data_frame"], expected_results[0]["data_frame"])
    assert_frame_equal(df_result[1]["data_frame"], expected_results[1]["data_frame"])
    assert_frame_equal(df_result[2]["data_frame"], expected_results[2]["data_frame"])
    assert_frame_equal(df_result[3]["data_frame"], expected_results[3]["data_frame"])


if __name__ == "__main__":
    test_process()


