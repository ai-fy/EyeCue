
# EyeCue - AI Gen for career Videos


This is a streamlit app developed during the GenAI Hackathon at LabLab.ai, using the official Clarifai Python utilities. The Project creates inspirational videos for Social Media to inspire careers - a valuable recruiting tool.  

* Try the EyeCue Module in Clarify at: https://clarifai.com/ai-fy/EyeCue/modules/eye_cue

## Installation

Simply git clone and setup this repo with the requirements.txt file:
```cmd
git clone git@github.com:ai-fy/EyeCue.git
cd EyeCue
pip install -r requirements.txt
```

If the installation failed, it may be necessary to download futher build tools, like "Microsoft C++ Build Tools" (see error messages)


## Getting started

Create a .env file that contains the required tokens: 
PAT = 'your clarifai token'
ELEVENLABS_TOKEN = "a token for elevenlabs" 
You can leave the ELEVENLABS_TOKEN empty, it will fall back to OpenAI voice generation

After installation you just need to run the streamlit app:
```cmd
streamlit run app.py
```

Find your `user_id` [here](https://portal.clarifai.com/settings/profile), `app_id` (of whatever app you  want to interact with in your account), personal access token (`pat`) [here](https://portal.clarifai.com/settings/authentication), and the `base` URL for the API you're calling such as https://api-dev.clarifai.com or http://host:port for a direct Clarifai API stack.

If these links don't work, go to the profile in clarify (round circle), security and click on eye icon to show the access token. Your user_id can be found in the section "Account"

Put them into the following parts of the url below in your browser:
http://localhost:8501?user_id={user_id}&app_id={app_id}&pat={pat}=base={base}

