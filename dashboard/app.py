import streamlit as st
import requests

st.title("OnboardAI")

question = st.text_input("Ask a question")

if st.button("Submit"):
    response = requests.get(
        f"http://127.0.0.1:8000/chat?question={question}"
    )

    st.write(response.json()["answer"])