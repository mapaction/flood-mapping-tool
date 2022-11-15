# Flood Mapping Tool

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mapaction-flood-map.streamlit.app/)
[![license](https://img.shields.io/github/license/OCHA-DAP/pa-aa-toolbox.svg)](https://github.com/mapaction/flood-mapping-tool/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

This repository contains a Streamlit app that allows to estimate flood extent using Sentinel-1 synthetic-aperture radar <a href='https://sentinel.esa.int/web/sentinel/user-guidessentinel-1-sar'>SAR</a> data.

The methodology is based on a <a href='https://un-spider.org/advisory-support/recommended-practices/recommended-\practice-google-earth-engine-flood-mapping'> recommended practice </a> published by the United Nations Platform for Space-based Information for Disaster Management and Emergency Response (UN-SPIDER) and it uses several satellite imagery datasets to produce the final output. The datasets are retrieved from <a href='https://earthengine.google.com/'>Google Earth Engine</a> which is a powerful web-platform for cloud-based processing of remote sensing data on large scales. More information on the methodology is given in the <i>Description</i> page in the Streamlit app.

This analysis provides a comprehensive overview of a flooding event, across different areas of interest, from settlements to countries. However, as mentioned in the UN-SPIDER website, the methodology is meant for broad information provision in a global context, and contains inherent uncertainties. Therefore, it is important that the tool is not used as the only source of information for rescue response planning.

## Usage

#### Requirements

The Python version currently used is 3.10. Please install all packages from
``requirements.txt``:

```shell
pip install -r requirements.txt
```

#### Google Earth Engine authentication

[Sign up](https://signup.earthengine.google.com/) for a Google Earth Engine account, if you don't already have one. Open a terminal window, type `python` and then paste the following code:

```python
import ee
ee.Authenticate()
```

Log in to your Google account to obtain the authorization code and paste it back into the terminal. Once you press "Enter", an authorization token will be saved to your computer under the following file path (depending on your operating system):

- Windows: `C:\\Users\\USERNAME\\.config\\earthengine\\credentials`
- Linux: `/home/USERNAME/.config/earthengine/credentials`
- MacOS: `/Users/USERNAME/.config/earthengine/credentials`

The credentials will be used when initialising Google Earth Engine in the app.

#### Run the app

Finally, open a terminal and run

```shell
streamlit run app/Home.py
```

A new browser window will open and you can start using the tool.

## Contributing

#### Pre-commit

All code is formatted according to
[black](https://github.com/psf/black) and [flake8](https://flake8.pycqa.org/en/latest) guidelines. The repo is set-up to use [pre-commit](https://github.com/pre-commit/pre-commit). Please run ``pre-commit install`` the first time you are editing. Thereafter all commits will be checked against black and flake8 guidelines.

To check if your changes pass pre-commit without committing, run:

```shell
pre-commit run --all-files
```
