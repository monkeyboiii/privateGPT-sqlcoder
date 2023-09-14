import streamlit as st

with open("README.md", "r") as md:
    content = md.read()

st.markdown(content)
