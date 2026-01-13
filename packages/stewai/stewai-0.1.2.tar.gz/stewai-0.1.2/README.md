# stewai (Python SDK)

Base URL (only): `https://api.stewai.com/v1`

## Install

```bash
pip install stewai
```

## Get an API key

1. Log in to `stewai.com`
2. Go to `Settings → API keys`
3. Create a key and copy it once (`sk-live-...`)

## Usage

```python
from stewai import Client

client = Client(api_key="sk-live-...")

# Use the Input step “API input id” shown in the editor as the inputs key
run = client.runs.create(
    recipe_id="01K....",
    inputs={"USERQUESTION": "What should I focus on this week?"},
)

print(run["status"])  # done|failed|cancelled|blocked

# Debug only: full execution trace (steps + outputs)
trace = client.runs.steps(run["id"])
```

## Ingest sources (URLs + Pantry docs)

```python
from stewai import Client, IngestSource

client = Client(api_key="sk-live-...")

run = client.runs.create(
    recipe_id="01K....",
    ingest={
        "ingest_1": [
            IngestSource(uri="https://example.com/docs", kind="url"),
        ]
    },
)
```

## Upload + resolve Pantry paths

```python
from stewai import Client, IngestSource

client = Client(api_key="sk-live-...")

upload = client.storage.upload("./report.pdf")
run = client.runs.create(
    recipe_id="01K....",
    ingest={"ingest_1": [upload.to_ingest_source(label="Q4 Report")]},
)

resolved = client.storage.resolve_path("Reports/Q4.pdf")
if resolved:
    client.runs.create(
        recipe_id="01K....",
        ingest={"ingest_1": [resolved.to_ingest_source()]},
    )
```

## Environment variable

```bash
export STEWAI_API_KEY="sk-live-..."
```

```python
from stewai import Client

client = Client()  # reads STEWAI_API_KEY
run = client.runs.create(recipe_id="01K....", wait=False)
run = client.runs.wait(run["id"], timeout=300)
```
