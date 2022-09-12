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
    tab1, tab2 = st.tabs(["1. input", "2. output"])
    with tab1:
        st.header("Flood Map Input")
        data = st.file_uploader(
                    "Upload a GeoJSON file to use as an ROI. 😇👇",
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
        with st.sidebar:
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
    with tab2:
        st.header("Flood Map Output")
        st.write("Please run \"compute flood extent\" before checking output..")
        with st.sidebar.form(key="my_form2"):
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
                    # detected_flood_vector_geojson = geemap.ee_to_geojson(detected_flood_vector)
                    # st.json(detected_flood_vector_geojson, expanded=True)
                    # st.download_button(label='Download Image',
                    #     data= open('detected_flood_vector_geojson', 'rb').read(),
                    #     file_name='imagename.png',
                    #     mime='image/png')
                    with tab2:        
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
                        # out_dir = os.path.expanduser('~/Downloads')
                        # out_shp = os.path.join(out_dir, 'countries.shp')
                        # st.download_button('download' , geemap.ee_to_shp(detected_flood_vector, filename=out_shp))
        #             out_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        #             # st.download_button('output',)
        #             st.download_button(
        #                     label="Download image",
        #                     data=geemap.ee_to_df(detected_flood_vector),
        #                     file_name="flower.png",
        #                     mime="image/png"
        #    )
app()

