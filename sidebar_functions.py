"""Functions for the sidebar of the Streamlit app."""
import base64
from datetime import date

import streamlit as st

from config_parameters import config

sidebar_title = "Flood Mapping Tool"


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(png_file):
    """
    Get base64 from image file.

    Inputs:
        png_file (str): image filename

    Returns:
        str: encoded ASCII file
    """
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
    png_file,
    background_position=f"{config['MA_logo_background_position']}",
    image_width=f"{config['MA_logo_width']}",
    image_height="",
    sidebar_header_fontsize=config["sidebar_header_fontsize"],
    sidebar_header_fontweight=config["sidebar_header_fontweight"],
):
    """
    Create full string for navigation bar, including logo and title.

    Inputs:
        png_file (str): image filename
        background_position (str): position logo
        image_width (str): width logo
        image_height (str): height logo

    Returns
        str: full string with logo and title for sidebar
    """
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    padding-top: 50px;
                    padding-bottom: 10px;
                    background-position: %s;
                    background-size: %s %s;
                }
                [data-testid="stSidebarNav"]::before {
                    content: %s;
                    margin-left: 20px;
                    margin-top: 20px;
                    margin-bottom: 20px;
                    padding-bottom: 50px;
                    font-size: %s;
                    font-weight: %s;
                    position: relative;
                    top: 85px;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        image_width,
        image_height,
        sidebar_title,
        sidebar_header_fontsize,
        sidebar_header_fontweight,
    )


def add_logo(png_file):
    """
    Add logo to sidebar.

    Inputs:
        png_file (str): image filename
    Returns:
        None
    """
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )


def add_about():
    """
    Add about and contacts to sidebar.

    Inputs:
        None
    Returns:
        None
    """
    today = date.today().strftime("%B %d, %Y")

    st.sidebar.markdown("## About")
    st.sidebar.markdown(
        "<div class='warning' "
        "style='background-color:"
        f"{config['about_box_background_color']}"
        "; "
        "margin: 0px; "
        "padding: 1em;'>"
        "<p style='margin-left:1em; "
        "margin: 0px; "
        "font-size: 1rem; "
        "margin-bottom: 1em;'>"
        "Last update: "
        f"{today}"
        "</p>"
        "<p "
        "style='margin-left:1em; "
        "font-size: 1rem; "
        "margin: 0px'>"
        "<a href='"
        "https://mapaction.atlassian.net/wiki/spaces/GAFO/pages/15920922751/"
        "Rapid+flood+mapping+from+satellite+imagery"
        "'>"
        "Wiki reference page"
        "</a><br>"
        "<a href='"
        "https://github.com/mapaction/flood-extent-tool"
        "'>"
        "GitHub repository"
        "</a><br>"
        "<a href='"
        "https://mapaction.atlassian.net/wiki/spaces/GAFO/overview"
        "'>"
        "Data Science Lab"
        "</a>"
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(" ")
    st.sidebar.markdown("## Contacts")
    st.sidebar.markdown(
        "<div class='warning' "
        "style='background-color:#dae7f4; "
        "margin: 0px; "
        "padding: 1em;'>"
        "<p "
        "style='margin-left:1em; "
        "font-size: 1rem; "
        "margin: 0px'>"
        "Piet:"
        "<span "
        "style='float:right; "
        "margin-right: 2%;'>"
        "<a href='mailto:pgerrits@mapaction.org'>pgerrits@mapaction.org</a>"
        "</span>"
        "<br>"
        "Daniele: "
        "<span "
        "style='float:right; "
        "margin-right: 2%;'>"
        "<a href='mailto:dcastellana@mapaction.org'>"
        "dcastellana@mapaction.org</a>"
        "</span>"
        "<br>"
        "Cate: "
        "<span "
        "style='float:right; "
        "margin-right: 2%;'>"
        "<a href='mailto:cseale@mapaction.org'>cseale@mapaction.org</a>"
        "</span>"
        "<br>"
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )
