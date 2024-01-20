import streamlit as st
from metaphor_python import Metaphor

# Initialize the Metaphor API client at the global level
metaphor = Metaphor("f4ca1ab6-2d62-475c-850f-9bbcdb7d281c")

def run_metaphor_search(company_name):
    prompt = f"positive reviews about employees working at {company_name}"
    response = metaphor.search(prompt, num_results=3, include_domains=["comparably.com"], type="keyword")
    st.write(f"received {len(response.results)} entries")

    contents = []
    for result in response.results:
        st.write("now checking for: "+str(result.id))
        content = metaphor.get_contents(result.id)
        content = content.contents
        contents.append(content)
    
    return contents

def show():
    st.markdown("### Research Agend")
    company_name = st.text_input("Company Name", "LabLab.ai")

    if st.button("Start research"):
        st.write("Researching relevant data for  " + company_name)

        # Call the function to run Metaphor search and retrieve extracts
        extracts = run_metaphor_search(company_name)

        for extract in extracts:
            st.write(extract)
        
      