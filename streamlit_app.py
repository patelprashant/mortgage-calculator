import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.write("I am writing new code with streamlit")
name = st.text_input("Are you enjoying Mr.?")
st.write(f"Here we go... Mr. {name} is enjoying streamlit..whoo..hoo!!")