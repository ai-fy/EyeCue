import numpy as np
import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS

##########################################################
ClarifaiStreamlitCSS.insert_default_css(st)

st.header("Widgets")
st.title("These are a suite of widgets provided by streamlit")
st.header("It's nice to see them")
st.subheader("But it's nicer to see them in action")
st.markdown("## Markdown")
st.latex(r''' e^{i\pi} + 1 = 0 ''')
st.write("write")
st.text("text")

st.button('Install Module')
st.download_button('Download Button', 'download.csv')
st.checkbox('checkbox')
st.radio('radio', ['option 1', 'option 2'])
st.selectbox('selectbox', ['option 1', 'option 2'])
st.multiselect('multiselect', ['option 1', 'option 2'])
st.slider('slider', 1.0, 5.0)
st.select_slider('select slider', range(5))
st.text_input('text input')
st.number_input('number input')
st.text_area('text area')
st.date_input('date input')
st.time_input('time input')
st.file_uploader('file uploader', type='csv')
# st.camera_input('camera input')
# st.color_picker('color picker')
with st.expander("expander"):
  st.write("here is some text")

st.progress(50, text="progress text")
st.success("success text")
st.info("info text")
st.warning("warning text")
st.error("error text")
st.exception("exception text")

tabs = st.tabs(["tab 1", "tab 2"])

a = np.random.randn(10, 2)
st.dataframe(a)

st.divider()
st.code("print('hello world')")
