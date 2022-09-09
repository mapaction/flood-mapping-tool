import streamlit as st
import geemap.foliumap as geemap
import pandas as pd
import os
import ee
import io
import folium
from flood_mapper import derive_flood_extents, export_flood_data
from io import StringIO
import geojson

st.set_page_config(layout="wide")

st.sidebar.title("About")
st.sidebar.info(
    """
    Web App URL: <https://geospatial.streamlitapp.com>
    GitHub repository: <https://github.com/giswqs/streamlit-geospatial>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Qiusheng Wu: <https://wetlands.io>
    [GitHub](https://github.com/giswqs) | [Twitter](https://twitter.com/giswqs) | [YouTube](https://www.youtube.com/c/QiushengWu) | [LinkedIn](https://www.linkedin.com/in/qiushengwu)
    """
)


def app():
    st.title("Flood mapper application")
    data = st.file_uploader(
                "Upload a GeoJSON file to use as an ROI. Customize timelapse parameters and then click the Submit button 😇👇",
                type=["geojson", "kml", "zip"],
            )
    if data is not None:
        gj = geojson.load(data)
        coords = gj['features'][0]['geometry']['coordinates']

    with st.form(key='my_form'):
        row1_col1, row1_col2 = st.columns([2, 1])
        with row1_col1:
            crs = "epsg:4326"
            Map = geemap.Map(
                basemap="HYBRID",
                plugin_Draw=True,
                Draw_export=True,
                locate_control=True,
                plugin_LatLngPopup=False,
                )
            keyword = st.text_input("Search for a location:", "")
            if keyword:
                locations = geemap.geocode(keyword)
                if locations is not None and len(locations) > 0:
                    str_locations = [str(g)[1:-1] for g in locations]
                    location = st.selectbox("Select a location:", str_locations)
                    loc_index = str_locations.index(location)
                    selected_loc = locations[loc_index]
                    lat, lng = selected_loc.lat, selected_loc.lng
                    folium.Marker(location=[lat, lng], popup=location).add_to(Map)
                    Map.set_center(lng, lat, 12)
                    st.session_state["zoom_level"] = 12
            Map.to_streamlit()

        with row1_col2:

            before_start = st.date_input(" start date imagery before the flooding event")
            before_end = st.date_input("end date imagery before the flooding event")
            after_start = st.date_input(" start date imagery after the flooding event")
            after_end = st.date_input("end date imagery after the flooding event")
            add_slider = st.slider(
            'Select a threshold',
            0.0, 5.0, 1.0, 0.25, help('higher value might reduce overall noise'))
            datasets = {"Yes": {
                "Yes",
            }, "No": {
                "No",
            }}
            export_option = st.selectbox("Export to Google Drive (Yes/No)", datasets.keys(), index=0)
            empty_text = st.empty()
            submitted = st.form_submit_button('Compute flood extent')
            if submitted:
                if data is None:
                    empty_text.text("No data")
                    # empty_text.text("No region selected")
                else:
                    empty_text.text("Computing... Please wait...")
                    ee_geom_region = ee.Geometry.Polygon(coords)
                    detected_flood_vector, detected_flood_raster, before_imagery, after_imagery = derive_flood_extents(
                        ee_geom_region,
                        str(before_start),
                        str(before_end),
                        str(after_start),
                        str(after_end),
                        export=False)
                    empty_text.text("Done")
                    Map = geemap.Map(
                        basemap="HYBRID",
                        plugin_Draw=True,
                        Draw_export=True,
                        locate_control=True,
                        plugin_LatLngPopup=False,
                        )
                    Map.addLayer(detected_flood_vector)
                    Map.to_streamlit()
            # out_dir = st.download_button("Export to personal drive", os.path.expanduser('~'), 'Downloads')
            # with open("flower.png", "rb") as file:
            #     btn = st.download_button(label="Download image", data=file, file_name="flower.png", mime="image/png")
         
app()

