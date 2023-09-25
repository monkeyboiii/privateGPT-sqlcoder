from st_pages import add_page_title
from streamlit_timeline import timeline
import streamlit as st


########################################
# Title
add_page_title()
st.write("在本节中，我向我的导师和观众进行展示。")


########################################
# Timeline
st.divider()
st.header("⌚️ 时间轴")

with open("st-pages/timeline-cn.json", "r") as file:
    data = file.read()
timeline(data)


########################################
# Architecture
st.divider()
st.header("🏗️ 架构")
st.markdown("在本节中，我在侧边栏上打开 [Schema](/Schema)。")


########################################
# Feature
st.divider()
st.header("💥 功能")
st.markdown(
    "在本节中，我在侧边栏上打开 [Text-to-SQL Chatbot](/Text-to-SQL)。")
st.subheader("✅ 已实现")
st.markdown(
    """
    1. LLM 和 SQL 最佳实践来自 [2]，具体来说：
         * 添加样本行
         * 指定自定义表格信息
         * 使用查询检查器通过参数`use_query_checker=True`自我纠正无效的SQL
         * 自定义LLM提示：包含具体说明或相关信息，使用参数`prompt=CUSTOM_PROMPT`
         * 使用参数`return_intermediate_steps=True`获取中间步骤访问SQL语句以及最终结果
         * 使用参数`top_k=3`限制查询返回的行数。
                
     2. 编码最佳实践，具体来说：
         * 使用 :blue[Jupyter Notebooks] 实现交互性和可读性，甚至对于非编码人员也是如此
         * 利用:blue[pydantic]保证代码质量，更方便以后的适配和集成
         * 总共编写了大约 :blue[2k+] 行 python 代码
         * :blue[迭代]改进我的实现的逻辑流程，设计 -> 实现 -> 评估 -> 改进循环。
""")
st.subheader("⛽️ 提升空间")
st.markdown(
    """
    1. 当前的实施限制，具体来说：
        * 模型无法解析较长的文本，表格信息、示例行或聊天历史记录可能:red[丢失]
        * 问题太多时，模型可能会显示:red[无响应]
        * 返回:red[不准确]或:red[不正确]答案
        * 中文支持可能不太理想
        * 模型可能太:red[大]
        * 界面:red[无]交互或评估按钮。
        * 聊天机器人应支持:red[异步]调用。

     2. langchain 的 大语言模型LLM 和 SQL 改进，具体来说：
        * 使用 `ConversationSummaryBufferMemory` 或其他技术来总结聊天记录
        * 使用:green[分布式] GPU 设置
        * 添加 `HumanApprovalCallbackhandler` 人机交互工具验证，这建议使用 `SQLAgent` 支持更广泛的工具
        * 探索多种模型，找到最:green[合适]的模型
        * 添加按钮:green[中断], :green[评估]答案
        * 实现langchain框架中的:green[异步]调用功能。
""")


# ########################################
# #  Problems and Solutions
# st.divider()
# st.header("🛠️ Problems and Solutions")
# st.markdown(
#     """
#     1. No prior exprience to deep learning.
#         - Get basic understanding through building practical demo project.
#     2. GPU not available on on-premise machine.
#         - Use Google Colab to get preliminary results.
#     3. Missing dependencies.
#         - Conda environment on on-premise machine.
#     4. Current components not directly usable.
#         - Build an architecture that is modular.
# """
# )


# ########################################
# # Questions
# st.divider()
# st.header("🙋 Questions?")


########################################
# Reference
st.divider()
st.header("📃 参考")
st.markdown(
    """
    [1] Jeremy Howard, FastAI. (2022). Practical Deep Learning for Coders. [link](https://course.fast.ai/)

    [2] Langchain, MAR 13, 2023. LLMs and SQL. [link](ttps://blog.langchain.dev/llms-and-sql/)
    
    [3] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). React: Synergizing reasoning and acting in language models. [link](https://arxiv.org/abs/2210.03629)

    [4] Ken Van Haren. Jan 18, 2023. Replacing a SQL analyst with 26 recursive GPT prompts. [link](https://www.patterns.app/blog/2023/01/18/crunchbot-sql-analyst-gpt/?ref=blog.langchain.dev)
"""
)
