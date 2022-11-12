"""Documentation page for Streamlit app."""
import streamlit as st
from PIL import Image

from config_parameters import config
from sidebar_functions import add_about, add_logo

# Page configuration
st.set_page_config(layout="wide")

# Create sidebar
add_logo("img/MA-logo.png")
add_about()

# Set fontisize text
st.markdown(
    "<style>" "p { font-size: " f"{config['docs_fontsize']}" "; }" "</style>",
    unsafe_allow_html=True,
)

# Page title
st.markdown("# Documentation")

# First section
st.markdown("## Methodology")
st.markdown(
    "The methodology is based on the workflow depicted in Figure 1. In "
    "addition to Sentinel-1 "
    "synthetic-aperture radar "
    "<a href='"
    "https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar"
    "'>"
    "SAR"
    "</a> "
    "data, two other datasets are used through "
    "<a href='"
    "https://earthengine.google.com/"
    "'>"
    "Google Earth Engine"
    "</a>:"
    "<ul>"
    "<li><p>"
    "The <i>WWF HydroSHEDS Void-Filled DEM, 3 Arc-Seconds</i> "
    "<a href='"
    "https://developers.google.com/earth-engine/datasets/catalog/"
    "WWF_HydroSHEDS_03VFDEM"
    "'>"
    "dataset"
    "</a> "
    "is based on elevation data obtained in 2000 by NASA's Shuttle Radar "
    "Topography Mission (SRTM), and it is used to mask out areas with more "
    "than 5 percent slope (see following section on limitations)."
    "</p>"
    "<li><p>"
    "The <i>JRC Global Surface Water Mapping Layers, v1.4</i> "
    "<a href='"
    "https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_"
    "GlobalSurfaceWater"
    "'>"
    "dataset"
    "</a> "
    "contains maps of "
    "the location and temporal distribution of surface water from 1984 to "
    "2021, and it is used to mask areas with perennial water bodies, such as "
    "rivers or lakes."
    "</p>"
    "</ul>",
    unsafe_allow_html=True,
)

# Add image workflow
img = Image.open("img/workflow.png")
st.image(
    img,
    width=350,
    caption=(
        "Figure 1. Workflow of the flood mapping methodology. Source: "
        "https://un-spider.org/advisory-support/recommended-practices/"
        "recommended-practice-google-earth-engine-flood-mapping/in-detail."
    ),
)

# Second section
st.markdown("## Radar imagery for flood detection")
st.markdown(
    "While there are multiple change detections techniques for radar imagery, "
    "the one used by Sentinel-1 is one of the simplest. Active radar "
    "satellites produce active radiation directed at the land, and images are "
    "formed as a function of the time it takes for that radiation to reach "
    "back to the satellite. Because of this, radar systems are side-looking "
    "(otherwise radiation from multiple areas would reach back at the same "
    "time).  To be detected and imaged, radiation needs to be scattered back, "
    "but not all surfaces are equally able to scatter back, and that ability "
    "is also influenced by the radiation's wavelength (shorter wavelengths "
    "are "
    "better at detecting smaller objects, while longer wavelengths allow "
    "penetration, which is good for forest canopies for example, and biomass "
    "studies). Sentinel-1 satellites are C-band (~ 6 cm).<br><br>"
    "Water is characterised by a mirror-like reflection mechanism, meaning "
    "that no or very little radiation is scattered back to the satellite, "
    "so pixels on the image will appear very dark. This very simple change "
    'detection takes a "before" image, and looks for drops in intensity, dark '
    'spots, in the "after" image.<br><br>'
    "Sentinel-1 data is the result of measurements from a constellation of "
    "two "
    "satellites, assing over "
    "the same areas following the same orbit on average every 6 days. On "
    "Google Earth Engine, the processing level is Ground Range Detected "
    "(GRD), "
    "meaning that it has been detected, multi-looked and projected to ground "
    "range using an Earth ellipsoid model. GRD products report on intensity "
    "of "
    "radiation, but have lost the phase and amplitude information which is "
    "needed for other applications (interferometry for example). These "
    "satellites emits in different polarizations, and can acquire both single "
    "horizonal or vertical, or dual polarizations. Flood water is best "
    "detected by using VH (vertical transmit and horizontal receive), "
    "although "
    "VV (vertical transmit and vertical receive) can be effective to identify "
    "partially submerged features. This tool uses VH polarization. Figure 2 "
    "shows an overview of the "
    "Sentinel-1 observation plan, where pass directions and coverage "
    "frequencies are highlighted.",
    unsafe_allow_html=True,
)

# Add image satellite overview
st.image(
    "https://sentinel.esa.int/documents/247904/4748961/Sentinel-1-Repeat-"
    "Coverage-Frequency-Geometry-2021.jpg",
    width=1000,
    caption=(
        "Figure 2. Overview of the Sentinel-1 observation plan. Source: "
        "https://sentinel.esa.int/web/sentinel/missions/sentinel-1/"
        "observation-scenario"
    ),
)

# Third section
st.markdown("## Key limtations")
st.markdown(
    "Radar imagery is great for detecting floods, as it is good at picking up "
    "water and it is "
    "not affected by the time of the day or clouds (at this wavelength). But "
    "it has its limits, and performs actually quite bad if having to detect "
    "water "
    "in mountainous regions, especially if with narrow valleys, and in urban "
    "areas (urban canyons). The reasons are mainly around the viewing angles, "
    "which can cause image distortions. This method may also result in false "
    "positives for other land cover changes with smooth surfaces, such as "
    "roads and sand. Rough surface texture caused by wind or rainfall may "
    "also "
    "make it challenging for the radar imagery to identify water bodies.",
    unsafe_allow_html=True,
)

# Links for last section
url_spider = (
    "https://un-spider.org/advisory-support/recommended-practices/recommended"
    "-practice-google-earth-engine-flood-mapping/step-by-step"
)
url_radar = "https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar"
url_paper_1 = "https://onlinelibrary.wiley.com/doi/full/10.1111/jfr3.12303"
url_paper_2 = (
    "https://www.sciencedirect.com/science/article/abs/pii/S0924271620301702"
)

# Last section
st.markdown("## Useful links")
st.markdown(
    "<a href='"
    f"{url_spider}"
    "'>"
    "UN-SPIDER recommended practice"
    "</a><br>"
    "<a href='"
    f"{url_radar}"
    "'>"
    "Sentinel-1 satellite imagery user guide"
    "</a><br>"
    "Relevant scientific publications: "
    "<a href='"
    f"{url_paper_1}"
    "'>"
    "1"
    "</a>, "
    "<a href='"
    f"{url_paper_2}"
    "'>"
    "2"
    "</a><br>",
    unsafe_allow_html=True,
)
