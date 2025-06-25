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

![WhatsApp Image 2025-06-25 at 09 39 38_8cd6ee08](https://github.com/user-attachments/assets/48809a9c-1726-4e85-b699-6f4b12fcf037)
![WhatsApp Image 2025-06-25 at 09 39 54_15bca12a](https://github.com/user-attachments/assets/cae0a38f-d288-4f34-a9ba-ef0d4f8ad52f)

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

