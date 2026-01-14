## Python sample apps

This directory contains example Python applications that demonstrate how to use the Progress Observability SDK with:

- Azure OpenAI + LangChain (`test_azure_langchain.py`)
- Google GenAI Gemini (`test_gemini_genAI.py`)
- Azure OpenAI + LlamaIndex (`test_llamaindex_azure.py`)
- Google GenAI Gemini + LlamaIndex (`test_llamaindex_gemini.py`)

## Prerequisites

- Python (use the version defined in `pyproject.toml`)
- [uv](https://github.com/astral-sh/uv) installed locally
- Access to:
	- Azure OpenAI (for the Azure example)
	- Google GenAI (for the Gemini example)

## 1. Build the SDK and prepare the sample apps

From the repo root:

```bash
cd Progress.Observability.Instrumentation
bash build-python-instrumentation.sh
```

This will:

- build the Progress Observability Python SDK (`uv build`)
- copy the latest `.whl` file into `sample_apps/`
- update `sample_apps/pyproject.toml` to point to the latest wheel
- install dependencies in `sample_apps` (`uv sync`)

After this step you can run the samples from the `sample_apps` directory.

## 2. Configure environment variables (`.env`)

In the `sample_apps/` directory:

1. Use `.env.example` as a template (if present) or create a `.env` file manually.
2. Set the following variables as needed.

Minimum for the Azure LangChain sample:

```env
AZURE_API_KEY=...
AZURE_API_ENDPOINT=...
AZURE_API_VERSION=...
OBSERVABILITY_ENDPOINT=...
OBSERVABILITY_API_KEY=...
APP_ID=local-azure
```

Minimum for the Gemini sample:

```env
GEMINI_API_KEY=...
OBSERVABILITY_ENDPOINT=...
OBSERVABILITY_API_KEY=...
APP_ID=local-gemini
```

You can reuse the same `OBSERVABILITY_*` values for both samples.

Minimum for the Azure LlamaIndex sample (same Azure OpenAI settings as LangChain):

```env
AZURE_API_KEY=...
AZURE_API_ENDPOINT=...
AZURE_API_VERSION=...
OBSERVABILITY_ENDPOINT=...
OBSERVABILITY_API_KEY=...
APP_ID=local-llamaindex-azure
```

Minimum for the Gemini LlamaIndex sample (same Gemini settings as the basic sample):

```env
GEMINI_API_KEY=...
OBSERVABILITY_ENDPOINT=...
OBSERVABILITY_API_KEY=...
APP_ID=local-llamaindex-gemini
```

You can reuse the same `OBSERVABILITY_*` values and provider keys across all samples; only `APP_ID` needs to differ if you want to see separate applications in the UI.

## 3. Run only the Azure LangChain sample

From the repo root:

```bash
cd Progress.Observability.Instrumentation
bash run-sample-azure.sh
```

This will:

- change into `sample_apps/`
- run `uv run python test_azure_langchain.py`

## 4. Run only the Gemini (Google GenAI) sample

From the repo root:

```bash
cd Progress.Observability.Instrumentation
bash run-sample-gemini.sh
```

This will:

- change into `sample_apps/`
- run `uv run python test_gemini_genAI.py`

## 5. Run only the Azure LlamaIndex sample

From the repo root:

```bash
cd Progress.Observability.Instrumentation
bash run-sample-llamaindex-azure.sh
```

This will:

- change into `sample_apps/`
- run `uv run python test_llamaindex_azure.py`

## 6. Run only the Gemini LlamaIndex sample

From the repo root:

```bash
cd Progress.Observability.Instrumentation
bash run-sample-llamaindex-gemini.sh
```

This will:

- change into `sample_apps/`
- run `uv run python test_llamaindex_gemini.py`

## 7. Run scripts directly from `sample_apps` (optional)

If you have already run `bash build-python-instrumentation.sh` at least once and dependencies are installed, you can run the scripts directly:

```bash
cd Progress.Observability.Instrumentation/sample_apps

# Azure LangChain
uv run python test_azure_langchain.py

# Gemini
uv run python test_gemini_genAI.py
```
