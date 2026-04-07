# 🚀 Quick Start Guide - Planify

## 5-Minute Setup

### 1. Prerequisites
```bash
# Ensure you have Python 3.8+ and git
python --version
git --version
```

### 2. Clone & Setup
```bash
git clone <repo-url> && cd Planify
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. Configure Google Cloud
```bash
# Set environment variables
export GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json
export GOOGLE_CLOUD_PROJECT=your-project-id
```

### 4. Run
```bash
uvicorn agent:app --reload
# Visit: http://localhost:8080/docs (Swagger UI)
```

---

## 🎯 Common Tasks

### Add a Task
**Via REST API:**
```bash
curl -X POST http://localhost:8080/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "priority": "Medium"}'
```

**Via AI Chat:**
```bash
curl -X POST http://localhost:8080/api/v1/workspace/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Add a task: Buy groceries this weekend"}'
```

### Create a Note
**Via REST API:**
```bash
curl -X POST http://localhost:8080/api/v1/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Meeting", "content": "Q4 planning", "category": "Work"}'
```

**Via AI Chat:**
```bash
curl -X POST http://localhost:8080/api/v1/workspace/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Note: Team meeting on Friday at 2 PM"}'
```

### Schedule an Event
**Via REST API:**
```bash
curl -X POST http://localhost:8080/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Standup",
    "date": "2024-12-20",
    "time": "10:00",
    "location": "Zoom",
    "description": "Daily sync"
  }'
```

**Via AI Chat:**
```bash
curl -X POST http://localhost:8080/api/v1/workspace/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Schedule a team standup tomorrow at 10 AM on Zoom"}'
```

---

## 📊 View Your Workspace

### Get Summary
```bash
curl http://localhost:8080/api/v1/summary
```

Response:
```json
{
  "status": "success",
  "summary": {
    "active_tasks": 5,
    "completed_tasks": 3,
    "total_notes": 12,
    "total_events": 2
  }
}
```

### List All Tasks
```bash
curl http://localhost:8080/api/v1/tasks
```

### List All Notes
```bash
curl http://localhost:8080/api/v1/notes
```

### List Upcoming Events (next 7 days)
```bash
curl "http://localhost:8080/api/v1/events?days_ahead=7"
```

---

## 🤖 AI Agent Examples

The AI agent understands natural language. Try these:

```
"Create a task to finish the report by Friday"
"Add a note about the meeting outcomes"
"Schedule the team meeting for tomorrow at 2 PM"
"Show me my pending tasks"
"List events for the next 2 weeks"
"Create a note in the Work category about the project deadline"
"Mark task 123 as done"
```

---

## 🧪 Test with Swagger UI

1. Open http://localhost:8080/docs
2. Try any endpoint with the interactive UI
3. All parameters and responses are documented

---

## 📁 File Organization

| File | Purpose |
|------|---------|
| `agent.py` | Main FastAPI app, AI agents, core tools |
| `api_endpoints.py` | REST API routes for all features |
| `models.py` | Pydantic data validation models |
| `requirements.txt` | Python dependencies |
| `FEATURES.md` | Complete feature documentation |

---

## 🔍 Debug & Logs

### Enable Verbose Logging
```bash
export LOGLEVEL=DEBUG
uvicorn agent:app --reload --log-level debug
```

### Check Datastore
```bash
# Via Google Cloud Console
gcloud datastore query --kind Task
gcloud datastore query --kind Note
gcloud datastore query --kind CalendarEvent
```

---

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| `No Datastore` | Enable Datastore in GCP Console |
| `Auth Failed` | Check GOOGLE_APPLICATION_CREDENTIALS path |
| `Port 8080 taken` | Use `--port 8081` |
| `Module not found` | Run `pip install -r requirements.txt` |

---

## 📚 Next Steps

1. ✅ Read [FEATURES.md](FEATURES.md) for complete documentation
2. ✅ Explore API via Swagger UI at `/docs`
3. ✅ Deploy to Google Cloud Run
4. ✅ Build a frontend using the REST API

---

## 💡 Tips

- **Use descriptive task titles** - AI works better with specific requests
- **Organize notes with categories** - Makes searching easier
- **Set task priorities** - Helps prioritize your work
- **Use the calendar** - Sync with other calendar apps later
- **Chat interface** - Best for conversational requests

---

Happy planning! 🎉
