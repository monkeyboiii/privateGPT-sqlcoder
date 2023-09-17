"""Generated and modified from notebooks/SQLBasedChains.ipynb"""
from typing import Any, Dict, Optional, Union
from functools import partial
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, root_validator

from langchain.memory import ConversationBufferMemory
from langchain.chains.llm import LLMChain
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.schema.output_parser import StrOutputParser
from langchain.chains.sql_database.prompt import _sqlite_prompt, _mysql_prompt, _postgres_prompt
from langchain.schema import format_document, BaseRetriever
from langchain.schema.prompt_template import BasePromptTemplate
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import HuggingFaceEmbeddings
import chromadb
from langchain.vectorstores import Chroma
from chromadb.config import Settings
from langchain.llms import GPT4All
from SQLCoder import SQLCoder
from pprint import pprint


load_dotenv()


# Embedding
embedding_model = os.environ.get(
    "EMBEDDING_MODEL_NAME", "uer/sbert-base-chinese-nli")
persist_directory = os.environ.get("PERSIST_DIRECTORY", "vectorstore/")
score_threshold = float(os.environ.get("SCORE_THRESHOLD", "0.8"))
retriever_top_k = int(os.environ.get("RETRIEVER_TOP_K", "3"))

# Database
include_tables = os.environ.get(
    "DATABASE_INCLUDE_TABLES", 'fact_retention_model').strip(",").strip()
db_uri = os.environ.get("DATABASE_URI", "sqlite:///db/retention-sqlite.db")

# LLM
model_type = os.environ.get(
    "MODEL_TYPE", "GPT4All")
model_path = os.environ.get(
    "MODEL_PATH", "models/ggml-model-gpt4all-falcon-q4_0.bin")

# SQLDatabaseChatbot
qaq_pairs = {}
_specific_question_and_query_file = os.environ.get(
    "QUESTION_QUERY_PAIR", "downloads/retention/question_query.json"
)
with open(_specific_question_and_query_file, 'r') as file:
    qaq_pairs = json.load(file)
return_sql_only = os.environ.get("RETURN_SQL_ONLY", "false").lower() == "true"
return_intermediate_steps = os.environ.get(
    "RETURN_INTERMEDIATE_STEPS", "false").lower() == "true"
return_direct = os.environ.get("RETURN_DIRECT", "false").lower() == "true"
use_query_checker = os.environ.get(
    "USE_QUERY_CHECKER", "false").lower() == "true"
query_top_k = int(os.environ.get("QUERY_TOP_K", "3"))
chatbot_verbosity = os.environ.get(
    "CHATBOT_VERBOSITY", "false").lower() == "true"


def format_pairs(pairs: dict, question: str) -> Union[str, None]:
    if question is not None and question in pairs.keys():
        return f"Example inquiry: {question}\nCorresponding response: {pairs[question]}"
    else:
        print(f"[!] No such key as {question} in retrieving process")
        return None


def stuff_combine_docs(
    retriever: BaseRetriever,
    question: str,
    mappings: Optional[dict] = None,
    document_prompt: BasePromptTemplate = PromptTemplate(
        input_variables=["page_content"], template="{page_content}"),
    document_separator: str = "\n\n",
    prompt: BasePromptTemplate = PromptTemplate(
        input_variables=["context"], template="{context}"),
    document_variable_name: str = "context",  # laceholder name where  docs fills
    verbose: bool = False,
    **kwargs: Any,  # any more input_variables in prompt
) -> str:
    docs = retriever.get_relevant_documents(question)
    if len(docs) == 0:
        return ""

    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    doc_strings = doc_strings if mappings is None else list(
        map(partial(format_pairs, mappings), doc_strings))
    doc_strings = list(filter(lambda s: s is not None, doc_strings))

    inputs = {
        k: v
        for k, v in kwargs.items()
        if k in prompt.input_variables
    }
    inputs[document_variable_name] = document_separator.join(
        doc_strings)

    formatted = prompt.format(**inputs)
    if verbose:
        print("[*] The combined docs:```\nformatted\n```")
    return formatted


SQL_PROMPT_PRFIX = {
    # "crate": _cratedb_prompt,
    # "duckdb": _duckdb_prompt,
    # "googlesql": _googlesql_prompt,
    # "mssql": _mssql_prompt,
    "mysql": _mysql_prompt,
    # "mariadb": _mariadb_prompt,
    # "oracle": _oracle_prompt,
    "postgresql": _postgres_prompt,
    "sqlite": _sqlite_prompt,
    # "clickhouse": _clickhouse_prompt,
    # "prestodb": _prestodb_prompt,
}


def get_custom_template(db: SQLDatabase):
    _prompt_suffix = """Only use the following tables:
{table_info}

{few_shot_examples}Relevant pieces of previous conversation:
{history}
(You do not need to use these pieces of information if not relevant)

Question: {input}"""

    return PromptTemplate(
        input_variables=["input", "table_info",
                         "top_k", "few_shot_examples", "history"],
        template=SQL_PROMPT_PRFIX[db.dialect] + _prompt_suffix,
    )


