# Data Extractor

This is a basic template which can be used to write a data extractor.
The extraction logic should be placed in the `process` function within
`data_extractor/__init__.py`. An example has been provided.

The argument that the `process` function receives is a file-like object.
It can therefore be used with most regular Python libraries. The example
demonstrates this by usage of the `zipfile` module.

This project makes use of [Poetry](https://python-poetry.org/). It makes
creating the required Python Wheel a straight-forward process. Install
Poetry with the following command: `pip install poetry`. 
Then easily install the required python packages with `poetry install`.

The behavior of the `process` function can be verified by running the
tests. The test are located in the `tests` folder. To run the tests
execute: `poetry run pytest`.

To run the extraction code from the browser run:
`python3 -m http.server` from the project root folder (the one with `.git`).
This will start a webserver on: [localhost](http://localhost:8000).
Opening a browser with that URL will initialize the application. After
it has been loaded a file can be selected. The output of the process
function will be displayed after a while (depending on the amount of
processing required and the speed of the machine).