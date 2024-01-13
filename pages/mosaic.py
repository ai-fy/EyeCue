import streamlit as st
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.modules.css import ClarifaiStreamlitCSS

from utils.api_utils import list_all_inputs
from utils.mosaic import urls_to_mosaic

##########################################################

ClarifaiStreamlitCSS.insert_default_css(st)
# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
userDataObject = auth.get_user_app_id_proto()

# st.session_state.total = 0

st.title("Image Mosaic Builder")
with st.form(key="mosiac-inputs"):

  mtotal = st.number_input("Select number of images to add to mosaic:", min_value=1, max_value=100)
  submitted = st.form_submit_button('Submit')

if submitted:
  if mtotal is None or mtotal == 0:
    st.warning("Number of images must be provided.")
    st.stop()
  else:
    st.write("Mosaic number of images will be: {}".format(mtotal))

  # total = st.session_state['total']

  # Stream inputs from the app
  all_images = []
  #Change this function with list_inputs once per_page filter arguement added with new SDK.
  resp = list_all_inputs(userDataObject)
  for inp in resp.inputs:
    if inp.data.image is not None:
      all_images.append(inp.data.image)
    if len(all_images) >= mtotal:
      break

  url_list = [im.url for im in all_images if im.url != ""]

  if len(url_list) == 0:
    st.write("Please add image inputs into your app !")

  else:
    mosaic = urls_to_mosaic(url_list, auth.pat)
    st.image(mosaic)
