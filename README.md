# privateGPT-sqlcoder

A fork from privateGPT, integrated with sqlcoder, enabling text-to-sql generation.

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
