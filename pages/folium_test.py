import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

"## Try drawing some objects and then clicking on them"

m = folium.Map(location=[39.949610, -75.150282], zoom_start=5)
Draw(export=True).add_to(m)

c1, c2 = st.columns(2)
with c1: 
    output = st_folium(m, width = 700, height=500)

with c2:
    st.write(output)
    st.write(output["all_drawings"]==None or output["all_drawings"]==[])
    # if output['all_drawings'] is not None and len(output['all_drawings'])>0:
    #     coords = output['all_drawings'][-1]['geometry']['coordinates']
    #     st.write(coords)
    # else:
    #     st.write("Nothing selected")