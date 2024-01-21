import glob
import json
import os

import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS

from clarifai.client.model import Model
from clarifai.client.input import Inputs
from services import voice
from services import video
from services import story as Story
from services import llm
from dotenv import load_dotenv
import datetime
import yaml
import services.research_agend as research_agend
import random



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
SERP_TOKEN = os.environ['SERP_API']

os.environ['CLARIFAI_PAT'] = PAT


def show_all_scenes(_story):
    print("showing story with "+str(len(_story.getScenes()))+" scenes")
    st.session_state["current_story"] = _story
    container_to_show_in = st.session_state["story_area2"]
    container_to_show_in = container_to_show_in.empty()
    container_to_show_in = container_to_show_in.container()
    with container_to_show_in:
      
      st.markdown("## Current Story about "+_story.getRoleText())
      st.markdown("*What Employees like:* "+_story.getEmployeeFeedback())

      column_count = 3
      if _story.hasVideo() == True:
        column_count = column_count + 1
      # else:
      #    if st.button("video", key="video_in_editor"+str(_story.getRoleText())+"_"+str(container_to_show_in)):
      #       vid = video.Video()
      #       vid.create_video(_story)
      #       st.write("video created")
      #       session_stories.save()
      #       st.experimental_rerun()

      row_count = int(len(_story.getScenes()) / column_count) + 1
      print("rows: "+str(row_count))
      rows = st.columns(row_count)
      row_colums = []

      for row in rows:
        #with row:
          columns = st.columns(column_count)
          row_colums.append(columns)

      #columns = st.columns(column_count)
      scene_counter = 0
      col_counter = 0
      scenes = _story.getScenes()
      
      if _story.hasVideo() == True:
        with row_colums[0][col_counter]:
          st.write("## Generated Video")
          vid = _story.getVideo()
          st.video(vid)
          col_counter = col_counter + 1
      
      for scene in scenes:
        #with columns[col_counter % len(columns)]:
        row_to_use = col_counter // column_count
        col_to_use = col_counter % column_count

        with row_colums[row_to_use][col_to_use]:  
          print(f"using row {row_to_use} and col {col_to_use}")
          scene_counter = scene_counter + 1
          col_counter = col_counter + 1
          
          st.write(f"## Scene {scene_counter}")
          desc = _story.getSceneDescription(scene_counter)
          st.markdown(f"{desc}")
          
          st.write("### Visual")
          image_prompt = _story.getVisualPrompt(scene_counter)
          st.markdown(f"{image_prompt}")
          image_filepath = _story.getSceneImage(scene_counter)
          if image_filepath != "":
            st.image(image_filepath)
          else:
            st.markdown("no image")

          st.markdown("### Voice")
          audio_prompt = _story.getAudioPrompt(scene_counter)
          st.markdown(f"{audio_prompt}")
          
          audio_path = _story.getSceneAudio(scene_counter)
          if audio_path != "":
            st.audio(audio_path)
          else:
            st.write("no audio")
        

        

st.set_page_config(layout="wide")
st.title("EyeCue - GenAI for recruiting videos")
#st.markdown("## the smart video creator for Career inspiration")
home,research = st.tabs(["Generate Story", "Research Agend"])
eleven_token = ""
stories = Story.stories()


#------------- load stories from filesystem ------------------- #
#check if stories exist in session state, if not create
if "stories" not in st.session_state:
  if stories.isSaved():
    stories.load()
    #st.write("loaded stories from filesystem")
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


  on = st.toggle('Show Archive')

  if on:
    
    for element in session_stories.getStories(): #<._stories["_stories"]:
      story = element["story"]
      scenes = story.getScenes()
      #print(scenes)
      with st.expander(story.getRoleText()):

        if story.hasVideo() != True:
          if st.button("video", key="video"+str(element["id"])):
            vid = video.Video()
            vid.create_video(story)
            st.write("video created")
            session_stories.save()
        

        if st.button("edit", key="edit"+str(element["id"]),on_click=show_all_scenes, args=[story]): #, key="edit "+str(element["id"])):
          st.write("editing")
          #set current story to session state to edit
          st.session_state["current_story"] = story

        if story.hasVideo():
          st.markdown("### Video")
          st.video(f"{story.getVideo()}")
          
        # iterate all scenes in story
        for scene in story.getScenes():
          st.write(f"## Scene {scene.get('number','')}")
          st.markdown(f"{scene['text']}")
          
          #st.write("### Visual")
          #st.markdown(f"{scene['visualprompt']}")
          st.image(scene["image"])

          #st.markdown("### Voice")  
          #st.markdown(f"{scene['voiceover']}")
          if eleven_token != "":
            st.audio(scene["audio"])
          else:
            st.write("no token, no audio")

        # for audio_path in story.getAudioPaths():
        #   if audio_path != "":
        #     st.audio(audio_path) 
        #   else:
        #     st.write("no audio")
        
        # #display generated images
        # for image_path in story.getImagePaths():
        #   st.image(image_path)

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


with research:
   research_agend.show()

