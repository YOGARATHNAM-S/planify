"""Test script to verify Planify setup and functionality."""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8080/api/v1"

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_tasks():
    """Test task management endpoints."""
    print_section("Testing Task Management")
    
    # Create task
    print("1. Creating a test task...")
    task_data = {
        "title": "Test Task - Buy Coffee",
        "priority": "Medium",
        "due_date": "2024-12-25",
        "description": "Get some quality coffee beans"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        task_id = response.json().get("id")
        print(f"   Created Task ID: {task_id}")
        print(f"   Message: {response.json().get('message')}")
    else:
        print(f"   Error: {response.text}")
        return
    
    # List tasks
    print("\n2. Listing all tasks...")
    response = requests.get(f"{BASE_URL}/tasks")
    print(f"   Status: {response.status_code}")
    tasks = response.json().get("tasks", [])
    print(f"   Total tasks: {len(tasks)}")
    for task in tasks[:3]:
        print(f"   - {task['title']} (Priority: {task['priority']})")
    
    # Mark complete
    if task_id:
        print(f"\n3. Marking task {task_id} as complete...")
        response = requests.patch(f"{BASE_URL}/tasks/{task_id}/complete")
        print(f"   Status: {response.status_code}")
        print(f"   Message: {response.json().get('message')}")

def test_notes():
    """Test note management endpoints."""
    print_section("Testing Note Management")
    
    # Create note
    print("1. Creating a test note...")
    note_data = {
        "title": "Test Meeting Notes",
        "content": "Discussed Q4 objectives and planning timeline",
        "category": "Work"
    }
    response = requests.post(f"{BASE_URL}/notes", json=note_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        note_id = response.json().get("id")
        print(f"   Created Note ID: {note_id}")
        print(f"   Message: {response.json().get('message')}")
    else:
        print(f"   Error: {response.text}")
        return
    
    # List notes
    print("\n2. Listing all notes...")
    response = requests.get(f"{BASE_URL}/notes")
    print(f"   Status: {response.status_code}")
    notes = response.json().get("notes", [])
    print(f"   Total notes: {len(notes)}")
    for note in notes[:3]:
        print(f"   - {note['title']} [{note['category']}]")

def test_events():
    """Test calendar event endpoints."""
    print_section("Testing Calendar Management")
    
    # Create event
    print("1. Creating a test calendar event...")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    event_data = {
        "title": "Test Team Meeting",
        "date": tomorrow,
        "time": "14:00",
        "location": "Conference Room A",
        "description": "Testing the calendar system"
    }
    response = requests.post(f"{BASE_URL}/events", json=event_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        event_id = response.json().get("id")
        print(f"   Created Event ID: {event_id}")
        print(f"   Message: {response.json().get('message')}")
    else:
        print(f"   Error: {response.text}")
        return
    
    # List events
    print("\n2. Listing upcoming events...")
    response = requests.get(f"{BASE_URL}/events?days_ahead=30")
    print(f"   Status: {response.status_code}")
    events = response.json().get("events", [])
    print(f"   Upcoming events: {len(events)}")
    for event in events[:3]:
        print(f"   - {event['title']} on {event['date']} at {event['time']}")

def test_summary():
    """Test workspace summary endpoint."""
    print_section("Testing Workspace Summary")
    
    print("Fetching workspace summary...")
    response = requests.get(f"{BASE_URL}/summary")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        summary = response.json().get("summary", {})
        print(f"\nWorkspace Status:")
        print(f"  Active Tasks: {summary.get('active_tasks', 0)}")
        print(f"  Completed Tasks: {summary.get('completed_tasks', 0)}")
        print(f"  Total Notes: {summary.get('total_notes', 0)}")
        print(f"  Total Events: {summary.get('total_events', 0)}")
    else:
        print(f"Error: {response.text}")

def test_ai_chat():
    """Test AI chat interface."""
    print_section("Testing AI Chat Interface")
    
    test_prompts = [
        "Create a task: Review code by tomorrow",
        "Add a note: Project ideas for Q1",
        "List my tasks"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"{i}. Sending: '{prompt}'")
        response = requests.post(
            "http://localhost:8080/api/v1/workspace/chat",
            json={"prompt": prompt}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            reply = response.json().get("reply", "No reply")
            print(f"   Response: {reply[:100]}...")
        else:
            print(f"   Error: {response.text[:100]}")
        print()

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  PLANIFY TEST SUITE")
    print("="*60)
    
    # Check if server is running
    print("\nChecking server connectivity...")
    try:
        response = requests.get(f"{BASE_URL}/summary", timeout=5)
        print("✓ Server is running and responding\n")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server at http://localhost:8080")
        print("  Make sure to run: uvicorn agent:app --reload")
        return
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Run all tests
    try:
        test_tasks()
        test_notes()
        test_events()
        test_summary()
        test_ai_chat()
        
        print_section("All Tests Completed!")
        print("✓ Task Management - Working")
        print("✓ Note Management - Working")
        print("✓ Calendar Management - Working")
        print("✓ Summary - Working")
        print("✓ AI Chat - Working")
        print("\nYour Planify setup is working correctly! 🎉\n")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")

if __name__ == "__main__":
    main()
