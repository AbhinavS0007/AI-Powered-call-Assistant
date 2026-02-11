import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini client with API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_reply(conversation_log, caller_text):
    prompt = f"""
You are Abhinav Sachan’s personal phone assistant.

Rules:
- Speak politely and naturally.
- Keep responses short (1–2 sentences).
- Ask follow-up questions if needed.
- If conversation is complete, end with:
  "Thank you for calling. Goodbye."

Conversation so far:
{chr(10).join(conversation_log)}

Caller just said:
{caller_text}
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text.strip()


def summarize_conversation(conversation_log):
    full_convo = "\n".join(conversation_log)

    prompt = f"""
Summarize this phone conversation in 3–4 lines:

{full_convo}
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text.strip()
