"""Inspiration from https://github.com/cefege/seo-chat-bot/blob/master/streamlit_app.py"""
from st_pages import add_page_title
import streamlit as st
from DatabaseChatbot import DatabaseChatbot


def hide_streamlit_header_footer():
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)


def display_existing_messages():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help?"}]
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def add_user_message_to_session(prompt):
    if prompt:
        st.session_state["messages"].append(
            {"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)


@st.cache_resource
def load_chatbot():
    return DatabaseChatbot()


def generate_assistant_response(chatbot, query):
    full_response = ""
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        conversation = {}
        with st.spinner('Generating response...'):
            # blocking
            conversation = chatbot({"query": query.strip()})

        full_response = conversation.get(
            "result", "Sorry, something is wrong.")
        message_placeholder.write(full_response)

        st.session_state["messages"].append(
            {"role": "assistant", "content": full_response}
        )

    return full_response


def main():
    # static
    add_page_title()
    hide_streamlit_header_footer()
    chatbot = load_chatbot()  # cached, load once, automatic spinner
    display_existing_messages()  # dynamic
    question = st.chat_input("Ask any question for text-to-sql")

    # dynamic
    # NOTE:
    # More intuitive and async frontend can/should be implemented in JS
    # Don't do premature improvements
    if question:
        add_user_message_to_session(question)
        response = generate_assistant_response(chatbot, question)


if __name__ == "__main__":
    main()
