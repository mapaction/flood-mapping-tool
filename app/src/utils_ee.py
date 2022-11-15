"""Module for ee-related functionalities."""
import ee
import streamlit as st


@st.cache
def ee_initialize():
    """Initialise Google Earth Engine."""
    ee.Initialize()
