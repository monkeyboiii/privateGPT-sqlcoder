import streamlit as st

with open("st-pages/example.md", "r") as md:
    content = md.read()

st.markdown(content)
