import streamlit as st
from metaphor_python import Metaphor

# Initialize the Metaphor API client at the global level
metaphor = Metaphor("f4ca1ab6-2d62-475c-850f-9bbcdb7d281c")

def run_metaphor_search(company_name):
    prompt = f"positive reviews about employees working at {company_name}"
    response = metaphor.search(prompt, num_results=3, include_domains=["comparably.com"], type="keyword")

    # Access the three Metaphor IDs
    id1 = response.results[0].id
    id2 = response.results[1].id
    id3 = response.results[2].id

    # Get individual responses
    response1 = metaphor.get_contents(id1)
    response2 = metaphor.get_contents(id2)
    response3 = metaphor.get_contents(id3)

    # Extract the relevant text
    extract1 = response1.contents
    extract2 = response2.contents
    extract3 = response3.contents

    return extract1, extract2, extract3

def show():
    st.markdown("### Research Agenda for EyeCue")
    company_name = st.text_input("Company Name", "LabLab.ai")

    if st.button("Start research"):
        st.write("Researching relevant data for  " + company_name)

        # Call the function to run Metaphor search and retrieve extracts
        #extracts = run_metaphor_search(company_name)

        # Now you can use the extracts globally
        #st.write("Extract for Company 1:")
        #st.write(extracts[0])

        #st.write("Extract for Company 2:")
        #st.write(extracts[1])

        #st.write("Extract for Company 3:")
        #st.write(extracts[2])
