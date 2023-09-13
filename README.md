# privateGPT-sqlcoder

A fork from [privateGPT](https://github.com/imartinez/privateGPT), integrated with [sqlcoder](https://huggingface.co/defog/sqlcoder), enabling text-to-sql generation.

## Usage

Define necessary environment variables:

```bash
# Copy `example.env` file to `.env`
cp example.env .env
```

Build embedding vector store:

```python
python ingest.py [--help]
```

Run text-to-sql model:

```python
python privateGPT.py [--help]
```

## Stats

```bash
# .ipynb LoC
jq '.cells[] | select(.cell_type == "code") .source[]' **/*.ipynb | wc -l

# .py Loc
git ls-files | grep -i "\.py$" | xargs wc -l
```
