## 🧠 About the Project

**Multiसाथी** is an AI-powered multitasking assistant that helps users perform daily tasks such as:
- Making voice calls
- Sending messages
- Adding events to Google Calendar
- Chatting with an AI in English
- Receiving voice/audio responses

With a sleek animated UI, particle backgrounds, and avatar integration, it brings productivity and fun together!

---

## 🎥 Demo Preview


## 🚀 Features

- 🎤 Voice input with automatic LLM-based parsing
- 💬 Chat-like responses powered by AI (Gemma 2B/Ollama)
- 🔊 Audio output using gTTS (Google TTS)
- 📞 Call & SMS using Twilio API
- 📅 Google Calendar event creation
- 🌐 English support as of now 
- 👧 Avatar 

---

## 🛠️ Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Frontend    | HTML, CSS, JavaScript             |
| Backend     | Python, Flask                     |
| AI Model    | Gemma 2B via Ollama               |
| APIs Used   | Google Calendar API, Twilio       |
| Voice       | Web Speech API (STT), gTTS (TTS)  |

---
**🧠 Flow Diagram**
mermaid
Copy
Edit
graph TD
A[User Voice/Text Input] --> B[LLM Parsing (Gemma/Ollama)]
B --> C{Task Type?}
C -->|Call/SMS| D[Twilio API]
C -->|Calendar| E[Google Calendar API]
C -->|General| F[LLM Answer]
F --> G[Text + Audio Response]

**📈 Future Enhancements**
⏰ Auto-reschedule events using AI

🌍 Multilingual translation support

🧠 Chat memory & conversation history

📊 Dashboard for daily tasks


**🤝 Contribution Guide**
We welcome contributions from everyone!
To contribute:

Fork the repository

Create a new branch: git checkout -b feature-name

Commit your changes: git commit -m "Add feature"

Push to the branch: git push origin feature-name

Create a Pull Request

