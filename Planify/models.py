"""Data models for Planify workspace features."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskRequest(BaseModel):
    """Model for creating/updating tasks."""
    title: str
    priority: Optional[str] = "Medium"  # Low, Medium, High
    due_date: Optional[str] = None  # YYYY-MM-DD format
    description: Optional[str] = None


class NoteRequest(BaseModel):
    """Model for creating notes."""
    title: str
    content: str
    category: Optional[str] = "General"


class CalendarEventRequest(BaseModel):
    """Model for creating calendar events."""
    title: str
    date: str  # YYYY-MM-DD format
    time: str  # HH:MM format
    description: Optional[str] = ""
    location: Optional[str] = ""


class TaskResponse(BaseModel):
    """Response model for tasks."""
    id: int
    title: str
    completed: bool
    priority: Optional[str] = "Medium"
    due_date: Optional[str] = None
    created_at: datetime


class NoteResponse(BaseModel):
    """Response model for notes."""
    id: int
    title: str
    content: str
    category: str
    created_at: datetime


class CalendarEventResponse(BaseModel):
    """Response model for calendar events."""
    id: int
    title: str
    date: str
    time: str
    description: Optional[str] = ""
    location: Optional[str] = ""
    created_at: datetime
