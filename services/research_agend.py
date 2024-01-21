import streamlit as st
from metaphor_python import Metaphor
from services import llm

# Initialize the Metaphor API client at the global level
metaphor = Metaphor("f4ca1ab6-2d62-475c-850f-9bbcdb7d281c")

def run_metaphor_search(company_name):
    prompt = f"positive reviews about employees working at {company_name}"
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
    prompt = f"think step-by-step. First extract the most mentioned positive aspects of working at {company_name} from the following text. Then summarize it for a promotion video in a very motivating voice. As an output, only write the voice for the promotion video in 2-3 sentences. here is the text: {full_content_result}"
    summary = llm.llm_multimodal(None,prompt=prompt)
    
    return contents, summary

def show():
    st.markdown("### Research Agend")
    company_name = st.text_input("Company Name", "LabLab.ai")

    if st.button("Start research"):
        st.write("Researching relevant data for  " + company_name)

        # Call the function to run Metaphor search and retrieve extracts
        extracts, summary = run_metaphor_search(company_name)

        for extract in extracts:
            with st.expander("Extracted content"):
                #st.write(extract)
                st.components.v1.html(extract, height=500)   

        st.markdown("### Summary:")
        st.write(summary)

        
      