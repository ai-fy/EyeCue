import streamlit as st
import datetime
from clarifai.client.model import Model
from clarifai.client.input import Inputs
from clarifai.client.model import Model


vision_model = "https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision"
image_model = "https://clarifai.com/openai/dall-e/models/dall-e-3"
image_model2 = "https://clarifai.com/stability-ai/stable-diffusion-2/models/stable-diffusion-xl"

# ------------------ Functions for Clarify interaction --------------------- #

#-------------------------------------------#        
# ----- Function for multimodal model ----- #      
#-------------------------------------------#  
@st.cache_data
def llm_multimodal(file_bytes,prompt):
   
    inference_params = dict(temperature=0.2, max_tokens=100)

    input = None
    if file_bytes != None:
      input = Inputs.get_multimodal_input(
                input_id="", 
                image_bytes = file_bytes if file_bytes != None else None, 
                raw_text=prompt)
    
    else:
      input = Inputs.get_text_input(input_id="",raw_text=prompt)

    model_prediction = Model(vision_model).predict(inputs = [input], inference_params=inference_params)
    return model_prediction.outputs[0].data.text.raw


#-------------------------------------------#
# ----- Function for image generation ----- #
#-------------------------------------------#

@st.cache_data
def generate_image (prompt, width=1024, height=1792): 
    
  inference_params = dict(quality="standard", size= f'{width}x{height}')
  model_prediction = Model(image_model).predict_by_bytes(prompt.encode(), input_type="text", inference_params=inference_params)
  output_base64 = model_prediction.outputs[0].data.image.base64
  #st.write(model_prediction.outputs[0].data.image.image_info)

  #add current date and time to filename
  now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
  filename = f'./images/generated_image_{now}.png'
  with open(filename, 'wb') as f:
    f.write(output_base64)

  return filename,prompt, width, height