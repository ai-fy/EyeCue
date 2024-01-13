import altair as alt
import pandas as pd
import streamlit as st
from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.modules.css import ClarifaiStreamlitCSS
from stqdm import stqdm

from utils.api_utils import (concept_key, concept_list, get_annotations_for_input_batch,
                             list_all_inputs)

page_size = 16

ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
stub = create_stub(auth)
userDataObject = auth.get_user_app_id_proto()

# st.session_state['total'] = 0
# st.session_state.get_input_count_response = {}

st.title("App Data Metrics")
with st.form(key="metrics-inputs"):
  st.text("This will compute a bunch of stats about your app. You ready?")
  submitted = st.form_submit_button('Ready')

if submitted:
  # Set in the app.py file.
  # total = st.session_state['total']

  concepts = []
  concept_response = concept_list(userDataObject)
  #st.write(f"concept status:{getattr(concept_response,'concepts')}")
  if hasattr(concept_response, "concepts"):
    for inp in getattr(concept_response, 'concepts'):
      concepts.append(inp)

  concept_ids = [concept_key(c) for c in concepts]

  # List all the inputs
  all_inputs = []
  input_response = list_all_inputs(userDataObject)
  for inp in input_response.inputs:
    if inp is not None:
      all_inputs.append(inp)

  # Stream inputs from the app
  all_annotations = []
  for i in stqdm(range(0, len(all_inputs), page_size), desc="Loading annotations for inputs"):
    batch = all_inputs[i:i + page_size]
    annotations = get_annotations_for_input_batch(stub, userDataObject, auth.metadata, batch)
    all_annotations.extend(annotations)
  ###################

  # Now we aggregate counts over all the annotations we've loaded.
  # this will be a dict of dicts with outer key being the concept_key and the inner key being the
  # "p" or "n" for positive or negative.

  def accume_concept(counts_by_input_id, counts, c):
    key = concept_key(c)
    counts_by_input_id.setdefault(ann.input_id, {})
    counts_by_input_id[ann.input_id].setdefault(key, {"p": 0, "n": 0})
    counts.setdefault(key, {"p": 0, "n": 0})
    if c.value > 0:
      counts[key]["p"] += 1
      counts_by_input_id[ann.input_id][key]['p'] += 1
    else:
      counts[key]["n"] += 1
      counts_by_input_id[ann.input_id][key]['n'] += 1

  counts_by_input_id = {}  # this has an extra outer key by input_id.
  counts = {}
  for ann in all_annotations:
    for c in ann.data.concepts:
      accume_concept(counts_by_input_id, counts, c)
    for r in ann.data.regions:
      for c in r.data.concepts:
        accume_concept(counts_by_input_id, counts, c)

  print("These are the annotation counts per concept")
  counts_source = pd.DataFrame.from_dict({
      "concept": concept_ids,
      "positives": [counts.get(k, {
          "p": 0
      })["p"] for k in concept_ids],
      "negatives": [counts.get(k, {
          "n": 0
      })["n"] for k in concept_ids],
  })
  print(counts_source)

  counts_melted = counts_source.melt('concept', var_name='posneg', value_name='count')
  print(counts_melted)

  print("These are the input counts per concept")
  # for the counts that are unique per input.
  unique_counts = {}
  for _, d in counts_by_input_id.items():
    for key, input_counts in d.items():
      unique_counts.setdefault(key, {"p": 0, "n": 0})
      if input_counts['p'] > 0:  # if more than 1 for this input we increment by 1.
        unique_counts[key]["p"] += 1
      if input_counts['n'] > 0:
        unique_counts[key]["n"] += 1
  unique_counts_source = pd.DataFrame.from_dict({
      "concept": concept_ids,
      "positives": [unique_counts.get(k, {
          "p": 0
      })["p"] for k in concept_ids],
      "negatives": [unique_counts.get(k, {
          "n": 0
      })["n"] for k in concept_ids],
  })
  print(unique_counts_source)

  unique_counts_melted = unique_counts_source.melt(
      'concept', var_name='posneg', value_name='count')
  print(unique_counts_melted)

  # get_input_count_response = st.session_state['get_input_count_response']
  st.header("Input status", anchor="input-status")
  st.markdown("Accumulated input counts broken down by status.")
  # status = pd.DataFrame({
  #     "cat": ["processed", "processing", "to process", "error processing"],
  #     "value": [
  #         get_input_count_response.counts.processed, get_input_count_response.counts.processing,
  #         get_input_count_response.counts.to_process, get_input_count_response.counts.errors
  #     ]
  # })

  c = alt.Chart(counts_melted).mark_bar().encode(x='concept', y='sum(count)')
  text = c.mark_text(dy=-5).encode(text='sum(count)')
  st.altair_chart(c + text, use_container_width=True)

  base = alt.Chart(counts_melted).mark_arc().encode(
      theta=alt.Theta('concept', stack=True), color='concept')
  pie = base.mark_arc(outerRadius=120)
  text = base.mark_text(radius=140, size=20).encode(text="sum(count)")
  st.altair_chart(pie + text, use_container_width=True)

  # Finally plot the results to the UI.
  st.header("Annotation stats", anchor="data-stats")

  st.text("These are annotation counts per concept.")
  c = alt.Chart(counts_melted).mark_bar().encode(x='concept', y='sum(count)', color='posneg')
  st.altair_chart(c, use_container_width=True)

  st.text('someting else')

  base = alt.Chart(counts_melted).mark_arc().encode(
      theta=alt.Theta('sum(count)', stack=True), color='concept')
  pie = base.mark_arc(outerRadius=120)
  text = base.mark_text(radius=140, size=20).encode(text="concept")
  st.altair_chart(pie + text, use_container_width=True)

  st.text("These are input counts per concept.")
  c = alt.Chart(unique_counts_melted).mark_bar().encode(
      x='concept', y='sum(count)', color='posneg')
  st.altair_chart(c, use_container_width=True)

  base = alt.Chart(unique_counts_melted).mark_arc().encode(
      theta=alt.Theta('sum(count)', stack=True), color='concept')
  pie = base.mark_arc(outerRadius=120)
  text = base.mark_text(radius=160, size=20).encode(text="concept")
  st.altair_chart(pie + text, use_container_width=True)
