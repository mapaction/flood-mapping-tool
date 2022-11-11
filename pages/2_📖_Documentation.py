import streamlit as st
from sidebar_functions import add_logo, add_about

st.set_page_config(layout="wide")

add_logo("MA-logo.png")
add_about()
st.markdown("# Documentation")

url_1 = 'https://un-spider.org/advisory-support/recommended-practices/recommended-practice-google-earth-engine-flood-mapping/step-by-step'
url_2 = 'https://mapaction.atlassian.net/wiki/spaces/GAFO/pages/16032071853/Rapid+flood+mapping+from+satellite+imagery+description'
url_3 = 'https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar'

st.markdown("### Useful links")
st.markdown("[Link 1](%s)" % url_1)
st.markdown("[Link 2](%s)" % url_2)
st.markdown("[Link 3](%s)" % url_3)
