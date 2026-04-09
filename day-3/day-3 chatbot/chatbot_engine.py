from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5-20251001"

def user_message(context: list, text):
    message = {"role": "user", "content": text}
    context.append(message)

def assistant_message(context: list, text):
    message = {"role": "assistant", "content": text}
    context.append(message)

def chat(context: list, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": context
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
