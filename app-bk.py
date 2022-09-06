import streamlit as st
from multiapp import MultiApp
from apps import (
    timelapse,
    gee_datasets,
)

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Create Timelapse", timelapse.app)
apps.add_app("Awesome GEE Community Datasets", gee_datasets.app)

# The main app
apps.run()
