import os
import openai
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandasai
from pandasai.llm import OpenAI
from pandasai import PandasAI

# Header Name [Working...]
st.title("File Analyzer...")

# OpenAI Connection... [Working...]
openai.api_key = st.secrets["OPENAI_API_KEY"]
llm = OpenAI(api_token=openai.api_key)
pandas_ai = PandasAI(llm)

# Upload CSV File
file_input = st.file_uploader("Upload a file for analysis", type=["csv","xlsx"], accept_multiple_files=True)

# In process [Working...]
if file_input:
    # Load CSV file [Working...]
    data_file =[]
    for files in file_input:
        data_file_temp = pd.read_csv(files)
        st.write(files.name)
        st.write(data_file_temp.head(3))
        data_file.append(data_file_temp)
      
    # Enter Prompt  
    prompt = st.text_area("Enter here . . .")

    # Generate Response
    if st.button("Generate"):    
        if prompt :
            with st.spinner("Generating response..."):
                response = pandas_ai.run(data_file, prompt=prompt)
                st.write(response)
        else:
            st.write("Enter prompt...")

