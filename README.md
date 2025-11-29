<h1 align="center"> Communication Learning Assistant</h1>

📌 **A language-learning app that helps users practice speaking and listening anywhere through natural, real-time conversations with AI, providing a personalized and adaptive learning experience.**

---

##  Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Commit-Convention](#commit-convention)
- [License](#-license)



##  Overview
**Ai Communication** leverages AI technology to support multi-language learning through natural, interactive conversations.  
Users can communicate with the AI in **text or voice**, receiving real-time feedback and corrections.  
The system also provides **personalized learning recommendations** based on AI assessments to enhance overall progress.

The goal of this project is to deliver a more natural, engaging, and effective learning experience compared to traditional language-learning applications.



##  Features

###  1. AI Voice Conversation Chatbot
- Engage in real-life conversations through text or voice.
- Supports contextual scenarios (market, airport, restaurant, and more).

###  2. Real-time STT (Julius Integration)
- On-device, low-latency speech recognition using **Julius STT**.
- Users can speak naturally and receive instant AI responses.

###  3. Grammar & Vocabulary Feedback
- Real-time grammar correction.
- Suggestions for more natural and accurate vocabulary usage.

###  4. Personalized Exercises
- Automatically generated exercises based on user proficiency.
- AI adapts to the user’s learning progress over time.

###  5. OpenAI API Integration
- **GPT-4o** for intelligent, context-aware conversations.
- Whisper or streaming STT as additional options.
- Ensures high-quality responses and analysis.



##  Requirements

#### **Hardware Requirement**
Minimum recommended hardware to run the project smoothly
- CPU: Dual-core processor
- RAM: 4GB RAM or more
- Storage: 2GB free disk space
- Microphone: medium quality requirements.
- Camera: medium quality requirements.
- Internet Connection: Stable connection for realtime AI responses

#### **System / Tools Needed**
- Python **3.10+**
- Git
- Docker
- OpenAI API Key
- WebSocket
- STT Engine 


## Installation
#### 1. Clone the repository
```sh
git clone https://github.com/CerasCTK/ai_communication.git
cd ai_communication
```

#### 2. Install dependencies
#### Python dependencies
```sh
pip install -r requirements.txt
```

#### Install WebSocket library
```sh
pip install websockets
```

#### 3. Run via Docker (optional)
```sh
docker compose up -d
```



## Commit Convention

We follow [Conventional Commits](./commit-convention.md) for clean Git history.


## 📄 License


This project is licensed under the MIT License.

See the [LICENSE](./LICENSE) file for details.

---
