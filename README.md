# Deprecated 
![No Maintenance Intended](https://img.shields.io/maintenance/no/2022.svg)

This repository was used as a proof-of-concept for data donation and described in the following paper:

Boeschoten, L., Mendrik, A., van der Veen, E., Vloothuis, J., Hu, H., Voorvaart, R., & Oberski, D. L. (2022). [Privacy-preserving local analysis of digital trace data: A proof-of-concept](https://www.sciencedirect.com/science/article/pii/S2666389922000174). Patterns, 3(3).

For the latest version of the data donation software visit the [feldspar repository](https://github.com/eyra/feldspar), which is used as part of the Port program for data donation. 

---

# Eyra Port POC

## Description
This proof-of-concept shows how Python can be used, from within a web-browser,
to extract data for research purposes. The end-user (data donator) needs only
to have a modern web-browser.

An application is provided which creates a basic user-interface for selecting a
file. This file is then submitted to a Python interpreter. The relevant file
API's of the web-browser have been wrapped so that the Python code does not
need to be aware of running in a web-browser.

Example code for the Python part of the project is provided in the
[data_extractor](data_extractor/) folder. This also contains a [README](data_extractor/README.md) 
which explains how to modify this code and presents two examples of data extraction scripts,
namely for Google Semantic Location History and Google Search History data.

To run the application execute the following command from the checkout:

	python3 -m http.server

This launches a web-server that can be accessed on 
[http://localhost:8000](http://localhost:8000).


## Contributors
Port POC is developed by [Eyra](https://github.com/eyra). The example data extraction scripts for 
Google Semantic Location History and Google Search History data packages are developed by the 
[Research Engineering team](https://github.com/orgs/UtrechtUniversity/teams/research-engineering) of Utrecht University.
