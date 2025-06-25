from flask import Flask, render_template, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from twilio.rest import Client
import datetime
import os
import base64
from io import BytesIO
from gtts import gTTS
import re
import json

app = Flask(__name__)

# 🔐 CONFIG
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
YOUR_CALENDAR_ID = "milisha058@gmail.com"  # Replace with your actual calendar ID

# ✅ GOOGLE SERVICE ACCOUNT AUTH via ENVIRONMENT VARIABLE
service_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
if not service_json:
    raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_JSON env variable")

info = json.loads(service_json)
creds = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/calendar"]
)
calendar_service = build("calendar", "v3", credentials=creds)

# 📞 INIT
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# 🧠 Dummy LLM
def query_gemma(prompt):
    return prompt  # Replace with real LLM logic if needed

# 🔊 TTS
def speak(text):
    tts = gTTS(text)
    buf = BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# 📅 Calendar Extraction
def extract_datetime_and_title(text):
    pattern = r"(?:set\s*)?(?:(\d{1,2})\s*(am|pm))?\s*(?:appointment|event|meeting|doctor)?\s*(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        hour, ampm, day, month, year = match.groups()
        hour = int(hour) if hour else 9
        if ampm:
            if ampm.lower() == "pm" and hour != 12:
                hour += 12
            elif ampm.lower() == "am" and hour == 12:
                hour = 0
        try:
            dt = datetime.datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
        except:
            return None, None
        dt = dt.replace(hour=hour, minute=0)
        return dt.isoformat(), "Doctor Appointment"
    return None, None

def set_calendar_event(title, dt_iso):
    event = {
        "summary": title,
        "start": {"dateTime": dt_iso, "timeZone": "Asia/Kolkata"},
        "end": {
            "dateTime": (datetime.datetime.fromisoformat(dt_iso) + datetime.timedelta(hours=1)).isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }
    created_event = calendar_service.events().insert(calendarId=YOUR_CALENDAR_ID, body=event).execute()
    return created_event.get("htmlLink")

# 📩 SMS
def send_message_via_twilio(to, message):
    try:
        twilio_client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=to)
        return f"📩 Message sent to {to}: \"{message}\""
    except Exception as e:
        return f"❌ Message failed: {e}"

# 📞 Call
def make_call_via_twilio(to_number, message_to_say):
    try:
        twiml = f"<Response><Say voice='alice'>{message_to_say}</Say></Response>"
        twilio_client.calls.create(twiml=twiml, to=to_number, from_=TWILIO_PHONE_NUMBER)
        return f"📞 Calling {to_number} and saying: \"{message_to_say}\""
    except Exception as e:
        return f"❌ Call failed: {e}"

# 🤖 Multitask Parser
def parse_and_execute(instruction):
    response = ""
    tasks = [t.strip() for t in re.split(r'\band\b|\n|,', instruction, flags=re.IGNORECASE) if t.strip()]

    for task in tasks:
        if not task:
            continue

        # 🔍 Search
        search_match = re.search(r'find providers for (.+)', task, re.IGNORECASE)
        if search_match:
            query = search_match.group(1).strip()
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            response += f"🔍 Found providers for '{query}': {url}\n"
            continue

        # 💬 Message
        msg_match = re.search(r'message.*?(\+\d{10,15})\D+that (.+)', task, re.IGNORECASE)
        if msg_match:
            number = msg_match.group(1)
            message = msg_match.group(2).strip().capitalize()
            response += send_message_via_twilio(number, message) + "\n"
            continue

        # 📞 Call
        call_match = re.search(r'call.*?(\+\d{10,15})\D+that (.+)', task, re.IGNORECASE)
        if call_match:
            number = call_match.group(1)
            message = call_match.group(2).strip().capitalize()
            response += make_call_via_twilio(number, message) + "\n"
            continue

        # 📅 Calendar
        dt, title = extract_datetime_and_title(task)
        if dt and title:
            link = set_calendar_event(title, dt)
            response += f"📅 Calendar event '{title}' created.\nView: {link}\n"
            continue

        # ⚠️ Fallback
        response += f"⚠️ Didn't understand: \"{task}\"\n"

    return response.strip()

# 🌐 ROUTES
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chatbot.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")
    ai_response = query_gemma("Break this into tasks and answer: " + question)
    action_response = parse_and_execute(question)
    final_response = ai_response + "\n\n" + action_response
    audio = speak(final_response)
    return jsonify({"answer": final_response, "audio": audio})

# 🚀 START
if __name__ == "__main__":
    app.run(debug=True, port=5500)
