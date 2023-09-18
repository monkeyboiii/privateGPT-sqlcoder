from st_pages import add_page_title
from streamlit_timeline import timeline
import streamlit as st


########################################
# Title
add_page_title()
st.write("In this section, I present my work to my supervisior and audience.")


########################################
# Timeline
st.divider()
st.header("⌚️ Timeline")

with open("st-pages/timeline.json", "r") as file:
    data = file.read()
timeline(data)


########################################
# Architecture
st.divider()
st.header("🏗️ Architecture")
st.markdown("In this section, I open [Schema](/Schema) on the sidebar.")


########################################
# Feature
st.divider()
st.header("💥 Features")
st.markdown(
    "In this section, I open [Text-to-SQL Chatbot](/Text-to-SQL) on the sidebar.")
st.subheader("✅ Implemented")
st.markdown(
    """
    1. LLMs and SQL best practices from [2], specifically:
        * Add sample rows;
        * Specify custom table information;
        * Use Query Checker to self-correct invalid SQL using parameter `use_query_checker=True`;
        * Customize the LLM Prompt: include specific instructions or relevant information, using parameter `prompt=CUSTOM_PROMPT`;
        * Get intermediate steps access the SQL statement as well as the final result using parameter `return_intermediate_steps=True`;
        * Limit the number of rows a query will return using parameter `top_k=5`.
                
    2. Coding best practices, specifically:
        * Use :blue[Jupyter Notebooks] for interactiveness and readability, even to non-coders;
        * Leveraged :blue[pydantic] to ensure code quality, easier for future adaptation and integration;
        * Wrote approximately a total of :blue[2k+] lines python code;
        * :blue[Iteratively] improving the logic flow of my implementation, design -> implement -> evaulate -> improve loop.
""")
st.subheader("⛽️ Room for Improvement")
st.markdown(
    """
1. Current implementation limitations, specifically:
    * Model cannot parse longer text, table info, sample rows or chat history might be :red[lost];
    * Model might be :red[unresponsive] under too much questions;
    * :red[Inaccurate] and :red[incorrect] answers are returned;
    * Chinese support may not be ideal.
    * Model may be too :red[large].
    * Interface has :red[no] interaction or evaluation button.
    * Chatbot should support :red[asynchronous] calling.

2. LLMs and SQL improvements from langchain, specifically:
    * Use `ConversationSummaryBufferMemory` or other techniques to summarize chat history;
    * Use :green[distributed] GPU setup;
    * Add `HumanApprovalCallbackhandler` human-in-the-loop tool validation, this suggests using `SQLAgent` to support a wider range of tools;
    * Explore a variety of models to find the most :green[suitable] ones.
    * Add button to :green[interrupt], :green[evaluate] the answer.
    * Implement :green[asynchronous] calling function in langchain framework.
""")


########################################
#  Problems and Solutions
st.divider()
st.header("🛠️ Problems and Solutions")
st.markdown(
    """
    1. No prior exprience to deep learning.
        - Get basic understanding through building practical demo project.
    2. GPU not available on on-premise machine.
        - Use Google Colab to get preliminary results.
    3. Missing dependencies.
        - Conda environment on on-premise machine.
    4. Current components not directly usable.
        - Build an architecture that is modular.
"""
)


########################################
# Questions
st.divider()
st.header("🙋 Questions?")


########################################
# Reference
st.divider()
st.header("📃 Reference")
st.markdown(
    """
    [1] Jeremy Howard, FastAI. (2022). Practical Deep Learning for Coders. [link](https://course.fast.ai/)

    [2] Langchain, MAR 13, 2023. LLMs and SQL. [link](ttps://blog.langchain.dev/llms-and-sql/)
    
    [3] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). React: Synergizing reasoning and acting in language models. [link](https://arxiv.org/abs/2210.03629)
"""
)
