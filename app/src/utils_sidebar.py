"""Functions for the sidebar of the Streamlit app."""
import base64
from datetime import date

import streamlit as st
from src.config_parameters import config

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

    # About textbox
    st.sidebar.markdown("## About")
    st.sidebar.markdown(
        """
        <div class='warning' style='
            background-color: %s;
            margin: 0px;
            padding: 1em;'
        '>
            <p style='
                margin-left:1em;
                margin: 0px;
                font-size: 1rem;
                margin-bottom: 1em;
            '>
                    Last update: %s
            </p>
            <p style='
                margin-left:1em;
                font-size: 1rem;
                margin: 0px
            '>
                <a href='%s'>
                Wiki reference page</a><br>
                <a href='%s'>
                GitHub repository</a><br>
                <a href='%s'>
                Data Science Lab</a>
            </p>
        </div>
        """
        % (
            config["about_box_background_color"],
            today,
            config["url_project_wiki"],
            config["url_github_repo"],
            config["url_data_science_wiki"],
        ),
        unsafe_allow_html=True,
    )

    # Contacts textbox
    st.sidebar.markdown(" ")
    st.sidebar.markdown("## Contacts")

    # Add data scientists and emails
    contacts_text = ""
    for ds, email in config["data_scientists"].items():
        contacts_text += ds + (
            "<span style='float:right; margin-right: 3px;'>"
            "<a href='mailto:%s'>%s</a></span><br>" % (email, email)
        )

    # Add text box
    st.sidebar.markdown(
        """
        <div class='warning' style='
            background-color: %s;
            margin: 0px;
            padding: 1em;'
        '>
            <p style='
                margin-left:1em;
                font-size: 1rem;
                margin: 0px
            '>
                %s
            </p>
        </div>
        """
        % (config["about_box_background_color"], contacts_text),
        unsafe_allow_html=True,
    )
