from huggingface_hub import InferenceClient
import os

client = InferenceClient(token=os.getenv("HF_TOKEN"))


def summarize_text(text):
    response = client.summarization(
    text,
    model="facebook/bart-large-cnn"
)
    return response["summary_text"]
