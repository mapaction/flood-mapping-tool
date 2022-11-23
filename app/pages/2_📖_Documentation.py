"""Documentation page for Streamlit app."""
import streamlit as st
from PIL import Image
from src.config_parameters import params
from src.utils import (
    add_about,
    add_logo,
    set_doc_page_style,
    toggle_menu_button,
)

# Page configuration
st.set_page_config(layout="wide", page_title=params["browser_title"])

# If app is deployed hide menu button
toggle_menu_button()

# Create sidebar
add_logo("app/img/MA-logo.png")
add_about()

# Set page style
set_doc_page_style()

# Page title
st.markdown("# Documentation")

# First section
st.markdown("## Methodology")
st.markdown(
    """
    The methodology is based on the workflow depicted in Figure 1. In
    addition to Sentinel-1 synthetic-aperture radar <a href='%s'>SAR</a> data,
    two other datasets are used through <a href='%s'>Google Earth Engine</a>:
    <ul>
        <li><p>
            The <i>WWF HydroSHEDS Void-Filled DEM, 3 Arc-Seconds</i>
            <a href='%s'>dataset</a> is based on elevation data
            obtained in 2000 by NASA's Shuttle Radar Topography Mission (SRTM),
            and it is used to mask out areas with more than 5 percent slope
            (see following section on limitations).
        </p>
        <li><p>
            The <i>JRC Global Surface Water Mapping Layers, v1.4</i>
            <a href='%s'>dataset</a> contains maps of the
            location and temporal distribution of surface water from 1984 to
            2021, and it is used to mask areas with perennial water bodies,
            such as rivers or lakes.
        </p>
    </ul>
    """
    % (
        params["url_sentinel_dataset"],
        params["url_gee"],
        params["url_elevation_dataset"],
        params["url_surface_water_dataset"],
    ),
    unsafe_allow_html=True,
)

# Add image workflow
img = Image.open("app/img/workflow.png")
col1, mid, col2, last = st.columns([5, 3, 10, 10])
with col1:
    st.image(img, width=350)
with col2:
    # Trick to add caption at the bottom of the column, as Streamlit has not
    # developed a functionality to allign text to bottom
    space_before_caption = "<br>" * 27
    st.markdown(
        space_before_caption,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <p style="font-size:%s;">
            Figure 1. Workflow of the flood mapping methodology (<a href=
            '%s'>source</a>).
        </p>
        """
        % (
            params["docs_caption_fontsize"],
            params["url_unspider_tutorial_detail"],
        ),
        unsafe_allow_html=True,
    )


# Second section
st.markdown("## Radar imagery for flood detection")
st.markdown(
    """
    While there are multiple change detections techniques for radar imagery,
    the one used by Sentinel-1 is one of the simplest. Active radar satellites
    produce active radiation directed at the land, and images are formed as a
    function of the time it takes for that radiation to reach back to the
    satellite. Because of this, radar systems are side-looking (otherwise
    radiation from multiple areas would reach back at the same time).  To be
    detected and imaged, radiation needs to be scattered back, but not all
    surfaces are equally able to scatter back, and that ability is also
    influenced by the radiation's wavelength (shorter wavelengths are better at
    detecting smaller objects, while longer wavelengths allow penetration,
    which is good for forest canopies for example, and biomass studies).
    Sentinel-1 satellites are C-band (~ 6 cm).<br><br>
    Water is characterised by a mirror-like reflection mechanism, meaning that
    no or very little radiation is scattered back to the satellite, so pixels
    on the image will appear very dark. This very simple change detection takes
    a "before" image, and looks for drops in intensity, dark spots, in the
    "after" image.<br><br>
    Sentinel-1 data is the result of measurements from a constellation of two
    satellites, assing over the same areas following the same orbit on average
    every 6 days. On Google Earth Engine, the processing level is Ground Range
    Detected (GRD), meaning that it has been detected, multi-looked and
    projected to ground range using an Earth ellipsoid model. GRD products
    report on intensity of radiation, but have lost the phase and amplitude
    information which is needed for other applications (interferometry for
    example). These satellites emits in different polarizations, and can
    acquire both single horizonal or vertical, or dual polarizations. Flood
    water is best detected by using VH (vertical transmit and horizontal
    receive), although VV (vertical transmit and vertical receive) can be
    effective to identify partially submerged features. This tool uses VH
    polarization. Figure 2 shows an overview of the Sentinel-1 observation
    plan, where pass directions and coverage frequencies are highlighted.
    """,
    unsafe_allow_html=True,
)

# Add image satellite overview
st.image(
    "%s" % params["url_sentinel_img"],
    width=1000,
)
st.markdown(
    """
        <p style="font-size:%s;">
            Figure 2. Overview of the Sentinel-1 observation plan (<a href=
            '%s'>source</a>).
        </p>
        """
    % (params["docs_caption_fontsize"], params["url_sentinel_img_location"]),
    unsafe_allow_html=True,
)

# Third section
st.markdown("## Key limitations")
st.markdown(
    """
    Radar imagery is great for detecting floods, as it is good at picking up
    water and it is not affected by the time of the day or clouds (at this
    wavelength). But it has its limits, and performs actually quite bad if
    having to detect water in mountainous regions, especially if with narrow
    valleys, and in urban areas (urban canyons). The reasons are mainly around
    the viewing angles, which can cause image distortions. This method may also
    result in false positives for other land cover changes with smooth
    surfaces, such as roads and sand. Rough surface texture caused by wind or
    rainfall may also make it challenging for the radar imagery to identify
    water bodies.
    """,
    unsafe_allow_html=True,
)


# Last section
st.markdown("## Useful links")
st.markdown(
    """
    <a href='%s'>UN-SPIDER recommended practice</a><br>
    <a href='%s'>Sentinel-1 satellite imagery user guide</a><br>
    Relevant scientific publications:
    <a href='%s'>1</a>, <a href='%s'>2</a><br>
    """
    % (
        params["url_unspider_tutorial"],
        params["url_sentinel_esa"],
        params["url_publication_1"],
        params["url_publication_2"],
    ),
    unsafe_allow_html=True,
)
