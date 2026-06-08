import streamlit as st
import requests

st.set_page_config(
    page_title="OnboardAI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 OnboardAI")
st.write("Ask company policy questions")

question = st.text_input("Enter your question")

if st.button("Submit"):
    response = requests.get(
        f"http://127.0.0.1:8000/chat?question={question}"
    )

    st.success(response.json()["answer"])