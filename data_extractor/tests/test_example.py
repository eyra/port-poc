from example import process
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

DATA_PATH = Path(__file__).parent / "data"

EXPECTED = [
    {'username': 'emielvdveen', 'description': '-'},
    {'username': 'a.m.mendrik', 'description': '-'},
    {'username': '9bitcat', 'description': 'you'}
]

SELECTED_USERNAME = '9bitcat'


def test_example_flow():
    flow = process()

    # start flow and handle first prompt
    file_prompt = flow.send(None)
    assert file_prompt["cmd"] == 'prompt'
    assert file_prompt["prompt"]["type"] == 'file'

    # simulate filename selection
    selected_filename = DATA_PATH.joinpath("helloworld.txt")
    radio_prompt = flow.send(selected_filename)
    assert radio_prompt["cmd"] == 'prompt'
    assert radio_prompt["prompt"]["type"] == 'radio'

    # simulate username selection
    result = flow.send(SELECTED_USERNAME)
    assert result["cmd"] == 'result'
    assert result["result"][0]["id"] == 'overview'
    assert result["result"][0]["title"] == 'The following usernames where extracted:'

    data_frame = result["result"][0]["data_frame"]

    print(data_frame)

    data_frame_expected = pd.DataFrame(EXPECTED)
    assert_frame_equal(data_frame, data_frame_expected)
