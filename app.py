import glob
import json
import os

import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS

from clarifai.client.model import Model
from clarifai.client.input import Inputs
from services import voice
from services import story as Story
from services import llm
from dotenv import load_dotenv
import datetime
import yaml

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

def show_story_on_mainpage(current_story):
    
    area = st.session_state["story_area"]
    with area.container():
    
      st.markdown(f"## Current Story: {current_story._role}")
    #display generated images
      for image_path in current_story.getImagePaths():
        st.image(image_path)

    #display generated audio
      for audio_path in current_story.getAudioPaths():
        if audio_path != "":
          st.audio(audio_path) 
        else:
          st.write("no audio")


st.set_page_config(layout="wide")
st.title("EyeCue")
st.markdown("## the smart video creator for Career inspiration")
eleven_token = ""
stories = Story.stories()

#------------- load stories from filesystem ------------------- #
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

  st.markdown(f"## Generated Stories ("+str(st.session_state.stories.getStoryAmount())+")")
  session_stories = st.session_state["stories"]
  for element in session_stories.getStories(): #<._stories["_stories"]:
    story = element["story"]
    with st.expander(story._role):
      if st.button("edit", key="edit "+str(element["id"]),on_click=show_story_on_mainpage, args=(story,)): 
        st.write("editing")
        #set current story to session state to edit
        st.session_state["current_story"] = story
        

      for audio_path in story.getAudioPaths():
        if audio_path != "":
          st.audio(audio_path) 
        else:
          st.write("no audio")
      
      #display generated images
      for image_path in story.getImagePaths():
        st.image(image_path)

#------------------- The Repository in sidebar ------------------- #
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

  # ------------------ Images in sidebar ------------------------ #
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

# ------------------ Story generation in main page  ------------------------ #
job_role = st.text_input("Job Role",key="job_role")
company = st.text_input("Company",value="Gymondo")
max_number_of_scenes = st.number_input("Max number of scenes", min_value=1, max_value=10, value=3)

if job_role and st.button("Generate Storyboard"):
  storyboard = llm.llm_multimodal(None,f"Generate a 40 seconds video storyboard for the job role {job_role} at the company {company}. Describe each of maximally {max_number_of_scenes} scene. For each scene describe the following, - desciption: Describe the scene shortly - visualprompt: Generate a prompt for the scene for an image generator, describing persons, clothes, light, perspective in this prompt. Prefer showing happy people. - voiceover: the text of the speaker in the voice of Sir Attemborough (without mentioning his name). The video should be very positive and inspire to do the next career step. Start with presenting the role and end with present some great jobs. Do not mention your name. Output a clean utf-8 JSON as text without JavaScript Object Notation formatted data.")

  #st.write(storyboard)
  #st.write(str(type(storyboard)))

  try:
    parsed_storyboard = json.loads(storyboard)
    
    scene_counter = 0
    for scene in parsed_storyboard["scenes"]:
      scene_counter = scene_counter + 1
      
      st.write(f"## Scene {scene_counter}")
      st.markdown(f"{scene['description']}")
      
      st.write("### Visual")
      st.markdown(f"{scene['visualprompt']}")
      filename, prompt, width, height = llm.generate_image(scene["visualprompt"])
      st.image(filename)
      
      st.markdown("### Voice")  
      st.markdown(f"{scene['voiceover']}")
      if eleven_token != "":
        filepath = voice.generate_audio(scene["voiceover"],eleven_token)
        st.audio(filepath)
      else:
        st.write("no token, no audio")

  except Exception as e:
    st.write("not parsed storyboard")
    st.write(e)


if job_role and st.button("Generate Story"):
    prompt = f"Make a 3 sentence emotional elevator pitch to a candidate in the style of Sir Attenborough, that the {job_role} is great and you are going to present some good jobs. Do not mention your name. Also make a prompt to generate a very appealing photography of an impressive person doing this job and name the role. Output both as a JSON with attributes story and impage_prompt."
    text = llm.llm_multimodal(None,prompt)
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

    filename, prompt, width, height = llm.generate_image(parsed["image_prompt"])
    story.addImage(filename, width, height, parsed["image_prompt"])
    stories = st.session_state["stories"]
    stories.addStory(story)
    stories.save()
    st.session_state["stories"] = stories
    st.session_state["current_story"] = story
    #st.experimental_rerun() #updating ui to reflect new story
    show_story_on_mainpage(story)

#------------------- The current story in main page ------------------- #

if (not ("story_area" in st.session_state)):
  st.write("creating story area")
  placeholder = st.empty()
  placeholder.text("EMPTY")
  st.session_state["story_area"] = placeholder


# ------------------ Testing Image Curation ------------------------ #
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    file_bytes = uploaded_file.getvalue()
    #st.write(file_bytes)
    prompt = "Is there at least one clear face of person on this image? Is it a photography? How positive on a scale from 1-10 will this image be perceived? Use JSON as an output format with attributes is_person, positivity_rating, is_photography"
    text = llm.llm_multimodal(file_bytes, prompt)
    st.markdown(text)



ClarifaiStreamlitCSS.insert_default_css(st)

#st.markdown("Please select a specific page by adding it to the url")



# cols = st.columns(10)

# d = os.path.dirname(__file__)
# for fi, f in enumerate(glob.glob(os.path.join(d, "pages", "*.py"))):
#   name = os.path.splitext(os.path.basename(f))[0]
#   ClarifaiStreamlitCSS.buttonlink(cols[fi % len(cols)], name, "/" + name)

