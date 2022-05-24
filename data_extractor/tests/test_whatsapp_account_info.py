import pandas as pd
from pandas.testing import assert_frame_equal

from whatsapp_account_info import process
from pathlib import Path


DATA_PATH = Path(__file__).parent / "data"
EXPECTED = [
    {'number_of_groups': 4,
     'number_of_contacts': 3
     }
]


def test_process():
    """ Test process function.
        compares the expected dataframe with the output of the process function to check if all the columns are matched.
        Raises
        -------
        AssertionError: When provided expected dataframe could not match the participants dataframe
        """
    df_expected = pd.DataFrame(EXPECTED)

    result = process(DATA_PATH.joinpath("account_info.zip").open("rb"))
    df_result = result[0]["data_frame"]
    assert_frame_equal(df_result, df_expected)


if __name__ == '__main__':
    test_process()