import requests
import streamlit as st
#import os
#import openai

BASE_URL = "http://localhost:8080/api/"

@st.cache(show_spinner=False)
def get_topic(cluster_text: str) -> str:

    # openai.api_key = os.getenv("OPENAI_API_KEY")

    # response = openai.Completion.create(
    # engine="text-davinci-001",
    # prompt=f"""{cluster_text} \n\nSummarize the topic of the cluster. Use as few words as possible:\n\nThis cluster is about""",
    # temperature=0.7,
    # max_tokens=22,
    # top_p=1,
    # frequency_penalty=0,
    # presence_penalty=0
    # )

    return "This cluster is about ..."
