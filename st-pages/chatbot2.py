"""Inspiration from https://github.com/cefege/seo-chat-bot/blob/master/streamlit_app.py"""

from st_pages import add_page_title
import streamlit as st
from concurrent.futures import ThreadPoolExecutor
import signal
from time import sleep
from pprint import pprint
from DatabaseChatbot import DatabaseChatbot


AWAIT_INPUT = "AWAIT_INPUT"
AWAIT_RESPONSE = "AWAIT_RESPONSE"
CANCEL_TASK = "CANCEL_TASK"
if "chat_state" not in st.session_state.to_dict():
    st.session_state["chat_state"] = AWAIT_INPUT
CURRENT_CHAT_STATE = st.session_state["chat_state"]
cancel_botton = None


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


@st.cache_resource
def load_executor():
    return ThreadPoolExecutor()


def task(chatbot, query):
    """chatbot tasks that can be cancelled through interruption"""
    return chatbot({"query": query.strip()})


def dummy_task(name="default"):
    for _ in range(20):
        print(f"[+] In progress on {name}")
        sleep(1)
    return {"result": "Dummy success"}


def interrupt_handler(signum, frame):
    print(f'[*] Handling signal {signum} ({signal.Signals(signum).name}).')


def generate_assistant_response(chatbot, query):
    full_response = ""
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # TODO: add streaming support
        # for response in openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     temperature=0,
        #     messages=[
        #         {"role": "system", "content": primer},
        #         {"role": "user", "content": augmented_query},
        #     ],
        #     stream=True,
        # ):
        #     full_response += response.choices[0].delta.get("content", "")
        #     message_placeholder.markdown(full_response + "▌")
        conversation = {}
        executor = load_executor()
        with st.spinner('Generating response...'):
            # future = executor.submit(task, chatbot, query)
            print(f"[*] Received question {query}")
            dummy_future = executor.submit(dummy_task, query)
            print("[*] Task sumbitted to executor")
            if st.button("Cancel"):
                print("[!] Cancel button true, cancel through future.cancel()")
                dummy_future.cancel()
            else:
                print("[*] Not cancelled")

            print("[*] Waiting on future...")
            conversation = dummy_future.result()

        print("[*] Returned conversation:")
        pprint(conversation)
        full_response = conversation.get(
            "result", "Sorry, something is wrong.")
        message_placeholder.markdown(full_response)

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
    if CURRENT_CHAT_STATE == CANCEL_TASK:
        pass
    elif question:
        add_user_message_to_session(question)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            cancel_button = st.button("Cancel")

            response = generate_assistant_response(chatbot, question)
            CURRENT_CHAT_STATE = AWAIT_RESPONSE

            full_response = conversation.get(
                "result", "Sorry, something is wrong.")
            message_placeholder.markdown(full_response)

            st.session_state["messages"].append(
                {"role": "assistant", "content": full_response}
            )

    print(f"[🚨] Loading finished with {question}")


if __name__ == "__main__":
    main()
