import glob
import os

import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS

########################
# Required in every Clarifai streamlit app
########################

st.set_page_config(layout="wide")

ClarifaiStreamlitCSS.insert_default_css(st)

st.markdown("Please select a specific page by adding it to the url")

cols = st.columns(10)

d = os.path.dirname(__file__)
for fi, f in enumerate(glob.glob(os.path.join(d, "pages", "*.py"))):
  name = os.path.splitext(os.path.basename(f))[0]
  ClarifaiStreamlitCSS.buttonlink(cols[fi % len(cols)], name, "/" + name)
