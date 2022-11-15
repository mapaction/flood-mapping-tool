"""Module for ee-related functionalities."""
import os

import ee
import streamlit as st
from ee import oauth
from google.oauth2 import service_account


@st.experimental_memo
def ee_initialize():
    """Initialise Google Earth Engine."""
    if "HOSTNAME" in os.environ and os.environ["HOSTNAME"] == "streamlit":
        service_account_keys = st.secrets["ee_keys"]
        credentials = service_account.Credentials.from_service_account_info(
            service_account_keys, scopes=oauth.SCOPES
        )
        ee.Initialize(credentials)
    else:
        ee.Initialize()
