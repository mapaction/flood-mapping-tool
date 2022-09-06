import streamlit as st
import geemap.foliumap as geemap
import pandas as pd
import os
import ee
import io
import folium
from flood_mapper import derive_flood_extents, export_flood_data

def app():
    st.title("Flood mapper application")
    row1_col1, row1_col2 = st.columns([2, 1])
    with row1_col2:
        # uploaded_file = st.file_uploader("Choose a file")
        # if uploaded_file is not None:
        #     # To read file as bytes:
        #     bytes_data = uploaded_file.getvalue()
        #     st.write(bytes_data)
        before_start = st.date_input(" start date imagery before the flooding event")
        before_end = st.date_input("end date imagery before the flooding event")
        after_start = st.date_input(" start date imagery after the flooding event")
        after_end = st.date_input("end date imagery after the flooding event")
        add_slider = st.slider(
        'Select a threshold',
        0.0, 5.0, 1.0, 0.25, help('higher value might reduce overall noise'))
            # To convert to a string based IO:
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            st.write(bytes_data)

            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            st.write(stringio)

            # To read file as string:
            string_data = stringio.read()
            st.write(string_data)

            # Can be used wherever a "file-like" object is accepted:
            dataframe = pd.read_csv(uploaded_file)
            st.write(dataframe)
        datasets = {"Yes": {
            "Yes",
        }, "No": {
            "No",
        }}
        export_option = st.selectbox("Export to Google Drive (Yes/No)", datasets.keys(), index=0)
        out_dir = st.download_button("Export to personal drive", os.path.expanduser('~'), 'Downloads')
        # with open("flower.png", "rb") as file:
        #     btn = st.download_button(label="Download image", data=file, file_name="flower.png", mime="image/png")
    with row1_col1:
        Map = geemap.Map(center=[40, -100], zoom=4)
        # region_select = Map.draw_last_feature
        # geo_dict = region_select.getInfo()
        # ee_geom_region = ee.Geometry.Polygon(geo_dict['geometry']['coordinates'])
        # detected_flood_vector, detected_flood_raster, before_imagery, after_imagery = derive_flood_extents(
        #     ee_geom_region,
        #     before_start,
        #     before_end,
        #     after_start,
        #     after_end,
        #     export=False)
        # location = ee_geom_region.centroid().coordinates().getInfo()[::-1]

        # Set visualization parameters.
        # s1_vis_params = {'min': -30, 'max': 0}
        # flood_vis_params = {'min': 0, 'max': 1, 'palette': 'blue'}
        Map.to_streamlit()

