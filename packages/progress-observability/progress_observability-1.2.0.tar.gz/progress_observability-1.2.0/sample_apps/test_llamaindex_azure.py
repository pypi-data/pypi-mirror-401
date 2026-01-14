import os

from dotenv import load_dotenv

from progress.observability import Observability
from llama_index.llms.azure_openai import AzureOpenAI


QUESTION = "What is the capital of Portugal?"


def instrument_observability() -> None:
    load_dotenv()

    endpoint = os.getenv("OBSERVABILITY_ENDPOINT")
    api_key = os.getenv("OBSERVABILITY_API_KEY")
    app_id = os.getenv("APP_ID", "local")

    Observability.instrument(
        app_name=f"llamaindex-azure-python-example-{app_id}",
        endpoint=endpoint,
        api_key=api_key,
    )


def build_llm() -> AzureOpenAI:
    # Prefer AZURE_OPENAI_* variables if provided, otherwise fall back to AZURE_API_*
    api_key = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("AZURE_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") or os.getenv("AZURE_API_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION") or os.getenv("AZURE_API_VERSION")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") or "gpt-4o-mini"

    return AzureOpenAI(
        engine=deployment,
        model=deployment,
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )


def run_llamaindex_azure_demo(question: str = QUESTION) -> str:
    instrument_observability()

    llm = build_llm()

    print(f"Question: {question}")

    response = llm.complete(question)

    answer = str(response)
    print(f"Answer: {answer}")
    return answer


if __name__ == "__main__":
    run_llamaindex_azure_demo()
