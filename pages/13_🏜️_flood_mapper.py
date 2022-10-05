from enum import auto
from tkinter import CENTER
import streamlit as st
import geemap.foliumap as geemap
import pandas as pd
import geopandas as gpd
import os
import ee
import io
import folium
from flood_mapper import derive_flood_extents, export_flood_data
from io import StringIO
import geojson
from folium.plugins import Draw
from streamlit_folium import st_folium
import datetime as dt

font_css = """
<style>
button[data-baseweb="tab"] {
    color: #DAA520;
  font-size: 26px;
  font-weight: bold;
  line-height: 40px;
}
</style>
"""

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.write(font_css, unsafe_allow_html=True)

@st.cache
def initialize_ee():
    ee.Initialize()

initialize_ee()

@st.cache
def uploaded_file_to_gdf(data):
    import tempfile
    import os
    import uuid

    _, file_extension = os.path.splitext(data.name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(data.getbuffer())

    if file_path.lower().endswith(".kml"):
        gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"
        gdf = gpd.read_file(file_path, driver="KML")
    else:
        gdf = gpd.read_file(file_path)

    return gdf

def app():
    st.header("Flood Map Input")
    data = st.file_uploader(
                    "Upload a GeoJSON file to use as an ROI. 😇👇",
                    type=["geojson", "kml", "zip"],
                )
    if data is not None:
        gj = geojson.load(data)
        coords = gj['features'][0]['geometry']['coordinates']
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
            Map.location = [lat, lng]
            st.session_state["zoom_level"] = 12
    col1, col2 = st.columns([2, 1])
    with col1:
        
        Map = folium.Map(
            location=[39.949610, -75.150282], 
            zoom_start=5
            )
        Draw(export=True).add_to(Map)
        output = st_folium(Map, width = 700, height=500)

    with st.sidebar:
        before_start = st.date_input(
            "start date imagery before the flooding event",
            value=dt.date(2022, 7, 1)
            )
        before_end = st.date_input(
            "end date imagery before the flooding event",
            value=dt.date(2022, 7, 30)
            )
        after_start = st.date_input(
            " start date imagery after the flooding event",
            value=dt.date(2022, 9, 1)
            )
        after_end = st.date_input(
            "end date imagery after the flooding event",
            value=dt.date(2022, 9, 16)
            )
        add_slider = st.slider(
        'Select a threshold',
        0.0, 5.0, 1.0, 0.25, help('higher value might reduce overall noise'))
        datasets = {"Yes": {
            "Yes",
        }, "No": {
            "No",
        }}
    with st.sidebar.form(key="my_form2"):
        empty_text = st.empty()
        empty_text.text(add_slider)
        submitted = st.form_submit_button('Compute flood extent')
        check_dates = before_start<before_end<=after_start<after_end
        check_drawing = output['all_drawings'] != [] and output['all_drawings'] is not None
        if submitted:
            if not check_dates:
                empty_text.text("Make sure that the dates were inserted correctly")
                # empty_text.text("No region selected")
            elif not check_drawing:
                empty_text.text("No region selected")
            else:
                empty_text.text("Computing... Please wait...")
                st.write(str(before_start))
                st.write(str(before_end))
                st.write(str(after_start))
                st.write(str(after_end))
                st.write(str(add_slider))
                coords = output['all_drawings'][-1]['geometry']['coordinates'][0]
                st.write(coords)
                ee_geom_region = ee.Geometry.Polygon(coords)
                detected_flood_vector, detected_flood_raster, before_imagery, after_imagery = derive_flood_extents(
                    ee_geom_region,
                    str(before_start),
                    str(before_end),
                    str(after_start),
                    str(after_end),
                    difference_threshold=add_slider,
                    export=False)
                empty_text.text("Done")
                with col2:        
                    Map2 = geemap.Map(
                        basemap="HYBRID",
                        plugin_Draw=True,
                        Draw_export=True,
                        locate_control=True,
                        plugin_LatLngPopup=False,
                        )
                    Map2.add_layer(detected_flood_vector, {}, "Flood extent vector")
                    Map2.add_layer(detected_flood_raster, {}, "Flood extent raster")
                    Map2.centerObject(detected_flood_vector)
                    Map2.to_streamlit()
app()

