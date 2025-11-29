<h1 align="center"> Communication Learning Assistant</h1>

📌 **A language-learning app that helps users practice speaking and listening anywhere through natural, real-time conversations with AI, providing a personalized and adaptive learning experience.**

---

##  Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Commit-Convention](#commit-convention)
- [License](#license)
- [Team-Members](#team-members)



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

#### **System / Tools Needed**
- Python **3.10+**
- Git
- Docker (optional)
- OpenAI API Key
- WebSocket support for real-time STT
- Julius STT Engine (for local speech recognition)

#### **Environment Variables**
Create a `.env` file at the project root:

Sample initialization:
Open-AI key
```sh
OPENAI_API_KEY=your_api_key_here
BASE_URL=https://aiportalapi.stu-platform.live/jpe
client = openai.OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)
```



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

#### Install Julius (Speech-to-Text Engine)

Ubuntu:

```sh
sudo apt install julius
```

macOS:
```sh
brew install julius
```

Windows:

Download from Julius official website and add to PATH.

#### Install WebSocket library
```sh
pip install websockets
```

#### 3. Run via Docker (optional)
```sh
docker compose up -d
```



## 📝 Commit Convention

This project follows the Conventional Commits standard.

Short commit
```sh
git commit -m "Add comment here"
```
Long commit format
```sh
<type>[Compoent]: <short description>

[optional body]

[optional footer]
```

Commit Types

| **Type**             | **Meaning**                                                      |
| -------------------- | ---------------------------------------------------------------- |
| **bug**              | Something isn't working                                          |
| **documentation**    | Improvements or additions to documentation                       |
| **duplicate**        | This issue or pull request already exists                        |
| **enhancement**      | New feature or request                                           |
| **good first issue** | Good for newcomers                                               |
| **help wanted**      | Extra attention is needed                                        |
| **invalid**          | This doesn't seem right                                          |
| **question**         | Further information is requested                                 |
| **study**            | For issues related to research or learning before implementation |
| **wontfix**          | This will not be worked on                                       |

Compoent Types

| **Compoent:** **Julius**, **Websocket**, **etc**         |
| -------------------- |



## 📄 License


This project is licensed under the MIT License.

You are free to use, modify, and distribute the project under its terms.



##  Team Members
| Name          | Role                           |
| ------------- | ------------------------------ |
| **KhaiCT1**   | Leader – AI Engineer / Backend |
| **HaoNV35**   | Frontend Engineer              |
| **DuyLM10**   | Frontend Engineer              |
| **KienNT167** | Backend Engineer               |
| **AnhPD54**   | Backend Engineer               |

---
