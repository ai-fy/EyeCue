import glob
import os

import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS

from clarifai.client.model import Model
from clarifai.client.input import Inputs



########################
# Required in every Clarifai streamlit app
########################

######################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the URL of 
# the text we want as an input. Change these strings to run your own example.
######################################################################################################

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = '0bc1049b7d9f486184f1c5f863bcae9f'
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'openai'
APP_ID = 'chat-completion'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'openai-gpt-4-vision'
MODEL_VERSION_ID = '266df29bc09843e0aee9b7bf723c03c2'
RAW_TEXT = 'What do you see on this picture?'
# To use a hosted text file, assign the url variable
# TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'
# Or, to use a local text file, assign the url variable
# TEXT_FILE_LOCATION = 'YOUR_TEXT_FILE_LOCATION_HERE'

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

os.environ['CLARIFAI_PAT'] = PAT

st.set_page_config(layout="wide")
st.title("EyeCue, the smart video creator for Career inspiration")

# IMAGE_FILE_LOCATION = './content/malte.png'
# with open(IMAGE_FILE_LOCATION, "rb") as f:
#     file_bytes = f.read()


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    file_bytes = uploaded_file.getvalue()
    #st.write(file_bytes)

prompt = "How will people probably perceive this person."
inference_params = dict(temperature=0.2, max_tokens=100)

model_prediction = Model("https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision").predict(inputs = [Inputs.get_multimodal_input(input_id="", image_bytes = file_bytes, raw_text=prompt)], inference_params=inference_params)


st.markdown(model_prediction.outputs[0].data.text.raw)



ClarifaiStreamlitCSS.insert_default_css(st)

st.markdown("Please select a specific page by adding it to the url")



cols = st.columns(10)

d = os.path.dirname(__file__)
for fi, f in enumerate(glob.glob(os.path.join(d, "pages", "*.py"))):
  name = os.path.splitext(os.path.basename(f))[0]
  ClarifaiStreamlitCSS.buttonlink(cols[fi % len(cols)], name, "/" + name)
