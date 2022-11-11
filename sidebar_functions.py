import base64
import streamlit as st

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
    png_file,
    background_position="35% 10%",
    image_width="60%",
    image_height=""
):
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
                    content: "Flood Mapping Tool";
                    margin-left: 20px;
                    margin-top: 20px;
                    margin-bottom: 20px;
                    padding-bottom: 50px;
                    font-size: 30px;
                    font-weight: bold;
                    position: relative;
                    top: 85px;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        image_width,
        image_height
    )


def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

def add_about():
    st.sidebar.title("About")
    st.sidebar.info(
        """
        Web App URL: <https://geospatial.streamlitapp.com>
        GitHub repository: <https://github.com/mapaction/flood-extent-tool>
        """
    )

    st.sidebar.title("Contacts")
    st.sidebar.info(
        """
        Piet: <pgerrits@mapaction.org>\n
        Daniele: <dcastellana@mapaction.org>
        """
    )