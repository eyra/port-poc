from google_search_history import process
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data"


def test_gslh():
    result = process(DATA_PATH.joinpath("BrowserHistory.json").open("rb"))
    assert result["summary"] == 'The following files where read: BrowserHistory.json.'
