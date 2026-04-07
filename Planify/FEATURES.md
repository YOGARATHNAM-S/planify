# 📋 Planify - Task, Notes & Calendar Management

An intelligent AI Assistant workspace with integrated task management, note-taking, and calendar features built on FastAPI and Google Cloud.

## 🚀 Features

### ✅ **Task Management**
- Create tasks with priority levels (Low, Medium, High)
- Set due dates for tasks
- Mark tasks as complete
- Update task details
- List tasks with completion status
- Track task priority and due dates

### 📝 **Notes Management**
- Create notes with categories for organization
- Store detailed note content
- Categorize notes (General, Personal, Work, etc.)
- List and search notes by category
- Delete notes when no longer needed

### 📅 **Calendar Management**
- Create calendar events with date, time, location, and description
- View upcoming events for the next N days
- Delete events
- Track event timing and locations
- Get event descriptions for context

### 🤖 **AI-Powered Assistant**
- Natural language conversation interface
- Agent-based workflow orchestration
- Automatic tool selection for user requests
- Integration with Google ADK for intelligent processing

## 🛠️ Tech Stack

- **Backend**: FastAPI + Uvicorn
- **Database**: Google Cloud Datastore
- **AI/ML**: Google ADK (Agents), Langchain
- **Logging**: Google Cloud Logging
- **Language**: Python 3.x
- **Deployment**: Google Cloud Run

## 📂 Project Structure

```
Planify/
├── agent.py                 # Main FastAPI app & AI agents
├── api_endpoints.py         # REST API endpoints
├── models.py               # Pydantic data models
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── .env                    # Environment variables
└── .vscode/               # VS Code configuration
```

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- Google Cloud Project with Datastore enabled
- Google Cloud credentials (service account key)

### Steps

1. **Clone the repository**
```bash
git clone <repo-url>
cd Planify
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Google Cloud**
```bash
# Set your Google Cloud project
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

5. **Configure environment**
Create a `.env` file:
```env
MODEL=gemini-1.5-flash
GOOGLE_CLOUD_PROJECT=your-project-id
PORT=8080
```

## ▶️ Run Locally

```bash
uvicorn agent:app --reload --port 8080
```

The API will be available at `http://localhost:8080`

## 📡 API Endpoints

### Base URL
```
http://localhost:8080/api/v1
```

### Task Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | List all tasks |
| PUT | `/tasks/{task_id}` | Update a task |
| PATCH | `/tasks/{task_id}/complete` | Mark task as complete |
| DELETE | `/tasks/{task_id}` | Delete a task |

**Create Task Example:**
```bash
curl -X POST http://localhost:8080/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project report",
    "priority": "High",
    "due_date": "2024-12-31",
    "description": "Finish quarterly report"
  }'
```

### Note Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes` | Create a new note |
| GET | `/notes` | List all notes |
| PUT | `/notes/{note_id}` | Update a note |
| DELETE | `/notes/{note_id}` | Delete a note |

**Create Note Example:**
```bash
curl -X POST http://localhost:8080/api/v1/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Project Ideas",
    "content": "Consider implementing real-time collaboration features",
    "category": "Work"
  }'
```

### Calendar Event Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/events` | Create a new event |
| GET | `/events` | List upcoming events |
| DELETE | `/events/{event_id}` | Delete an event |

**Create Event Example:**
```bash
curl -X POST http://localhost:8080/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "date": "2024-12-20",
    "time": "14:00",
    "location": "Conference Room A",
    "description": "Quarterly planning session"
  }'
```

### Summary Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/summary` | Get workspace summary |

## 🤖 AI Chat Interface

### Endpoint
```
POST /api/v1/workspace/chat
```

### Request Format
```json
{
  "prompt": "Add a task to buy groceries on Friday"
}
```

### Example Usage
```bash
curl -X POST http://localhost:8080/api/v1/workspace/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a meeting note: Q4 planning session at 2 PM in Conference Room"
  }'
```

## 🎯 AI Agent Tools

The workspace agent has access to the following tools:

- `add_task()` - Create a new task
- `list_tasks()` - View all tasks
- `complete_task()` - Mark task as done
- `update_task()` - Modify task details
- `add_note()` - Create a note
- `list_notes()` - View all notes
- `delete_note()` - Remove a note
- `add_event()` - Create calendar event
- `list_events()` - View upcoming events
- `delete_event()` - Remove an event
- `get_summary()` - Get workspace overview

The AI agent intelligently selects and uses these tools based on your natural language requests.

## 📝 Data Models

### Task
```python
{
  "id": 123,
  "title": "Complete project",
  "completed": false,
  "priority": "High",           # Low, Medium, High
  "due_date": "2024-12-31",
  "description": "Optional",
  "created_at": "2024-01-01T10:00:00"
}
```

### Note
```python
{
  "id": 456,
  "title": "Meeting notes",
  "content": "Discussed Q4 objectives...",
  "category": "Work",           # General, Personal, Work, etc.
  "created_at": "2024-01-01T10:00:00"
}
```

### Calendar Event
```python
{
  "id": 789,
  "title": "Team Meeting",
  "date": "2024-12-20",
  "time": "14:00",
  "location": "Conference Room A",
  "description": "Quarterly planning",
  "created_at": "2024-01-01T10:00:00"
}
```

## ☁️ Deploy to Google Cloud Run

### Build Docker Image
```bash
docker build -t gcr.io/YOUR-PROJECT/planify:latest .
docker push gcr.io/YOUR-PROJECT/planify:latest
```

### Deploy to Cloud Run
```bash
gcloud run deploy planify \
  --image gcr.io/YOUR-PROJECT/planify:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars MODEL=gemini-1.5-flash
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL` | Gemini model to use | `gemini-1.5-flash` |
| `PORT` | Server port | `8080` |
| `GOOGLE_CLOUD_PROJECT` | GCP project ID | Required |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to service account key | Required |

## 📚 Example Workflows

### Example 1: Add Task via AI
```
User: "Remind me to call clients tomorrow at 10 AM"
AI: Uses add_task tool → Creates task with tomorrow's date
Response: "Task created: Call clients (Priority: Medium, Due: Tomorrow)"
```

### Example 2: Create Note via AI
```
User: "Take a note: Research competitors for Q1 strategy"
AI: Uses add_note tool with category "Work"
Response: "Note saved: Research competitors"
```

### Example 3: Add Calendar Event
```
User: "Schedule a meeting with the team on Friday at 2 PM"
AI: Uses add_event tool → Creates calendar event
Response: "Calendar event created: Team meeting - Friday 2:00 PM"
```

## 🐛 Troubleshooting

### Database Connection Issues
- Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to a valid service account key
- Verify your Google Cloud project has Datastore enabled
- Check that the service account has Datastore permissions

### Model API Issues
- Verify `MODEL` env variable matches an available Gemini model
- Check Google Cloud AI API is enabled
- Confirm API quotas are not exceeded

### Port Already in Use
```bash
# Use a different port
uvicorn agent:app --reload --port 8081
```

## 📦 Adding New Features

### Add a New Tool
1. Define a function decorated with `@mcp.tool()`
2. Add it to the `workspace_agent` tools list
3. Document the tool in this README

### Add New API Endpoints
1. Add endpoint to `api_endpoints.py`
2. Include the router in `agent.py`
3. Update the models in `models.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use this project

## 📞 Support

For issues and questions, please create an issue in the repository.

---

**Built with ❤️ for productivity and organization**
