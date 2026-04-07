import os
import logging
import datetime
import asyncio
import google.cloud.logging
from google.cloud import datastore
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from mcp.server.fastmcp import FastMCP 

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from api_endpoints import router as workspace_router

# --- 1. Setup Logging ---
try:
    cloud_logging_client = google.cloud.logging.Client()
    cloud_logging_client.setup_logging()
except Exception:
    logging.basicConfig(level=logging.INFO)

load_dotenv()
model_name = os.getenv("MODEL", "gemini-1.5-flash")

# --- 2. Database Setup ---
# PRO TIP: For the default database, leaving arguments empty is the most stable 
# way to deploy on Google Cloud. It auto-detects the project and (default) DB.
db = datastore.Client() 

mcp = FastMCP("WorkspaceTools")

# ================= 3. TOOLS =================

@mcp.tool()
def add_task(title: str) -> str:
    """Adds a new task to the workspace."""
    try:
        key = db.key('Task')
        task = datastore.Entity(key=key)
        task.update({
            'title': title, 
            'completed': False, 
            'created_at': datetime.datetime.now()
        })
        db.put(task)
        return f"Success: Task '{title}' saved (ID: {task.key.id})."
    except Exception as e:
        logging.error(f"DB Error in add_task: {e}")
        return f"Database Error: {str(e)}"

@mcp.tool()
def list_tasks() -> str:
    """Lists all current tasks."""
    try:
        query = db.query(kind='Task')
        tasks = list(query.fetch())
        if not tasks: return "Your task list is empty."
        
        res = ["📋 Current Tasks:"]
        for t in tasks:
            status = "✅" if t.get('completed') else "⏳"
            res.append(f"{status} {t.get('title')} (ID: {t.key.id})")
        return "\n".join(res)
    except Exception as e:
        return f"Database Error: {str(e)}"

@mcp.tool()
def complete_task(task_id: str) -> str:
    """Marks a task as complete. Input must be the numeric ID."""
    try:
        numeric_id = int(''.join(filter(str.isdigit, task_id)))
        key = db.key('Task', numeric_id)
        task = db.get(key)
        if task:
            task['completed'] = True
            db.put(task)
            return f"Task {numeric_id} marked as done."
        return f"Task {numeric_id} not found."
    except Exception as e:
        return f"Error processing task ID: {str(e)}"

@mcp.tool()
def add_note(title: str, content: str, category: str = "General") -> str:
    """Saves a detailed note with category for organization."""
    try:
        key = db.key('Note')
        note = datastore.Entity(key=key)
        note.update({
            'title': title, 
            'content': content, 
            'category': category,
            'created_at': datetime.datetime.now()
        })
        db.put(note)
        return f"Note '{title}' saved successfully in '{category}' category."
    except Exception as e:
        return f"Database Error: {str(e)}"

@mcp.tool()
def list_notes() -> str:
    """Lists all saved notes."""
    try:
        query = db.query(kind='Note')
        notes = list(query.fetch())
        if not notes: return "You have no notes yet."
        
        res = ["📝 Your Notes:"]
        for n in notes:
            category = n.get('category', 'General')
            created = n.get('created_at', 'Unknown')
            res.append(f"📌 {n.get('title')} [{category}] (ID: {n.key.id})")
            res.append(f"   {n.get('content')[:50]}...")
        return "\n".join(res)
    except Exception as e:
        return f"Database Error: {str(e)}"

@mcp.tool()
def delete_note(note_id: str) -> str:
    """Deletes a note by ID."""
    try:
        numeric_id = int(''.join(filter(str.isdigit, note_id)))
        key = db.key('Note', numeric_id)
        db.delete(key)
        return f"Note {numeric_id} deleted successfully."
    except Exception as e:
        return f"Error deleting note: {str(e)}"

@mcp.tool()
def add_event(title: str, date: str, time: str, description: str = "", location: str = "") -> str:
    """Adds a calendar event. Date format: YYYY-MM-DD, Time format: HH:MM."""
    try:
        # Parse date and time
        event_datetime = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        
        key = db.key('CalendarEvent')
        event = datastore.Entity(key=key)
        event.update({
            'title': title,
            'date': date,
            'time': time,
            'datetime': event_datetime,
            'description': description,
            'location': location,
            'created_at': datetime.datetime.now()
        })
        db.put(event)
        return f"Calendar event '{title}' added on {date} at {time}."
    except ValueError as ve:
        return f"Date/Time Format Error: Use YYYY-MM-DD for date and HH:MM for time."
    except Exception as e:
        return f"Database Error: {str(e)}"

