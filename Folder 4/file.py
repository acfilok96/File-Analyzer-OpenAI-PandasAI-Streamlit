import os,time
import openai
import streamlit as st
import pandas as pd
from pandasai.llm import OpenAI
from pandasai import PandasAI

# Header Name [Working...]
st.title("File Analyzer 2.2")

# OpenAI Connection... [Working...]
openai.api_key = st.secrets["OPENAI_API_KEY"]
llm = OpenAI(api_token=openai.api_key)
pandas_ai = PandasAI(llm)

# Side Bar [Working...]
file_input = None
with st.sidebar.header("Option"):
    # Upload CSV File
    file_input = st.file_uploader("Upload files for analysis", type=["csv","xlsx"], accept_multiple_files=True)

###########################################################
    
if file_input:
    st.success('Successfully uploaded!', icon="✅")
    
    # Make a list files
    if "files" not in st.session_state:
        st.session_state.files = []
    
    # Load CSV file [Working...]
    data_file =[]
    for files in file_input:
        data_file_temp = pd.read_csv(files)
        st.write(files.name)
        st.write(data_file_temp.head(3))
        data_file.append(data_file_temp)
        
    # Make a list of dictionary, namely 'messages'
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # To continue the loop of conversation
    for message in st.session_state.messages:
        with st.chat_message(message["question"]):
            st.markdown(message["answer"])

    # Run the live conversation
    # Enter prompt
    if prompt := st.chat_input("Ask me about data..."):
            
        # Append the 'prompt' as a 'user'
        st.session_state.messages.append({"question":"user","answer":prompt})
        
        # Show user's prompt
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Show assistant's response
        response_temp = ""
        with st.chat_message("assistant"):
            # Pick one random string
            with st.spinner("Generating response..."):
                response = pandas_ai.run(data_file, prompt=prompt)
                response_temp = response
                st.write(response)
        
        # Append the 'response' as a 'assistant'
        st.session_state.messages.append({"question":"assistant", "answer":response_temp})