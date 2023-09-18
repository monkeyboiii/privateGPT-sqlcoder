"""Split the original question-query pair SQL file to questions only and question-query json file.
Before running, modify SQL text file by appending a r'\d+、'
"""
import os
import re
import json


directory_write = "retention/question"
full_sql_text_file = "retention/sql.txt"
obj_dump_file = "retention/question_query.json"


pattern = r"\d+、(.+?)(?=\d+、)"  # regex lookahead
qaqs = {}


def extract_text(file_path, qaq_pattern):
    try:
        with open(file_path, 'r') as sql_file:
            content = sql_file.read()

        qaqs_str = re.findall(qaq_pattern, content, re.DOTALL)
        for i, qaq in enumerate(qaqs_str):
            question = qaq.split("\n", 1)[0].strip()
            query = qaq.split("\n", 1)[1]
            query = " ".join(query.split()) + ";"
            # print(i, question, query, sep="\n")

            with open(os.path.join(os.path.join(directory_write, f"sql-{str(i)}.txt")), "w+") as file:
                file.write(question)
            print(f'question and query {i} proccessed')

            qaqs[question] = query

    except Exception as e:
        print(f'Error prcessing {file_path}: {e}')


def main():
    if not os.path.exists(directory_write):
        os.makedirs(directory_write)

    extract_text(full_sql_text_file, pattern)

    with open(obj_dump_file, 'w+', encoding='utf-8') as write_file:
        json.dump(qaqs, write_file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
