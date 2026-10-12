
from google import genai
from config import GOOGLE_API_KEY

if not GOOGLE_API_KEY:
    raise ValueError(
        "Google API key is missing. Check your .env file."
    )

client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"


def get_ai_response(message, history=None):
    history = history or []

    conversation = []

    for item in history[-10:]:
        role = "User" if item["role"] == "user" else "Assistant"
        conversation.append(f"{role}: {item['content']}")

    conversation.append(f"User: {message}")

    prompt = (
        "You are a friendly and helpful AI personal assistant. "
        "Answer clearly and simply. Remember the conversation "
        "provided below when answering the latest question.\n\n"
        + "\n".join(conversation)
        + "\nAssistant:"
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        return "Sorry, I couldn't generate a response. Please try again."

    return response.text