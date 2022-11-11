import streamlit as st
import streamlit_ext as ste
import streamlit.components.v1 as components
import geemap.foliumap as geemap
import ee
import requests
import folium
from flood_functions import derive_flood_extents
from folium.plugins import Draw, Geocoder, MiniMap
from streamlit_folium import st_folium
import datetime as dt
from sidebar_functions import add_logo, add_about

st.set_page_config(layout="wide")

add_logo("img/MA-logo.png")
add_about()
st.markdown("# Flood extent analysis")

def error_markdown(err_text):
    err_text_formatted = '<p style="color:Red; font-weight: bold; font-size: 18px;">Error: '+err_text+'</p>'
    return st.markdown(err_text_formatted, unsafe_allow_html=True)

def output_markdown(out_text):
    out_text_formatted = '<p style="font-size: 18px;">'+out_text+'</p>'
    return st.markdown(out_text_formatted, unsafe_allow_html=True)

st.markdown("""
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
""", unsafe_allow_html=True)

@st.cache
def initialize_ee():
    ee.Initialize()

initialize_ee()

def app():
    if "output_created" not in st.session_state:
        st.session_state.output_created = False
    def callback():
        st.session_state.output_created = False
    # st.header("Flood extent detection tool")
    row1 = st.container()
    row2 = st.container()
    col1, col2 = row1.columns([2, 1])
    with col1:
        with st.expander("Input map", expanded=True):
            Map = folium.Map(
                location=[52.205276, 0.119167], 
                zoom_start=3,
                control_scale = True,
                # crs='EPSG4326'
                )
            Draw(
                export=False,
                draw_options={
                    'circle':False,
                    'polyline':False,
                    'polygon':False,
                    'circle':False,
                    'marker':False,
                    'circlemarker':False
                }
                ).add_to(Map)
            Geocoder(
                add_marker=False
            ).add_to(Map)
            MiniMap().add_to(Map)
            # data = st.file_uploader(
            #     "Upload a GeoJSON file to use as an ROI.",
            #     type=["geojson", "kml", "zip"],
            # )
            # ss = st.empty()
            # with ss:
            output = st_folium(Map, width = 800, height=600)
            # if data is not None:
            #     with ss:
            #         # gj = geojson.load(data)
            #         # coords = gj['features'][0]['geometry']['coordinates']
            #         st.write('Still to be implemented') 
    with col2:
        with st.expander("Choose Image Dates"):
            before_start = st.date_input(
                "Start date for reference imagery",
                value=dt.date(2022, 7, 1),
                help='It needs to be prior to the flooding event',
                on_change=callback
                )
            before_end = st.date_input(
                "End date for reference imagery",
                value=dt.date(2022, 7, 30),
                help=(
                    'It needs to be prior to the flooding event, at least 15 '
                    'days subsequent to the date selected above'
                    ),
                on_change=callback
                )
            after_start = st.date_input(
                "Start date for flooding imagery",
                value=dt.date(2022, 9, 1),
                help='It needs to be subsequent to the flooding event',
                on_change=callback
            )
            after_end = st.date_input(
                "End date for flooding imagery",
                value=dt.date(2022, 9, 16),
                help=(
                    'It needs to be subsequent to the flooding event and at '
                    'least 10 days to the date selected above'
                    ),
                on_change=callback
                )
        with st.expander("Choose Parameters"):        
            add_slider = st.slider(
                label='Select a threshold',
                min_value=0.0, 
                max_value=5.0, 
                value=1.25, 
                step=0.25, 
                help='higher value might reduce overall noise',
                on_change=callback
                )
            # polarization = st.radio(
            #     "Set polarization",
            #     ["VH", "VV"],
            #     on_change=callback
            #     )
            pass_direction = st.radio(
                "Set pass direction",
                ["Ascending", "Descending"],
                on_change=callback
                )
        submitted = st.button('Compute flood extent')
        check_dates = before_start<before_end<=after_start<after_end
        check_drawing = output['all_drawings'] != []\
            and output['all_drawings'] is not None
    if submitted:
        with col2:
            if not check_dates:
                st.error(
                    "Make sure that the dates were inserted correctly"
                    )
            elif not check_drawing:
                st.error("No region selected")
            else:
                with st.spinner("Computing... Please wait..."):
                    # output_markdown("Computing... Please wait...")
                    coords = output['all_drawings'][-1]['geometry']['coordinates'][0]
                    ee_geom_region = ee.Geometry.Polygon(coords) 
                    detected_flood_vector, detected_flood_raster, _, _ = derive_flood_extents(
                        aoi=ee_geom_region,
                        before_start_date=str(before_start),
                        before_end_date=str(before_end),
                        after_start_date=str(after_start),
                        after_end_date=str(after_end),
                        difference_threshold=add_slider,
                        polarization='VH',
                        pass_direction=pass_direction,#pass_direction,
                        export=False)
                    # output_markdown("Detection complete")                  
                    # st.session_state['is_expanded'] = False  
                    Map2 = geemap.Map(
                        # basemap="HYBRID",
                        plugin_Draw=False,
                        Draw_export=False,
                        locate_control=False,
                        plugin_LatLngPopup=False,
                        )
                    # output_markdown("Map generated")
                    try:
                        Map2.add_layer(detected_flood_raster, {}, "Flood extent raster")
                    # output_markdown("Flood raster added to the map")
                        Map2.centerObject(detected_flood_raster)
                    except Exception as e:
                        if 'If one image has no bands, the other must also have no bands' in str(e):
                            st.error(
                                "No satellite image found for the selected dates.\n\n"
                                "Try changing the pass direction or the polarization.\n\n"
                                "If this does not work, choose different dates: "
                                "it is likely that the satellite did not cover "
                                "the area of interest in the range of dates "
                                "specified (either before or after the flooding "
                                "event)."
                                )
                        else:
                            raise
                    else:
                        st.success("Computation complete")
                        st.session_state.output_created = True
                        st.session_state.Map2 = Map2
                        st.session_state.detected_flood_raster = detected_flood_raster
                        st.session_state.detected_flood_vector = detected_flood_vector
                        st.session_state.ee_geom_region = ee_geom_region
    if st.session_state.output_created:
        with row2:
            with st.expander("Output map", expanded=True):
                st.session_state.Map2.to_streamlit()
                submitted2 = st.button('Export to file')
                if submitted2:
                    with st.spinner("Computing... Please wait..."):
                        try:
                            url_r = st.session_state.detected_flood_raster.getDownloadUrl({
                                'region': st.session_state.ee_geom_region,
                                'scale': 30,
                                'format': 'GEO_TIFF'
                            })
                        except:
                            st.error(
                                "The image size is too big for the image to be "
                                "exported to file. Select a smaller area of "
                                "interest (side <~ 150km) and repeat the analysis."
                            )
                        else:
                            response_r = requests.get(url_r)
                            url_v = st.session_state.detected_flood_vector.getDownloadUrl('GEOJSON')
                            response_v = requests.get(url_v)
                            with row2:
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
                            st.success("Computation complete")


app()

