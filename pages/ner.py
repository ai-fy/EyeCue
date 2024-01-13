import streamlit as st
from annotated_text import annotated_text
from clarifai.client.model import Model

#Note(Eran) turn to multipage app where all demos are nested under a pretrained_models_demos subfolder

# Uses the enviorment variables CLARIFAI_USER_ID, CLARIFAI_APP_ID, CLARIFAI_PAT
# (although only PAT is needed for authentication as we're used a pretrained model)

# Main page title
st.title("NER Demo")
# Define color templates
ent_colors = {"PER": "#8ce59e", "LOC": '#8edce4', "ORG": '#79abdc', "MISC": '#8d7dca'}

# Get User text and run prediction
with st.spinner("Finding Entities"):
  text_input = st.text_area("Press ⌘+Enter to rerun NER prediction:",
                            "Eran lives in New York\nand works for Clarifai")
  response = Model("https://clarifai.com/clarifai/main/models/ner-english").predict_by_bytes(
      bytes(text_input, 'utf-8'), "text")
  output = response.outputs[0]  #no batching

  # Turn Clarifai response to streamlit annotated text standard
  ents = []
  for region in output.data.regions:
    char_start = region.region_info.span.char_start
    char_end = region.region_info.span.char_end
    entity_name = region.data.concepts[0].name
    entity_confidence = region.data.concepts[0].value
    if entity_name == "O":
      ents.append(text_input[char_start:char_end])
    else:
      ents.append((text_input[char_start:char_end], entity_name, ent_colors[entity_name]))

  annotated_text(*ents)
