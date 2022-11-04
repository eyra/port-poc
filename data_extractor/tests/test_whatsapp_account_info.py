""" Test script for the whatsapp_account_info script"""

from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal

from whatsapp_account_info import process


DATA_PATH = Path(__file__).parent / "data"

EXPECTED = [
    {'Aantal groepen': 4,
     'Aantal contacten': 3
     }
]


def test_process():
    """ Test process function.
        compares the expected dataframe with the output of the process function
        to check if all the columns are matched.
        Raises
        -------
        AssertionError: When provided expected dataframe could not match the participants dataframe
        """
    df_expected = pd.DataFrame(EXPECTED)
    file_to_test = DATA_PATH.joinpath("account_info.zip")

    flow = process()

    file_prompt = flow.send(None)
    assert file_prompt["cmd"] == 'prompt'
    assert file_prompt["prompt"]["type"] == 'file'

    file_prompt = flow.send(str(file_to_test))
    assert file_prompt[0]["id"] == 'Whatsapp account info'
    assert file_prompt[0]["title"] == 'Het account informatie bestand bestaat uit:'
    assert_frame_equal(file_prompt[0]["data_frame"], df_expected)


