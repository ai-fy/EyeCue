
######################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the URL of 
# the text we want as an input. Change these strings to run your own example.
######################################################################################################

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = '3c426c65b7d843859eaee7fe56dc8640'
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'eleven-labs'
APP_ID = 'audio-generation'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'speech-synthesis'
MODEL_VERSION_ID = 'f2cead3a965f4c419a61a4a9b501095c'
RAW_TEXT = 'I love your product very much'
# To use a hosted text file, assign the url variable
# TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'
# Or, to use a local text file, assign the url variable
# TEXT_FILE_LOCATION = 'YOUR_TEXT_FILE_LOCATION_HERE'

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

from clarifai.client.model import Model


def generate_audio (text,token):
    

    input = text
    api_key = token

    inference_params = dict( model_id="eleven_multilingual_v2", stability= 0.5, similarity_boost= 0.5, style=0,use_speaker_boost=True, api_key = api_key)
    inference_params['voice-id']="mKSoejsrVfEDyafPAHdx"

    # Model Predict
    model_prediction = Model("https://clarifai.com/eleven-labs/audio-generation/models/speech-synthesis").predict_by_bytes(input.encode(), input_type="text", inference_params=inference_params)

    output_base64 = model_prediction.outputs[0].data.audio.base64

    with open('audio_file3.wav', 'wb') as f:
        f.write(output_base64)