@mcp.tool()
def list_events(days_ahead: int = 7) -> str:
    """Lists upcoming calendar events in the next N days."""
    try:
        query = db.query(kind='CalendarEvent')
        events = list(query.fetch())
        
        now = datetime.datetime.now()
        future_events = []
        
        for evt in events:
            evt_datetime = evt.get('datetime')
            if evt_datetime:
                days_diff = (evt_datetime - now).days
                if 0 <= days_diff <= days_ahead:
                    future_events.append((evt_datetime, evt))
        
        if not future_events: 
            return f"No events scheduled in the next {days_ahead} days."
        
        future_events.sort(key=lambda x: x[0])
        
        res = [f"📅 Upcoming Events (Next {days_ahead} days):"]
        for _, evt in future_events:
            location_str = f" @ {evt.get('location')}" if evt.get('location') else ""
            res.append(f"📌 {evt.get('title')} on {evt.get('date')} at {evt.get('time')}{location_str}")
            if evt.get('description'):
                res.append(f"   {evt.get('description')}")
        return "\n".join(res)
    except Exception as e:
        return f"Database Error: {str(e)}"

@mcp.tool()
def delete_event(event_id: str) -> str:
    """Deletes a calendar event by ID."""
    try:
        numeric_id = int(''.join(filter(str.isdigit, event_id)))
        key = db.key('CalendarEvent', numeric_id)
        db.delete(key)
        return f"Calendar event {numeric_id} deleted successfully."
    except Exception as e:
        return f"Error deleting event: {str(e)}"

@mcp.tool()
def update_task(task_id: str, title: str = None, priority: str = "Medium", due_date: str = None) -> str:
    """Updates task details like priority and due date. Priority: Low/Medium/High."""
    try:
        numeric_id = int(''.join(filter(str.isdigit, task_id)))
        key = db.key('Task', numeric_id)
        task = db.get(key)
        
        if not task:
            return f"Task {numeric_id} not found."
        
        if title:
            task['title'] = title
        if priority in ["Low", "Medium", "High"]:
            task['priority'] = priority
        if due_date:
            task['due_date'] = due_date
        
        db.put(task)
        return f"Task {numeric_id} updated successfully."
    except Exception as e:
        return f"Error updating task: {str(e)}"

@mcp.tool()
def get_summary() -> str:
    """Gets a summary of all tasks, notes, and upcoming events."""
    try:
        # Tasks
        task_query = db.query(kind='Task')
        tasks = list(task_query.fetch())
        incomplete_tasks = [t for t in tasks if not t.get('completed', False)]
        
        # Notes
        note_query = db.query(kind='Note')
        notes = list(note_query.fetch())
        
        # Events
        event_query = db.query(kind='CalendarEvent')
        events = list(event_query.fetch())
        
        summary = [
            "📊 Workspace Summary:",
            f"✅ Tasks: {len(incomplete_tasks)} active, {len(tasks) - len(incomplete_tasks)} completed",
            f"📝 Notes: {len(notes)} saved",
            f"📅 Events: {len(events)} scheduled"
        ]
        return "\n".join(summary)
    except Exception as e:
        return f"Database Error: {str(e)}"

# ================= 4. AGENTS =================

def add_prompt_to_state(tool_context: ToolContext, prompt: str):
    """Internal tool to bridge user intent across the agent workflow."""
    tool_context.state["PROMPT"] = prompt
    return {"status": "ok"}

def workspace_instruction(ctx):
    # This pulls from the state we set in the root_agent
    user_prompt = ctx.state.get("PROMPT", "Welcome the user.")
    return f"""
You are the Workspace Executive Assistant for Dr. Abhishek.
Always start with a polite, professional greeting.
Then, use your tools to complete this request: {user_prompt}
"""

def root_instruction(ctx):
    # Pulls the prompt directly from the API call
    raw_input = ctx.state.get("user_input", "Hello")
    return f"""
1. Save this user input using 'add_prompt_to_state': {raw_input}
2. Hand off control to the 'workflow' agent.
"""

workspace_agent = Agent(
    name="workspace",
    model=model_name,
    instruction=workspace_instruction,
    tools=[
        add_task, list_tasks, complete_task, update_task,
        add_note, list_notes, delete_note,
        add_event, list_events, delete_event,
        get_summary
    ]
)

workflow = SequentialAgent(
    name="workflow",
    sub_agents=[workspace_agent]
)

root_agent = Agent(
    name="root",
    model=model_name,
    instruction=root_instruction,
    tools=[add_prompt_to_state],
    sub_agents=[workflow]
)

# ================= 5. API =================

app = FastAPI()

# Include the workspace routes
app.include_router(workspace_router)

class UserRequest(BaseModel):
    prompt: str

@app.post("/api/v1/workspace/chat")
async def chat(request: UserRequest):
    try:
        final_reply = ""
        # Inject user_input into the agent state
        async for event in root_agent.run_async({"user_input": request.prompt}):
            if hasattr(event, 'text') and event.text:
                final_reply = event.text

        return {
            "status": "success",
            "reply": final_reply if final_reply else "Request processed."
        }

    except Exception as e:
        logging.error(f"Chat Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)