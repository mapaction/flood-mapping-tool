"""Flood extent analysis page for Streamlit app."""
import datetime as dt

import ee
import folium
import geemap.foliumap as geemap
import requests
import streamlit as st
import streamlit_ext as ste
from folium.plugins import Draw, Geocoder, MiniMap
from streamlit_folium import st_folium

from flood_functions import derive_flood_extents
from sidebar_functions import add_about, add_logo

# Page configuration
st.set_page_config(layout="wide")

# Create sidebar
add_logo("img/MA-logo.png")
add_about()

# Page title
st.markdown("# Flood extent analysis")

# Set styles for text fontsize and buttons
st.markdown(
    """
<style>
.streamlit-expanderHeader {
    font-size: 23px;
    color: #000053;
}
.stDateInput > label {
    font-size:18px;
}
.stSlider > label {
    font-size:18px;
}
.stRadio > label {
    font-size:18px;
}
.stButton > button {
    font-size:24px;
    font-weight:bold;
    background-color:#dae7f4;
}
</style>
""",
    unsafe_allow_html=True,
)


# Initialise Google Earth Engine
@st.cache
def _initialize_ee():
    ee.Initialize()


_initialize_ee()


# Create app
def app():
    """Create Streamlit app."""
    # Output_created is useful to decide whether the bottom panel with the
    # output map should be visualised or not
    if "output_created" not in st.session_state:
        st.session_state.output_created = False

    # Function to be used to hide bottom panel (when setting parameters for a
    # new analysis)
    def callback():
        st.session_state.output_created = False

    # Create two rows: top and bottom panel
    row1 = st.container()
    row2 = st.container()
    # Crate two columns in the top panel: input map and paramters
    col1, col2 = row1.columns([2, 1])
    with col1:
        # Add collapsable container for input map
        with st.expander("Input map", expanded=True):
            # Create folium map
            Map = folium.Map(
                location=[52.205276, 0.119167],
                zoom_start=3,
                control_scale=True,
                # crs='EPSG4326'
            )
            # Add drawing tools to map
            Draw(
                export=False,
                draw_options={
                    "circle": False,
                    "polyline": False,
                    "polygon": False,
                    "circle": False,
                    "marker": False,
                    "circlemarker": False,
                },
            ).add_to(Map)
            # Add search bar with geocoder to map
            Geocoder(add_marker=False).add_to(Map)
            # Add minimap to map
            MiniMap().add_to(Map)
            # Add file uploader for GeoJSON to add polygons to map
            # data = st.file_uploader(
            #     "Upload a GeoJSON file to use as an ROI.",
            #     type=["geojson", "kml", "zip"],
            # )
            # ss = st.empty()
            # with ss:
            # Export map to Streamlit
            output = st_folium(Map, width=800, height=600)
            # if data is not None:
            #     with ss:
            #         # gj = geojson.load(data)
            #         # coords = gj['features'][0]['geometry']['coordinates']
            #         st.write('Still to be implemented')
    with col2:
        # Add collapsable container for image dates
        with st.expander("Choose Image Dates"):
            # Callback is added, so that, every time a parameters is changed,
            # the bottom panel containing the output map is hidden
            before_start = st.date_input(
                "Start date for reference imagery",
                value=dt.date(year=2022, month=7, day=1),
                help="It needs to be prior to the flooding event",
                on_change=callback,
            )
            before_end = st.date_input(
                "End date for reference imagery",
                value=dt.date(year=2022, month=7, day=30),
                help=(
                    "It needs to be prior to the flooding event, at least 15 "
                    "days subsequent to the date selected above"
                ),
                on_change=callback,
            )
            after_start = st.date_input(
                "Start date for flooding imagery",
                value=dt.date(year=2022, month=9, day=1),
                help="It needs to be subsequent to the flooding event",
                on_change=callback,
            )
            after_end = st.date_input(
                "End date for flooding imagery",
                value=dt.date(year=2022, month=9, day=16),
                help=(
                    "It needs to be subsequent to the flooding event and at "
                    "least 10 days to the date selected above"
                ),
                on_change=callback,
            )
        # Add collapsable container for parameters
        with st.expander("Choose Parameters"):
            # Add slider for threshold
            add_slider = st.slider(
                label="Select a threshold",
                min_value=0.0,
                max_value=5.0,
                value=1.25,
                step=0.25,
                help="Higher values might reduce overall noise",
                on_change=callback,
            )
            # Add radio buttons for pass direction
            pass_direction = st.radio(
                "Set pass direction",
                ["Ascending", "Descending"],
                on_change=callback,
            )
        # Button for computation
        submitted = st.button("Compute flood extent")
        # Introduce date validation
        check_dates = before_start < before_end <= after_start < after_end
        # Introduce drawing validation (a polygon needs to exist)
        check_drawing = (
            output["all_drawings"] != [] and output["all_drawings"] is not None
        )
    # What happens when button is clicked on?
    if submitted:
        with col2:
            # Output error if dates are not valid
            if not check_dates:
                st.error("Make sure that the dates were inserted correctly")
            # Output error if no polygons were drawn
            elif not check_drawing:
                st.error("No region selected")
            else:
                # Add output for computation
                with st.spinner("Computing... Please wait..."):
                    # Extract coordinates from drawn polygon
                    coords = output["all_drawings"][-1]["geometry"][
                        "coordinates"
                    ][0]
                    # Create geometry from coordinates
                    ee_geom_region = ee.Geometry.Polygon(coords)
                    # Crate flood raster and vector
                    (
                        detected_flood_vector,
                        detected_flood_raster,
                        _,
                        _,
                    ) = derive_flood_extents(
                        aoi=ee_geom_region,
                        before_start_date=str(before_start),
                        before_end_date=str(before_end),
                        after_start_date=str(after_start),
                        after_end_date=str(after_end),
                        difference_threshold=add_slider,
                        polarization="VH",
                        pass_direction=pass_direction,
                        export=False,
                    )
                    # Create output map
                    Map2 = geemap.Map(
                        # basemap="HYBRID",
                        plugin_Draw=False,
                        Draw_export=False,
                        locate_control=False,
                        plugin_LatLngPopup=False,
                    )
                    try:
                        # Add flood vector layer to map
                        Map2.add_layer(
                            ee_object=detected_flood_vector,
                            name="Flood extent vector",
                        )
                        # Center map on flood raster
                        Map2.centerObject(detected_flood_raster)
                    except Exception as e:
                        # If error contains the sentence below, it means that
                        # an image could not be properly generated
                        if (
                            "If one image has no bands, the other must also \
                            have no bands"
                            in str(e)
                        ):
                            st.error(
                                "No satellite image found for the selected "
                                "dates.\n\n"
                                "Try changing the pass direction or the "
                                "polarization.\n\n"
                                "If this does not work, choose different "
                                "dates: "
                                "it is likely that the satellite did not "
                                "cover "
                                "the area of interest in the range of dates "
                                "specified (either before or after the "
                                "flooding event)."
                            )
                        else:
                            raise
                    else:
                        # If computation was succesfull, save outputs for
                        # output map
                        st.success("Computation complete")
                        st.session_state.output_created = True
                        st.session_state.Map2 = Map2
                        st.session_state.detected_flood_raster = (
                            detected_flood_raster
                        )
                        st.session_state.detected_flood_vector = (
                            detected_flood_vector
                        )
                        st.session_state.ee_geom_region = ee_geom_region
    # If computation was successful, create output map in bottom panel
    if st.session_state.output_created:
        with row2:
            # Add collapsable container for output map
            with st.expander("Output map", expanded=True):
                # Export Map2 to streamlit
                st.session_state.Map2.to_streamlit()
                # Create button to export to file
                submitted2 = st.button("Export to file")
                # What happens if button is clicked on?
                if submitted2:
                    # Add output for computation
                    with st.spinner("Computing... Please wait..."):
                        try:
                            # Get download url for raster data
                            raster = st.session_state.detected_flood_raster
                            url_r = raster.getDownloadUrl(
                                {
                                    "region": st.session_state.ee_geom_region,
                                    "scale": 30,
                                    "format": "GEO_TIFF",
                                }
                            )
                        except Exception:
                            st.error(
                                "The image size is too big for the image to "
                                "be exported to file. Select a smaller area "
                                "of interest (side <~ 150km) and repeat the "
                                "analysis."
                            )
                        else:
                            response_r = requests.get(url_r)
                            # Get download url for raster data
                            vector = st.session_state.detected_flood_vector
                            url_v = vector.getDownloadUrl("GEOJSON")
                            response_v = requests.get(url_v)
                            with row2:
                                # Create download buttons for raster and vector
                                # data
                                with open("flood_extent.tif", "wb"):
                                    ste.download_button(
                                        label="Download Raster Extent",
                                        data=response_r.content,
                                        file_name="flood_extent_raster.tif",
                                        mime="image/tif",
                                    )
                                with open("flood_extent.geojson", "wb"):
                                    ste.download_button(
                                        label="Download Vector Extent",
                                        data=response_v.content,
                                        file_name="flood_extent_vec.geojson",
                                        mime="text/json",
                                    )
                            # Output for computation complete
                            st.success("Computation complete")


# Run app
app()
