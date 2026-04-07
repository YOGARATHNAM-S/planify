"""Additional REST API endpoints for task, note, and calendar management."""

from fastapi import APIRouter, HTTPException
from google.cloud import datastore
import datetime
import logging
from models import TaskRequest, NoteRequest, CalendarEventRequest

db = datastore.Client()
router = APIRouter(prefix="/api/v1", tags=["workspace"])

# ================= TASK ENDPOINTS =================

@router.post("/tasks")
def create_task(request: TaskRequest):
    """Create a new task."""
    try:
        key = db.key('Task')
        task = datastore.Entity(key=key)
        task.update({
            'title': request.title,
            'priority': request.priority,
            'due_date': request.due_date,
            'description': request.description,
            'completed': False,
            'created_at': datetime.datetime.now()
        })
        db.put(task)
        return {
            "status": "success",
            "id": task.key.id,
            "message": f"Task '{request.title}' created successfully."
        }
    except Exception as e:
        logging.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks")
def list_tasks(completed: bool = None):
    """List all tasks, optionally filtered by completion status."""
    try:
        query = db.query(kind='Task')
        tasks = list(query.fetch())
        
        if completed is not None:
            tasks = [t for t in tasks if t.get('completed') == completed]
        
        return {
            "status": "success",
            "count": len(tasks),
            "tasks": [{
                "id": t.key.id,
                "title": t.get('title'),
                "priority": t.get('priority', 'Medium'),
                "due_date": t.get('due_date'),
                "completed": t.get('completed', False),
                "created_at": t.get('created_at')
            } for t in tasks]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tasks/{task_id}")
def update_task(task_id: int, request: TaskRequest):
    """Update a task."""
    try:
        key = db.key('Task', task_id)
        task = db.get(key)
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task['title'] = request.title
        task['priority'] = request.priority
        task['due_date'] = request.due_date
        task['description'] = request.description
        db.put(task)
        
        return {"status": "success", "message": "Task updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/tasks/{task_id}/complete")
def mark_task_complete(task_id: int):
    """Mark a task as complete."""
    try:
        key = db.key('Task', task_id)
        task = db.get(key)
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task['completed'] = True
        db.put(task)
        
        return {"status": "success", "message": "Task marked as complete."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task."""
    try:
        key = db.key('Task', task_id)
        db.delete(key)
        return {"status": "success", "message": "Task deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ================= NOTE ENDPOINTS =================

@router.post("/notes")
def create_note(request: NoteRequest):
    """Create a new note."""
    try:
        key = db.key('Note')
        note = datastore.Entity(key=key)
        note.update({
            'title': request.title,
            'content': request.content,
            'category': request.category,
            'created_at': datetime.datetime.now()
        })
        db.put(note)
        return {
            "status": "success",
            "id": note.key.id,
            "message": f"Note '{request.title}' created successfully."
        }
    except Exception as e:
        logging.error(f"Error creating note: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notes")
def list_notes(category: str = None):
    """List all notes, optionally filtered by category."""
    try:
        query = db.query(kind='Note')
        notes = list(query.fetch())
        
        if category:
            notes = [n for n in notes if n.get('category') == category]
        
        return {
            "status": "success",
            "count": len(notes),
            "notes": [{
                "id": n.key.id,
                "title": n.get('title'),
                "category": n.get('category', 'General'),
                "content": n.get('content'),
                "created_at": n.get('created_at')
            } for n in notes]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/notes/{note_id}")
def update_note(note_id: int, request: NoteRequest):
    """Update a note."""
    try:
        key = db.key('Note', note_id)
        note = db.get(key)
        
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        note['title'] = request.title
        note['content'] = request.content
        note['category'] = request.category
        db.put(note)
        
        return {"status": "success", "message": "Note updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/notes/{note_id}")
def delete_note(note_id: int):
    """Delete a note."""
    try:
        key = db.key('Note', note_id)
        db.delete(key)
        return {"status": "success", "message": "Note deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ================= CALENDAR EVENT ENDPOINTS =================

@router.post("/events")
def create_event(request: CalendarEventRequest):
    """Create a new calendar event."""
    try:
        # Parse date and time
        event_datetime = datetime.datetime.strptime(
            f"{request.date} {request.time}", "%Y-%m-%d %H:%M"
        )
        
        key = db.key('CalendarEvent')
        event = datastore.Entity(key=key)
        event.update({
            'title': request.title,
            'date': request.date,
            'time': request.time,
            'datetime': event_datetime,
            'description': request.description,
            'location': request.location,
            'created_at': datetime.datetime.now()
        })
        db.put(event)
        return {
            "status": "success",
            "id": event.key.id,
            "message": f"Event '{request.title}' created successfully."
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date/time format. Use YYYY-MM-DD HH:MM")
    except Exception as e:
        logging.error(f"Error creating event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events")
def list_events(days_ahead: int = 7):
    """List upcoming calendar events."""
    try:
        query = db.query(kind='CalendarEvent')
        events = list(query.fetch())
        
        now = datetime.datetime.now()
        upcoming = []
        
        for evt in events:
            evt_datetime = evt.get('datetime')
            if evt_datetime:
                days_diff = (evt_datetime - now).days
                if 0 <= days_diff <= days_ahead:
                    upcoming.append((evt_datetime, evt))
        
        upcoming.sort(key=lambda x: x[0])
        
        return {
            "status": "success",
            "count": len(upcoming),
            "events": [{
                "id": evt.key.id,
                "title": evt.get('title'),
                "date": evt.get('date'),
                "time": evt.get('time'),
                "location": evt.get('location'),
                "description": evt.get('description'),
                "created_at": evt.get('created_at')
            } for _, evt in upcoming]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/events/{event_id}")
def delete_event(event_id: int):
    """Delete a calendar event."""
    try:
        key = db.key('CalendarEvent', event_id)
        db.delete(key)
        return {"status": "success", "message": "Event deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ================= SUMMARY ENDPOINT =================

@router.get("/summary")
def get_workspace_summary():
    """Get a summary of workspace items."""
    try:
        task_query = db.query(kind='Task')
        tasks = list(task_query.fetch())
        
        note_query = db.query(kind='Note')
        notes = list(note_query.fetch())
        
        event_query = db.query(kind='CalendarEvent')
        events = list(event_query.fetch())
        
        incomplete_tasks = len([t for t in tasks if not t.get('completed', False)])
        
        return {
            "status": "success",
            "summary": {
                "active_tasks": incomplete_tasks,
                "completed_tasks": len(tasks) - incomplete_tasks,
                "total_notes": len(notes),
                "total_events": len(events)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
