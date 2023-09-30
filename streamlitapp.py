import streamlit as st
from utils import run_conversation

if 'type'               not in st.session_state   : st.session_state.type = ''
if 'language'           not in st.session_state   : st.session_state.language = ''
if 'status'             not in st.session_state   : st.session_state.status = False
if 'traits'             not in st.session_state   : st.session_state.traits = None
if 't_status'           not in st.session_state   : st.session_state.t_status = False

st.set_page_config(layout="wide")

def change():
    st.session_state.status = True

st.title('Developer Personal Assistant (Finds Documentation, Extracts data from open Internet, Iterate over databases)')

if st.session_state.t_status == False:
    st.subheader("Optional: Before moving forward, could you please describe about yourself and what kind of language and tone you use to make your experience better")
    st.session_state.traits = st.text_area("Tell me about yourself and what kind of language (speech, programming language, etc) sand tone you use to make your experience better")

    if st.button('Submit Traits'):
        st.session_state.t_status = True
        st.experimental_rerun()

query = st.text_area('Got any query or thoughts bothering you?', 'Example: Provide me the code for implementing agents using LangChain documentation in python programming language')

if st.button('Submit'):
    change()
    results = run_conversation(query)
    
    if st.session_state.type == 'data':
        st.subheader(f"Your Query: {query}\n")
        st.subheader(f"Result:\n{results}")
    
    elif st.session_state.type == 'doc':
        if st.session_state.language != 'None':
            st.code(results, language=st.session_state.language, line_numbers=True)
        else:
            st.code(results, language='bash', line_numbers=True)
    
if st.session_state.status == False:
    st.write('Press Button to start exploring')