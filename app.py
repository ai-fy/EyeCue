import glob
import json
import os

import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS

from clarifai.client.model import Model
from clarifai.client.input import Inputs
from services import voice
from services import story as Story
from dotenv import load_dotenv
import datetime

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
stories = Story.stories()

#check if stories exist in session state, if not create
if "stories" not in st.session_state:
  if stories.isSaved():
    stories.load()
    st.write("loaded stories from filesystem")
  else: 
    st.write("no stories found, creating new")

  st.session_state["stories"] = stories



# ------------------- THE SIDEBAR ------------------- #

with st.sidebar: 


  eleven_token = st.text_input("elevenlabs token", value=ELEVENLABS_TOKEN)
  #load all files in folder ./audio and display them as audio files to click and play
  d = os.path.dirname(__file__)

  st.markdown(f"## Generated Stories ("+str(st.session_state["stories"]._stories["lastId"])+")")
  session_stories = st.session_state["stories"]
  for element in session_stories._stories["_stories"]:
    story = element["story"]
    with st.expander(story._role):

      for audio_path in story.getAudioPaths():
        if audio_path != "":
          st.audio(audio_path) 
        else:
          st.write("no audio")
      
      #display generated images
      for image_path in story.getImagePaths():
        st.image(image_path)

  st.markdown("# MEDIA REPOSITORY")
  with st.expander("## Generated audio files"):
    counter = 0
    for fi, f in enumerate(glob.glob(os.path.join(d, "audio", "*.wav"))):
      name = os.path.splitext(os.path.basename(f))[0]
      counter = counter + 1

      c1, c2 = st.columns([0.7,0.3])
      with c1:  
        st.audio(f, format='audio/wav', start_time=0)
      with c2:
        if st.button("delete", key="delete "+str(counter)):
          os.remove(f)
          st.write("deleted")


  #load all files in folder ./images and display them as images
  with st.expander("## Generated images"):
    counter = 0
    for fi, f in enumerate(glob.glob(os.path.join(d, "images", "*.png"))):
      name = os.path.splitext(os.path.basename(f))[0]
      counter = counter + 1
      #display image
      st.image("./images/"+name+".png")
      #display delete button
      if st.button("delete", key="delete image "+str(counter)):
        os.remove(f)
        st.write("deleted")

        
    #st.write(f)
    #st.write(name) 

@st.cache_data
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


@st.cache_data
def generate_image (prompt, width=1024, height=1024): 
  #prompt = "A cozy cabin in the woods surrounded by colorful autumn leaves"
  # inference_params = dict(width= width, height= height, steps=50, cfg_scale = 8.0)

  # # Model Predict
  # model_prediction = Model("https://clarifai.com/stability-ai/stable-diffusion-2/models/stable-diffusion-xl").predict_by_bytes(prompt.encode(), input_type="text", inference_params=inference_params)
  # output_base64 = model_prediction.outputs[0].data.image.base64

  inference_params = dict(quality="standard", size= f'{width}x{height}')

  # Model Predict
  model_prediction = Model("https://clarifai.com/openai/dall-e/models/dall-e-3").predict_by_bytes(prompt.encode(), input_type="text", inference_params=inference_params)

  output_base64 = model_prediction.outputs[0].data.image.base64
  #st.write(model_prediction.outputs[0].data.image.image_info)

  #add current date and time to filename
  now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
  filename = f'./images/generated_image_{now}.png'
  with open(filename, 'wb') as f:
    f.write(output_base64)
    st.image(filename, width=width, caption="Generated image")

  return filename,prompt, width, height

# IMAGE_FILE_LOCATION = './content/malte.png'
# with open(IMAGE_FILE_LOCATION, "rb") as f:
#     file_bytes = f.read()

job_role = st.text_input("Job Role")

if job_role and st.button("Generate Story"):
    prompt = f"Make a 3 sentence emotional elevator pitch to a candidate in the style of Sir Attenborough, that the {job_role} is great and you are going to present some good jobs. Do not mention your name. Also make a prompt to generate a very appealing photography of an impressive person doing this job and name the role. Output both as a JSON with attributes story and impage_prompt."
    text = llm_multimodal(None,prompt)
    #convert text to JSON
    parsed = json.loads(text)
    story_text = parsed["story"]
    
    story = Story.story(job_role)
    story.addStory(story_text)

    st.markdown(text)

    audio_filepath = voice.generate_audio(story_text,eleven_token)
    if audio_filepath == "":
      st.write("no audio generated, maybe no Eleven_labs token entered?")
    story.addAudio(audio_filepath,story_text)

    filename, prompt, width, height = generate_image(parsed["image_prompt"])
    story.addImage(filename, width, height, parsed["image_prompt"])
    stories = st.session_state["stories"]
    stories.addStory(story)
    stories.save()
    st.session_state["stories"] = stories
    st.experimental_rerun() #updating ui to reflect new story
    
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
