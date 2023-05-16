"""Module for ee-related functionalities."""
import ee
import streamlit as st
from ee import oauth
from google.oauth2 import service_account
from src.utils import is_app_on_streamlit


@st.experimental_memo
def ee_initialize(force_use_service_account: bool = False):
    """Initialise Google Earth Engine.

    Checks whether the app is deployed on Streamlit Cloud and, based on the
    result, initialises Google Earth Engine in different ways: if the app is
    run locally, the credentials are retrieved from the user's credentials
    stored in the local system (personal Google account is used). If the app
    is deployed on Streamlit Cloud, credentials are taken from the secrets
    field in the cloud (a dedicated service account is used).
    Inputs:
        force_use_service_account (bool): If True, the dedicated Google
            service account is used, regardless of whether the app is run
            locally or in the cloud. To be able to use a service account
            locally, a file called "secrets.toml" should be added to the
            folder ".streamlit", in the main project folder.

    Returns:
        None
    """
    if force_use_service_account or is_app_on_streamlit():
        service_account_keys = st.secrets["ee_keys"]
        credentials = service_account.Credentials.from_service_account_info(
            service_account_keys, scopes=oauth.SCOPES
        )
        ee.Initialize(credentials)
    else:
        ee.Initialize()
