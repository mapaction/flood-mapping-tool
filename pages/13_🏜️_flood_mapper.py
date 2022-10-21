from enum import auto
from tkinter import CENTER
import streamlit as st
import streamlit_ext as ste
import geemap.foliumap as geemap
import pandas as pd
import geopandas as gpd
import ee
import requests
import folium
from flood_mapper import derive_flood_extents, export_flood_data
from io import StringIO
import geojson
from folium.plugins import Draw
from folium.plugins import Search
from folium import plugins
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
    tab1, tab2 = st.tabs(["Map views", " "])
    with tab1:
        with st.expander("Input map", expanded=True):
            Map = folium.Map(
                location=[52.205276, 0.119167], 
                zoom_start=3
                )
            Draw(export=True).add_to(Map)
            output = st_folium(Map, width = 1000, height=600)
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
    with st.sidebar:
        with st.expander("Choose Image Dates"):
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
        with st.expander("Choose Parameters"):        
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
                # st.write(str(before_start))
                # st.write(str(before_end))
                # st.write(str(after_start))
                # st.write(str(after_end))
                # st.write(str(add_slider))
                coords = output['all_drawings'][-1]['geometry']['coordinates'][0]
                # st.write(coords)
                ee_geom_region = ee.Geometry.Polygon(coords)
                detected_flood_vector, detected_flood_raster, before_imagery, after_imagery = derive_flood_extents(
                    ee_geom_region,
                    str(before_start),
                    str(before_end),
                    str(after_start),
                    str(after_end),
                    difference_threshold=1,
                    export=False)
                empty_text.text("Done")                  
                with tab1:
                    st.session_state['is_expanded'] = False  
                    with st.expander("Output map", expanded=True):   
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
                        # info = ee.FeatureCollection.getInfo(detected_flood_vector)
                        # st.write(info)
                        url_r = detected_flood_raster.getDownloadUrl({
                            # 'bands': ['0'],
                            'region': ee_geom_region,
                            'scale': 20,
                            'format': 'GEO_TIFF'
                        })
                        response_r = requests.get(url_r)
                        url_v = detected_flood_vector.getDownloadUrl('GEOJSON')
                        response_v = requests.get(url_v)
                    with st.sidebar:
                        with open("flood_extent.tif", "wb") as file:
                            btn = ste.download_button(
                                    label="Download Raster Extent",
                                    data=response_r.content,
                                    file_name="flood_extent_raster.tif",
                                    mime="image/tif"
                                )
                        with open("flood_extent.geojson", "wb") as file:
                            btn = ste.download_button(
                                    label="Download Vector Extent",
                                    data=response_v.content,
                                    file_name="flood_extent_vector.geojson",
                                    mime="text/json"
                                )
app()

