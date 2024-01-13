![Clarifai logo](https://www.clarifai.com/hs-fs/hubfs/logo/Clarifai/clarifai-740x150.png?width=240)

# Clarifai App Module Gallery


This is a test streamlit app with  the official Clarifai Python utilities. This repo includes higher level convencience classes, functions, and scripts to make using our [API](https://docs.clarifai.com) easier. This is built on top of the [Clarifai Python gRPC Client](https://github.com/Clarifai/clarifai-python-grpc).

* Try the Clarifai demo at: https://clarifai.com/demo
* Sign up for a free account at: https://clarifai.com/signup
* Read the documentation at: https://docs.clarifai.com/

## Installation

Simply git clone and setup this repo with the requirements.txt file:
```cmd
git clone git@github.com:Clarifai/module-gallery.git
cd module-gallery
pip install -r requirements.txt
```

If the installation failed, it may be necessary to download futher build tools, like "Microsoft C++ Build Tools" (see error messages)

## Versioning

This library doesn't use semantic versioning. The first two version numbers (`X.Y` out of `X.Y.Z`) follow the API (backend) versioning, and
whenever the API gets updated, this library follows it.

The third version number (`Z` out of `X.Y.Z`) is used by this library for any independent releases of library-specific improvements and bug fixes.

## Getting started

After installation you just need to run the streamlit app:
```cmd
streamlit run app.py
```

Find your `user_id` [here](https://portal.clarifai.com/settings/profile), `app_id` (of whatever app you  want to interact with in your account), personal access token (`pat`) [here](https://portal.clarifai.com/settings/authentication), and the `base` URL for the API you're calling such as https://api-dev.clarifai.com or http://host:port for a direct Clarifai API stack.

If these links don't work, go to the profile in clarify (round circle), security and click on eye icon to show the access token. Your user_id can be found in the section "Account"

Put them into the following parts of the url below in your browser:
http://localhost:8501?user_id={user_id}&app_id={app_id}&pat={pat}=base={base}


### Building Single Page Apps
For a single page app all you need to implement is the app.py file. You're of course free to import any other python modules you build but they will all be used to render that single page. A single page app will still let `page=N` come in as a query param but it will be ignored.

### Building Multi-Page Apps
This is now natively supported in streamlit since version 1.10.0. See https://docs.streamlit.io/library/get-started/multipage-apps for more details.

Note we add the following to `.streamlit/config.toml` so that the sidebar does not show by default:
```
[ui]
hideSidebarNav=true
```

## Using Clarifai CSS Styles

This is done via the .streamlit/config.toml file which sets the primaryColor to Clarifai blue "#356dff".

For more advanced css you can add a style.css file to the top level of the repo and load it in streamlit with:
```
def local_css(file_name):
  with open(file_name) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("style.css")
```

The way it works is it should be loaded (see `local_css`) at the top of your streamlit `app.py` in order to inject the styles into the rendered html page. Eventually we plan to fully host this style file and load it remotely from that url so that it's always the most up to date style file.

### If you've already created an app

You an copy the style.css file from this repo into your repo and then add the following code snippet to get the styles loaded on render:
```python
def local_css(file_name):
  with open(file_name) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("style.css")
```
