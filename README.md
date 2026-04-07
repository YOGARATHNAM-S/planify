# 🤖 Planify - AI Workspace Assistant

An intelligent AI-powered unified workspace that automates tasks, organizes notes, and manages your calendar using modern Google AI capabilities.

## 🚀 Features

* 💬 **Natural Language Workflow** - Talk to your tasks, notes, and calendar
* ⚡ **Fast API** - High-performance backend using FastAPI
* ☁️ **Cloud Native** - Ready for seamless deployment on Google Cloud Run
* 🔗 **Modular Architecture** - Agent-based design using Google ADK and MCP tools
* 🧠 **AI Orchestration** - Powered by Google Gemini for intelligent tool selection
* 📦 **Triple Productivity** - Tasks, Notes, and Calendar events in one system

## 🛠️ Tech Stack

* Python 3.11+
* FastAPI & Uvicorn
* Google ADK (Agent Development Kit)
* Gemini 1.5 Flash
* Google Cloud Datastore
* Pydantic
* MCP (Model Context Protocol)



## 📂 Project Structure

```
.
├── agent.py               # Main application and ADK AI agents
├── api_endpoints.py       # REST API defining endpoints
├── models.py             # Pydantic data validation models
├── requirements.txt      # Project dependencies
├── test_functionality.py # Comprehensive test suite
├── .env                  # Environment variables
└── README.md             # Documentation
```

## ⚙️ Installation

```bash
git clone https://github.com/YOGARATHNAM-S/planify.git
cd planify/Planify
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file in the `Planify` folder:

```env
MODEL=gemini-1.5-flash
PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
PORT=8080
```

## ▶️ Run Locally

```bash
uvicorn agent:app --reload --port 8080
```

Open `http://localhost:8080/docs` to see the interactive Swagger UI API documentation.

## ☁️ Deploy to Cloud Run

```bash
# Build and deploy easily via Google Cloud Run
gcloud run deploy planify \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "MODEL=gemini-1.5-flash,PROJECT_ID=your-project-id"
```

## 📌 Usage

You can use Planify in two ways:

1. **REST API**: Directly interact with tasks, notes, and calendar endpoints via `/api/v1/`
2. **AI Chat**: Send a natural language prompt to `/api/v1/workspace/chat`
   * *Example:* `{"prompt": "Create a high priority task to review code by Friday and set up a meeting for 2 PM."}`

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

MIT License

---

⭐ If you like this project, please give it a star on GitHub!

```bash
uvx --from google-adk==1.14.0 \
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --service_name=ai-assistant \
  --with_ui \
  . \
  -- \
  --service-account=$SERVICE_ACCOUNT
```

## 🔐 Environment Variables

Create `.env` file:

```
PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path-to-key.json
```

## 📌 Usage

* Start server
* Open provided URL
* Chat with AI assistant

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

## 📄 License

MIT License

---

⭐ If you like this project, give it a star!
