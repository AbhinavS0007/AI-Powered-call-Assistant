from fastapi import FastAPI, Request
from fastapi.responses import Response
import requests
import os
from dotenv import load_dotenv
import whisper
from google import genai

from twilio.rest import Client as TwilioClient


# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Load Whisper model once
whisper_model = whisper.load_model("base")

# Setup Gemini client
client = genai.Client()

# Twilio WhatsApp client
twilio_client = TwilioClient(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

# Store conversation in memory
conversation_log = []



@app.get("/")
def home():
    return {"message": "AI assistant running"}


# Incoming call handler
@app.api_route("/incoming-call", methods=["GET", "POST"])
async def incoming_call():
    response = """
    <Response>
        <Say>Hello, this is Abhinav's AI assistant.How can I help you?</Say>
        <Record action="/process-recording" maxLength="20" />
    </Response>
    """
    return Response(content=response, media_type="application/xml")


# Process recording
@app.api_route("/process-recording", methods=["GET", "POST"])
async def process_recording(request: Request):
    form_data = await request.form()
    recording_url = form_data.get("RecordingUrl")

    print("Recording URL:", recording_url)

    # Download audio with Twilio authentication
    audio_file = requests.get(
        recording_url + ".wav",
        auth=(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
    )

    with open("call.wav", "wb") as f:
        f.write(audio_file.content)

    # Transcribe with Whisper
    result = whisper_model.transcribe("call.wav")
    caller_text = result["text"]

    print("Caller said:", caller_text)

    # Generate AI reply using Gemini (new SDK)
    prompt = f"""
    You are Abhinav Sachan’s personal phone assistant.

    Rules:
    - Speak politely and naturally like a human.
    - Keep responses short (1–2 sentences).
    - Always ask a follow-up question to continue the conversation.
    - Try to understand the purpose of the call.

    Caller said: {caller_text}
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    ai_reply = response.text.strip()

    print("AI reply:", ai_reply)

    # Return voice response
    twiml = f"""
<Response>
    <Say>{ai_reply}</Say>
    <Record action="/process-recording" maxLength="20" />
</Response>
    """

    return Response(content=twiml, media_type="application/xml")
