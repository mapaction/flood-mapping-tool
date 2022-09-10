import streamlit as st
import geemap.foliumap as geemap
import pandas as pd
import geopandas as gpd
import os
import ee
import io
import folium
from flood_mapper import derive_flood_extents, export_flood_data

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
    row1_col1, row1_col2 = st.columns([2, 1])
    with row1_col2:

        before_start = st.date_input(" start date imagery before the flooding event")
        before_end = st.date_input("end date imagery before the flooding event")
        after_start = st.date_input(" start date imagery after the flooding event")
        after_end = st.date_input("end date imagery after the flooding event")
        add_slider = st.slider(
        'Select a threshold',
        0.0, 5.0, 1.0, 0.25, help('higher value might reduce overall noise'))
        #     # To convert to a string based IO:
        # uploaded_file = st.file_uploader("Choose a file")
        # if uploaded_file is not None:
        #     # To read file as bytes:
        #     bytes_data = uploaded_file.getvalue()
        #     st.write(bytes_data)

        #     # To convert to a string based IO:
        #     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        #     st.write(stringio)

        #     # To read file as string:
        #     string_data = stringio.read()
        #     st.write(string_data)

        #     # Can be used wherever a "file-like" object is accepted:
        #     dataframe = pd.read_csv(uploaded_file)
        #     st.write(dataframe)
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
        with st.expander(
            "Steps: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button. Expand this tab to see a demo 👉"
        ):
            video_empty = st.empty()

        data = st.file_uploader(
            "Upload a GeoJSON file to use as an ROI. Customize timelapse parameters and then click the Submit button 😇👇",
            type=["geojson", "kml", "zip"],
        )

        crs = "epsg:4326"
        Map = geemap.Map(
            basemap="HYBRID",
            plugin_Draw=True,
            Draw_export=True,
            locate_control=True,
            plugin_LatLngPopup=False,
        )
        Map.add_basemap("ROADMAP")

    with row1_col1:
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
app()