with home:

  # search_query = st.text_input("Search Query", "Data Scientist")
  # if st.button("Search Jobs"):
  #   research_agend.search_jobs(SERP_TOKEN,search_query)
  #   st.write("searching jobs for "+search_query)
    

  with st.form(key="story_form"):
    
    job_role = st.text_input("Job Role",key="job_role")
    company = st.text_input("Company",value="LabLab.ai")
    max_number_of_scenes = st.number_input("Max number of scenes", min_value=1, max_value=10, value=3)

    employee_feedback = ""    
    if st.form_submit_button("Generate Storyboard"):

      with st.status(f"first i will do some research about what people like at {company}") as status:
        contents, summary = research_agend.run_metaphor_search(company)
        st.write(summary)
        status.update(label="now i will extract the essence of the research")
        storyboard = llm.llm_multimodal(None,f"Generate a 40 seconds video storyboard for the job role {job_role} at the company {company}. Here are some things that employees like about the company, uses this in your storyline: '{summary}'. Now, Describe each of {max_number_of_scenes} scene. For each scene find very attention catching hooks and generate the following, - desciption: Describe the scene shortly with a great hook - visualprompt: Generate a prompt for the scene for an image generator, describing very positive energetic persons, clothes, light, perspective in this prompt. Do not include Text or logos. Prefer showing happy people. Generate a portrait orientation in 9:16 format - voiceover: the very short and compelling one sentence text of the speaker in the voice of Sir Attemborough (without mentioning his name). The video should be very positive and inspire to do the next career step. Start with presenting the role and end with present some great jobs. Do not mention your name. Write from an external perspective of someone outside the company who knows a lot about it. Output a clean utf-8 JSON as text without JavaScript Object Notation formatted data, that contains a scenes array with the scenes at the top level.")
        status.update(label="now we created a storyboard for you and will start to generate the scenes.")
        print(storyboard)
        
        storyboard = storyboard.replace("```json","")
        storyboard = storyboard.replace("```","")
        storyboard = storyboard.replace("json","") #remove javascript object notation from string, if LLM is not compliant
        
        #st.write(storyboard)
        #st.write(str(type(storyboard)))
        #------------------- The current story in main page ------------------- #

      

        try:
          parsed_storyboard = json.loads(storyboard)
          story = Story.story(job_role)
          story.addEmployeeFeedback(summary)
          story.addStory(storyboard)
          scenes = parsed_storyboard["scenes"]
          scene_counter = 0
          for scene in scenes:
            scene_counter = scene_counter + 1
            image_filepath, prompt, width, height = llm.generate_image(scene["visualprompt"])
            status.update(label="generated an image for the scene")
            if eleven_token != "":
              audio_filepath = voice.generate_audio(scene["voiceover"],eleven_token)
              status.update(label="generated audio for the scene")
            else:
              audio_filepath = ""

            story.addScene(scene["description"],scene['visualprompt'],image_filepath,scene["voiceover"],audio_filepath,scene_counter)
            status.update(label="added another scene to story")
            show_all_scenes(story)
        except Exception as e:
          st.write("not parsed storyboard")
          st.write(e)

        stories = st.session_state["stories"]
        stories.addStory(story)
        stories.save()
        st.session_state["stories"] = stories
        st.session_state["current_story"] = story
        st.balloons()
        #show_all_scenes(story)

  # if job_role and st.button("Generate Story"):
  #     prompt = f"Make a 3 sentence emotional elevator pitch to a candidate in the style of Sir Attenborough, that the {job_role} is great and you are going to present some good jobs. Do not mention your name. Also make a prompt to generate a very appealing photography of an impressive person doing this job and name the role. Output both as a JSON with attributes story and impage_prompt."
  #     text = llm.llm_multimodal(None,prompt)
  #     #convert text to JSON
  #     parsed = json.loads(text)
  #     story_text = parsed["story"]
      
  #     story = Story.story(job_role)
  #     story.addStory(story_text)

  #     st.markdown(text)

  #     audio_filepath = voice.generate_audio(story_text,eleven_token)
  #     if audio_filepath == "":
  #       st.write("no audio generated, maybe no Eleven_labs token entered?")
  #     story.addAudio(audio_filepath,story_text)

  #     image_filepath, prompt, width, height = llm.generate_image(parsed["image_prompt"])
  #     story.addImage(image_filepath, width, height, parsed["image_prompt"])
  #     stories = st.session_state["stories"]
  #     stories.addStory(story)
  #     stories.save()
  #     st.session_state["stories"] = stories
  #     st.session_state["current_story"] = story
  #     #st.experimental_rerun() #updating ui to reflect new story
  #     #show_story_on_mainpage(story)





  print("calling st.empty")

  if "current_story" in st.session_state:
    _story = st.session_state["current_story"]
    if _story.hasVideo() != True:
      if st.button("Generate Video", key="video_in_mainpage_top"+str(_story.getRoleText())):
        vid = video.Video()
        vid.create_video(_story)
        st.write("video created")
        session_stories.save()
        st.balloons()
        #st.experimental_rerun()

  placeholder = st.empty()
  with placeholder.container():
    st.info("### Select a Story in the Archive left or generate a new Story above")

  st.session_state["story_area2"] = placeholder

  if "current_story" in st.session_state:
  
    print("showing story from session.")
    # _story = st.session_state["current_story"]
    # if _story.hasVideo() == True:
    #   if st.button("show Video", key="video_in_modal"+str(_story.getRoleText())):
    #     with st.Modal():
    #       st.header("Video for "+_story.getRoleText())
    #       st.video(f"{_story.getVideo()}")    
    #       st.button("Close Modal")
      
    # else:
    #      if st.button("video", key="video_in_editor"+str(_story.getRoleText())):
    #         vid = video.Video()
    #         vid.create_video(_story)
    #         st.write("video created")
    #         session_stories.save()
    #         #st.experimental_rerun()
    show_all_scenes(st.session_state["current_story"])

ClarifaiStreamlitCSS.insert_default_css(st)

#st.markdown("Please select a specific page by adding it to the url")



# cols = st.columns(10)

# d = os.path.dirname(__file__)
# for fi, f in enumerate(glob.glob(os.path.join(d, "pages", "*.py"))):
#   name = os.path.splitext(os.path.basename(f))[0]
#   ClarifaiStreamlitCSS.buttonlink(cols[fi % len(cols)], name, "/" + name)

