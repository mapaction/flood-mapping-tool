"""Functions for the layout of the Streamlit app, including the sidebar."""
import base64
import os
from datetime import date

import streamlit as st
from src.config_parameters import params


# Check if app is deployed
def is_app_on_streamlit():
    """Check whether the app is on streamlit or runs locally."""
    return "HOSTNAME" in os.environ and os.environ["HOSTNAME"] == "streamlit"


# General layout
def toggle_menu_button():
    """If app is on streamlit, hide menu button."""
    if is_app_on_streamlit():
        st.markdown(
            """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """,
            unsafe_allow_html=True,
        )


# Home page
def set_home_page_style():
    """Set style home page."""
    st.markdown(
        """
    <style> p { font-size: %s; } </style>
    """
        % params["docs_fontsize"],
        unsafe_allow_html=True,
    )


# Documentation page
def set_doc_page_style():
    """Set style documentation page."""
    st.markdown(
        """
    <style> p { font-size: %s; } </style>
    """
        % params["docs_fontsize"],
        unsafe_allow_html=True,
    )


# Tool page
def set_tool_page_style():
    """Set style tool page."""
    st.markdown(
        """
            <style>
                .streamlit-expanderHeader {
                    font-size: %s;
                    color: #000053;
                }
                .stDateInput > label {
                    font-size: %s;
                }
                .stSlider > label {
                    font-size: %s;
                }
                .stRadio > label {
                    font-size: %s;
                }
                .stButton > button {
                    font-size: %s;
                    font-weight: %s;
                    background-color: %s;
                }
            </style>
        """
        % (
            params["expander_header_fontsize"],
            params["widget_header_fontsize"],
            params["widget_header_fontsize"],
            params["widget_header_fontsize"],
            params["button_text_fontsize"],
            params["button_text_fontweight"],
            params["button_background_color"],
        ),
        unsafe_allow_html=True,
    )


# Sidebar
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
                    content: "%s";
                    margin-left: 20px;
                    margin-top: 20px;
                    margin-bottom: 20px;
                    font-size: %s;
                    font-weight: %s;
                    position: relative;
                    text-align: center;
                    top: 85px;
                }
            </style>
            """ % (
        binary_string,
        params["MA_logo_background_position"],
        params["MA_logo_width"],
        "",
        params["sidebar_header"],
        params["sidebar_header_fontsize"],
        params["sidebar_header_fontweight"],
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
    # st.sidebar.title("ciao")
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
            params["about_box_background_color"],
            today,
            params["url_project_wiki"],
            params["url_github_repo"],
            params["url_data_science_wiki"],
        ),
        unsafe_allow_html=True,
    )

    # Contacts textbox
    st.sidebar.markdown(" ")
    st.sidebar.markdown("## Contacts")

    # Add data scientists and emails
    contacts_text = ""
    for ds, email in params["data_scientists"].items():
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
        % (params["about_box_background_color"], contacts_text),
        unsafe_allow_html=True,
    )
