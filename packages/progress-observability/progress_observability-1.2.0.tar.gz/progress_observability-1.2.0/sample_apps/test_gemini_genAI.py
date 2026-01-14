import os
from dotenv import load_dotenv
from progress.observability import Observability
from google import genai

load_dotenv()

def instrument_observability(app_name: str | None = None) -> None:
	api_key = os.environ.get("OBSERVABILITY_API_KEY")
	endpoint = os.environ.get("OBSERVABILITY_ENDPOINT")
	app_id = os.environ.get("APP_ID", "default")

	Observability.instrument(
		app_name=app_name or f"ai-gemini-python-example-{app_id}",
		endpoint=endpoint,
		api_key=api_key,
	)

def build_gemini_client():
	api_key = os.environ.get("GEMINI_API_KEY")
	return genai.Client(api_key=api_key)

def run_gemini_demo(question: str = "What is the capital of France?") -> str:

	instrument_observability()
	client = build_gemini_client()

	response = client.models.generate_content(
		model="gemini-2.5-flash",
		contents=question,
	)

	text = getattr(response, "text", None) or str(response)
	print(f"Question: {question}")
	print(f"Answer: {text}")
	return text

if __name__ == "__main__":
	# Allow running this file directly as a tiny sample app
	run_gemini_demo()


