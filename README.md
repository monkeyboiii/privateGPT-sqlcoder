# privateGPT-sqlcoder

The source code is hosted on [github](https://github.com/monkeyboiii/privateGPT-sqlcoder). This is a work developed at ZOFUND under the supervision of Mr. Shoubo Sheng. It's a fork from [privateGPT](https://github.com/imartinez/privateGPT), which has [sqlcoder](https://huggingface.co/defog/sqlcoder) integrated with the help of [langchain](https://github.com/langchain-ai/langchain), to enable text-to-sql generation.

## Usage

Install dependencies"

```shell
# conda environment recommended
pip install -r requirements.txt
```

Define necessary environment variables:

```bash
# Copy `example.env` file to `.env`
cp example.env .env
```

Use example data

```shell
# enter misc directory
cd misc

# format questions
python format_question.py

# populate sqlite database
python insert.py

# return to project level
cd ..
```

Build embedding vector store:

```python
python ingest.py [--help]
```

Run the app:

```python
# Streamlit interface (recommended)
streamlit run app.py

# Text-to-sql model cli
python privateGPT.py [--help]
```

## Stats

```bash
# .ipynb LoC
jq '.cells[] | select(.cell_type == "code") .source[]' **/*.ipynb | wc -l

# .py Loc
git ls-files | grep -i "\.py$" | xargs wc -l
```
