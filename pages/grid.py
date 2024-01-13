from itertools import cycle

import numpy as np
import streamlit as st
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.modules.css import ClarifaiStreamlitCSS

from utils.api_utils import list_all_inputs
from utils.mosaic import download_urls

##########################################################
ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
userDataObject = auth.get_user_app_id_proto()
st.title("Grid Input Viewer")

with st.form(key="data-inputs"):
  mtotal = st.number_input(
      "Select number of images to view as a grid:", min_value=1, max_value=100)
  submitted = st.form_submit_button('Submit')

if submitted:
  if mtotal is None or mtotal == 0:
    st.warning("Number of images must be provided.")
    st.stop()
  else:
    st.write("Number of images in grid will be: {}".format(mtotal))

  # Stream inputs from the app
  all_images = []

  #Change this function with list_inputs once per_page filter arguement added with new SDK.
  images_response = list_all_inputs(userDataObject)
  for inp in images_response.inputs:
    if inp.data.image is not None:
      all_images.append(inp.data.image)
    if len(all_images) >= mtotal:
      break

  url_list = [im.url for im in all_images if im.url != ""]
  filteredImages = [tup[1] for tup in download_urls(url_list, auth.pat)]

  # caption = [] # your caption here
  cols = cycle(
      st.columns(4))  # st.columns here since it is out of beta at the time I'm writing this
  for idx, filteredImage in enumerate(filteredImages):
    next(cols).image(np.array(filteredImage), use_column_width=True)
