# 🎙️ Voice-Activated AI Customer Support Agent

A full-stack, voice-enabled AI assistant capable of handling real-time customer queries, tracking order status, and managing context-aware conversations.

Built with **Rasa Open Source**, **Python**, and **Speech Recognition APIs**, this project demonstrates a decoupled microservices architecture simulating a modern SaaS customer care interface.

---

## 🚀 Key Features

* **🗣️ Bidirectional Voice Interface:**
    * **Speech-to-Text (STT):** Captures user audio via microphone using Google Speech Recognition.
    * **Text-to-Speech (TTS):** Generates real-time audio responses using gTTS (Google Text-to-Speech).
* **🧠 Advanced NLU (Natural Language Understanding):**
    * Detects intents (e.g., `ask_order_status`, `escalate_to_human`) from natural speech.
    * Extracts entities (e.g., Order IDs) automatically.
* **📦 Context Management (Rasa Forms):**
    * Uses slot-filling logic to handle missing information (e.g., asking for an Order ID if the user forgets it).
    * Maintains conversation context across multiple turns.
* **🔌 Backend Integration:**
    * Decoupled Action Server handles business logic.
    * Simulates database queries to retrieve dynamic order statuses.
    * Easily extensible to SQL/NoSQL databases (MongoDB ready).

---

## 🛠️ Tech Stack

* **Core Framework:** Rasa Open Source 3.x
* **Language:** Python 3.10
* **Voice Pipeline:**
    * `SpeechRecognition` (Input)
    * `gTTS` (Output)
    * `PyAudio` & `Pygame` (Audio Processing)
* **API Framework:** Sanic (Async Web Server)

---

## 📂 Project Structure

```text
VOICE_ADVISOR_PROJECT/
│
├── 📂 actions/             # Python business logic (The "Muscle")
├── 📂 channels/            # Custom Voice Input/Output Connectors
├── 📂 data/                # NLU training data & rules (The "Brain")
├── 📂 models/              # Trained AI models
├── 📂 scripts/             # Utility scripts (e.g., Database seeding)
│
├── 📄 config.yml           # AI pipeline configuration
├── 📄 credentials.yml      # Connector settings
├── 📄 domain.yml           # Intent & Response registry
├── 📄 endpoints.yml        # Action Server connection config
├── 📄 run_server.py        # Main entry point for the Rasa Core server
├── 📄 run_client.py        # Client-side script for Microphone/Speaker interaction
└── 📄 README.md            # Project Documentation


