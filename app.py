import glob
import os

import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS

from clarifai.client.model import Model
from clarifai.client.input import Inputs
from services import voice
from dotenv import load_dotenv

load_dotenv()


########################
# Required in every Clarifai streamlit app
########################

######################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the URL of 
# the text we want as an input. Change these strings to run your own example.
######################################################################################################

# Your PAT (Personal Access Token) can be found in the portal under Authentification

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

PAT = os.environ['PAT']
ELEVENLABS_TOKEN = os.environ['ELEVENLABS_TOKEN']

os.environ['CLARIFAI_PAT'] = PAT

st.set_page_config(layout="wide")
st.title("EyeCue")
st.markdown("## the smart video creator for Career inspiration")
eleven_token = ""
with st.sidebar: 
  eleven_token = st.text_input("elevenlabs token", value=ELEVENLABS_TOKEN)


def llm_multimodal(file_bytes,prompt):
    model = "https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision"
    inference_params = dict(temperature=0.2, max_tokens=100)

    input = None
    if file_bytes != None:
      input = Inputs.get_multimodal_input(
                input_id="", 
                image_bytes = file_bytes if file_bytes != None else None, 
                raw_text=prompt)
    
    else:
      input = Inputs.get_text_input(input_id="",raw_text=prompt)

    model_prediction = Model(model).predict(inputs = [input], inference_params=inference_params)
    return model_prediction.outputs[0].data.text.raw

# IMAGE_FILE_LOCATION = './content/malte.png'
# with open(IMAGE_FILE_LOCATION, "rb") as f:
#     file_bytes = f.read()

job_role = st.text_input("Job Role")
if job_role:
    prompt = f"Make a 3-5 sentence emotional elevator pitch to a candidate in the style of Sir Attenborough, that the {job_role} is great and you are going to present some good jobs. Do not mention your name."
    text = llm_multimodal(None,prompt)
    voice.generate_audio(text,eleven_token)
    st.markdown(text)

uploaded_file = st.file_uploader("Choose a file")







if uploaded_file is not None:
    # To read file as bytes:
    file_bytes = uploaded_file.getvalue()
    #st.write(file_bytes)
    prompt = "Is there at least one person on this image? How positive on a scale from 1-10 will this image be perceived? Use JSON as an output format with attributes is_person and positivity_rating.s"
    text = llm_multimodal(file_bytes, prompt)
    st.markdown(text)



    ClarifaiStreamlitCSS.insert_default_css(st)

    st.markdown("Please select a specific page by adding it to the url")



# cols = st.columns(10)

# d = os.path.dirname(__file__)
# for fi, f in enumerate(glob.glob(os.path.join(d, "pages", "*.py"))):
#   name = os.path.splitext(os.path.basename(f))[0]
#   ClarifaiStreamlitCSS.buttonlink(cols[fi % len(cols)], name, "/" + name)
