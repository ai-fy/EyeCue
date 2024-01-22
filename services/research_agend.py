import streamlit as st
from metaphor_python import Metaphor
from services import llm



def run_metaphor_search(company_name,metaphor_token):
    prompt = f"positive reviews about employees working at {company_name}"
    # Initialize the Metaphor API client at the global level
    metaphor = Metaphor(metaphor_token)
    response = metaphor.search(prompt, num_results=3, include_domains=["glassdoor.com"], type="keyword")
    st.write(f"received {len(response.results)} entries")

    # with st.expander("Metaphor API response complete"):
    #     st.components.v1.html(response.text, height=500)

    contents = []
    for result in response.results:
        st.write(f"now checking for: {result.title} at {result.url}")
        content = metaphor.get_contents(result.id)
        content = content.contents
        contents.append(content[0].extract)
    
    full_content_result = " ".join(contents)
    prompt = f"think step-by-step. First extract the most mentioned positive aspects of working at {company_name} from the following text. Then summarize just the facts. As an output, only write the fact summary in 3-5 sentences without mentioning names. here is the text: {full_content_result}"
    summary = llm.llm_multimodal(None,prompt=prompt)
    
    return contents, summary

def show(metaphor_token):
    st.markdown("### Rate images with vision for selection in video")
      # # ------------------ Testing Image Curation ------------------------ #
    uploaded_file = st.file_uploader("Choose a file to let it be rated by the AI for selection in the video")
    if uploaded_file is not None:
        # To read file as bytes:
        file_bytes = uploaded_file.getvalue()
        #st.write(file_bytes)
        prompt = "Is there at least one clear face of person on this image? Is it a photography? How positive on a scale from 1-10 will this image be perceived? On a scale from 1-10, would your recommend to use it in an image video for recruiting? Use JSON as an output format with attributes is_person, positivity_rating, is_photography"
        text = llm.llm_multimodal(file_bytes, prompt)
        st.markdown(text)

    st.divider()

    st.markdown("### Research company reviews with Metaphor API")
    company_name = st.text_input("Company Name", "LabLab.ai")

    if st.button("Start research"):
        st.write("Researching relevant data for  " + company_name)

        # Call the function to run Metaphor search and retrieve extracts
        extracts, summary = run_metaphor_search(company_name,metaphor_token)

        for extract in extracts:
            with st.expander("Extracted content"):
                #st.write(extract)
                st.components.v1.html(extract, height=500)   

        st.markdown("### Summary:")
        st.write(summary)

        

        
      