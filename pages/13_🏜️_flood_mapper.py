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

st.set_page_config(layout="wide")

# st.sidebar.title("About")
# st.sidebar.info(
#     """
#     Web App URL: 
#     GitHub repository: 
#     """
# )

# st.sidebar.title("Contact")
# st.sidebar.info(
#     """
#     Mapaction Flood Mapper App
#     """
# )


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
    st.title("Flood mapper application")
    data = st.file_uploader(
                "Upload a GeoJSON file to use as an ROI. Customize timelapse parameters and then click the Submit button 😇👇",
                type=["geojson", "kml", "zip"],
            )
    if data is not None:
        gj = geojson.load(data)
        coords = gj['features'][0]['geometry']['coordinates']
    # row1_col1, row1_col2 = st.columns([2, 1])
    # with row1_col1:
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
    if data: 
        gdf = uploaded_file_to_gdf(data)
        try:
            st.session_state["roi"] = geemap.gdf_to_ee(gdf, geodesic=False)
            Map.add_gdf(gdf, "ROI")
        except Exception as e:
            st.error(e)
            st.error("Please draw another ROI and try again.")
            return
    Map.to_streamlit()

    with st.sidebar:
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
# export_option = st.selectbox("Export to Google Drive (Yes/No)", datasets.keys(), index=0)
    with st.form(key="my_form2"):
        empty_text = st.empty()
        submitted = st.form_submit_button('Compute flood extent')
        if submitted:
            if data is None:
                empty_text.text("No data, please select a region..")
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
                st.title("Flood Map Output")
                Map = geemap.Map(
                    basemap="HYBRID",
                    plugin_Draw=True,
                    Draw_export=True,
                    locate_control=True,
                    plugin_LatLngPopup=False,
                    )
                Map.add_layer(detected_flood_vector, {}, "Flood extent vector")
                Map.add_layer(detected_flood_raster, {}, "Flood extent raster")
                Map.centerObject(detected_flood_vector)
                Map.to_streamlit()
                    # with open(file_path, 'rb') as my_file:
# st.button(label = 'Download', data = my_file, file_name = 'filename.xlsx')       
app()

