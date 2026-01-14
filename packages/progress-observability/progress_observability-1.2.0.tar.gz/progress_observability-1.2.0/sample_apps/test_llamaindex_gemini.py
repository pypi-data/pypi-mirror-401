import os

from dotenv import load_dotenv

from progress.observability import Observability
from llama_index.llms.google_genai import GoogleGenAI


QUESTION = "What is the capital of Greece?"


def instrument_observability() -> None:
    load_dotenv()

    endpoint = os.getenv("OBSERVABILITY_ENDPOINT")
    api_key = os.getenv("OBSERVABILITY_API_KEY")
    app_id = os.getenv("APP_ID", "local")

    Observability.instrument(
        app_name=f"llamaindex-gemini-python-example-{app_id}",
        endpoint=endpoint,
        api_key=api_key,
    )


def build_llm() -> GoogleGenAI:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY must be set")

    return GoogleGenAI(
        model="gemini-2.5-flash",
        api_key=api_key,
    )


def run_llamaindex_gemini_demo(question: str = QUESTION) -> str:
    instrument_observability()

    llm = build_llm()

    print(f"Question: {question}")

    # Direct LLM call via the LlamaIndex GoogleGenAI adapter, no VectorStoreIndex/embeddings
    response = llm.complete(question)

    answer = str(response)
    print(f"Answer: {answer}")
    return answer


if __name__ == "__main__":
    run_llamaindex_gemini_demo()