class RetrievalLLMChainWithMemory(LLMChain):

    retriever: BaseRetriever
    _word: str = "\nSQLQuery:"  # Stop word apppended to input by SQLDatabaseChain

    def prep_inputs(self, inputs: Dict[str, Any] | Any) -> Dict[str, str]:
        """Mainly overrides history addded to memory"""
        if not isinstance(inputs, dict):
            _input_keys = set(self.input_keys)
            if self.memory is not None:
                _input_keys = _input_keys.difference(
                    self.memory.memory_variables)
            if len(_input_keys) != 1:
                raise ValueError(
                    f"A single string input was passed in, but this chain expects "
                    f"multiple inputs ({_input_keys}). When a chain expects "
                    f"multiple inputs, please call it by passing in a dictionary, "
                    "eg `chain({'foo': 1, 'bar': 2})`"
                )
            inputs = {list(_input_keys)[0]: inputs}

        external_context = self.memory.load_memory_variables(
            inputs) if self.memory is not None else {"history": []}
        inputs = dict(inputs, **external_context)
        inputs["few_shot_examples"] = stuff_combine_docs(
            retriever=self.retriever,
            question=inputs["input"].strip().strip(self._word),
            mappings=qaq_pairs,
            prompt=PromptTemplate(
                input_variables=["context"],
                template="""Some examples of SQL queries response that correspond to human inquiry are listed below:\n{context}\n\n""")
        )
        if self.verbose:
            print("[*] The prepped input:")
            pprint(inputs)
        self._validate_inputs(inputs)
        return inputs

    def prep_outputs(
        self,
        inputs: Dict[str, str],
        outputs: Dict[str, str],
        return_only_outputs: bool = False,
    ) -> Dict[str, str]:
        """Mainly handles \\nSQLQuery added into input text"""
        self._validate_outputs(outputs)
        inputs["input"] = inputs["input"].strip().strip(self._word)
        # FIXME:
        # when outputs are not generated correctly,
        # they fill up bad memory.
        # Maybe use summary memory?
        if self.memory is not None:
            self.memory.save_context(inputs, outputs)
        if self.verbose:
            print("[*] The prepped output:")
            pprint(outputs)
        if return_only_outputs:
            return outputs
        else:
            return {**inputs, **outputs}


class DatabaseChatbot(BaseModel):
    sqlDatabaseChain: SQLDatabaseChain
    verbose: Optional[bool] = False

    @root_validator(pre=True)
    def validate_chain(cls, values):
        _verbosity = values.get("verbose", chatbot_verbosity)

        # retriever args
        CHROMA_SETTINGS = Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        )
        embeddings = HuggingFaceEmbeddings(
            model_name=values.get("embedding_model", embedding_model))
        chroma_client = chromadb.PersistentClient(
            settings=CHROMA_SETTINGS,
            path=values.get("persist_directory", persist_directory)
        )
        vectordb = Chroma(
            persist_directory=values.get(
                "persist_directory", persist_directory),
            embedding_function=embeddings,
            client_settings=CHROMA_SETTINGS,
            client=chroma_client
        )

        # Threshold retriever
        retriever = vectordb.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": values.get("retriever_top_k", retriever_top_k),
                "score_threshold": values.get("score_threshold", score_threshold)
            }
        )

        # Database
        db = SQLDatabase.from_uri(
            db_uri,
            include_tables=include_tables.split(","),
            sample_rows_in_table_info=2)

        # Large language model (LLM)
        llm = None
        llm_model_type = values.get("model_type", model_type)
        if llm_model_type == "GPT4All":
            llm = GPT4All(
                model=values.get("model_path", model_path),
                max_tokens=2048,
                backend='gptj',
                n_batch=8,
                # callbacks=[StreamingStdOutCallbackHandler()],
                # verbose=True
            )
        elif llm_model_type == "SQLCoder":
            llm = SQLCoder(
                model=values.get("model_path", model_path),
                verbosity=_verbosity)
        else:
            raise ValueError(f"Not implemented model type {llm_model_type}")

        # SQLDatabaseChain args
        SQLDatabaseChain_kwargs = {
            # Will return sql-command directly without executing it
            "return_sql": values.get("return_sql_only", return_sql_only),
            # Whether or not to return the intermediate steps along with the final answer.
            "return_intermediate_steps": values.get("return_intermediate_steps", return_intermediate_steps),
            # Whether or not to return the result of querying the SQL table directly.
            "return_direct": values.get("return_direct", return_direct),
            # Whether or not the query checker tool should be used to attempt to fix the initial SQL from the LLM.
            "use_query_checker": values.get("use_query_checker", use_query_checker),
            # The prompt template that should be used by the query checker
            "query_checker_prompt": None,
            "top_k": values.get("query_top_k", query_top_k),
        }
        memory = ConversationBufferMemory(
            input_key='input', memory_key="history")
        custom_prompt_for_llm = get_custom_template(db)

        # SQLDatabaseChain
        values["sqlDatabaseChain"] = SQLDatabaseChain(
            llm_chain=RetrievalLLMChainWithMemory(
                llm=llm,
                retriever=retriever,
                memory=memory,
                prompt=custom_prompt_for_llm,
                callbacks=[StreamingStdOutCallbackHandler()] if _verbosity else [
                ],
                verbose=_verbosity,
            ),
            database=db,
            **SQLDatabaseChain_kwargs
        )

        return values

    def __call__(self, inputs):
        return self.sqlDatabaseChain(inputs)

    def get_history(self):
        history_dict = self.sqlDatabaseChain.llm_chain.memory.load_memory_variables({
        })
        if self.verbose:
            print("[*] The current history:")
            pprint(history_dict)
        return history_dict


def main():
    chatbot = DatabaseChatbot()

    result1 = chatbot({"query": "查询上月末产品类型为投顾类基金保有规模和人数"})
    pprint(result1)

    result2 = chatbot({"query": "这其中招商银行的保有规模是多少"})
    pprint(result2)

    # print("[*] The current history:")
    # pprint(chatbot.get_history())


if __name__ == "__main__":
    main()
