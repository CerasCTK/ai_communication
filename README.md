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

###  2. Real-time Speech-to-Text (STT)
- Supports real-time, low-latency speech recognition.
- Users can speak naturally and receive instant AI responses.

###  3. OpenAI API Integration
- **GPT-4o** for intelligent, context-aware conversations.
- Ensures high-quality responses and analysis.


## Roadmap

- [x] Real-time Speech-to-Text
- [x] Applying AI
- [ ] Simple UI
- [ ] Code Websocket(django)
- [ ] Grammar & Vocabulary Feedback Feature
- [ ] Personalized Exercises Feature

See the [open issues](https://github.com/CerasCTK/ai_communication/issues) for a full list of proposed features (and known issues).


##  Requirements

### **Hardware Requirement**
Minimum recommended hardware to run the project smoothly
- CPU: Dual-core processor
- RAM: 4GB RAM or more
- Storage: 2GB free disk space
- Microphone: medium quality requirements.
- Camera: medium quality requirements.
- Internet Connection: Stable connection for realtime AI responses

### **System / Tools Needed**
- Python **3.10+**
- Git
- Docker
- OpenAI API Key
- WebSocket
- Speech-to-Text Engine 


## Installation

### 1. Install Docker
Follow the [Docker_Guide](https://docs.docker.com/get-started/get-docker/) to install correctly with the different os.

### 2. Clone the repository
```sh
git clone https://github.com/CerasCTK/ai_communication.git
cd ai_communication
```

### 3. Run via Docker
**Note:** Make sure that[Dockerfile](https://github.com/CerasCTK/ai_communication/blob/main/Dockerfile), [requirements](https://github.com/CerasCTK/ai_communication/blob/main/requirements.txt) and [docker-compose.yml](https://github.com/CerasCTK/ai_communication/blob/main/docker-compose.yml) files has been downloaded. Then:

```sh
docker compose up -d
```

## Commit Convention

We follow the [COMMIT_CONVENTION](./COMMIT_CONVENTION.md) guideline to keep Git history clean and consistent.


## 📄 License


This project is licensed under the MIT License.

See the [LICENSE](./LICENSE) file for details.

---
