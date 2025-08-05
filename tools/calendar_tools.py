import os
import pickle
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from functools import lru_cache
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the token.pickle file.
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def get_calendar_service():
    """Get or create Google Calendar API service."""
    creds = None
    
    # Check for credentials file with different possible names
    credentials_file = None
    possible_names = ['credentials.json', 'Credentials.json', 'client_secret.json']
    
    for name in possible_names:
        if os.path.exists(name):
            credentials_file = name
            break
    
    if not credentials_file:
        error_msg = (
            "❌ Google Calendar authentication failed: Missing credentials file!\n\n"
            "To fix this:\n"
            "1. Download your credentials.json file from Google Cloud Console\n"
            "2. Place it in the same directory as main.py\n"
            "3. Make sure it's named 'credentials.json' (lowercase)\n"
            "4. Delete token.pickle if it exists and run again\n\n"
            f"Current directory: {os.getcwd()}\n"
            f"Files in directory: {[f for f in os.listdir('.') if f.endswith('.json')]}"
        )
        return error_msg
    
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        try:
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            print(f"Warning: Could not load token.pickle: {e}")
            # Remove corrupted token file
            if os.path.exists('token.pickle'):
                os.remove('token.pickle')
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Warning: Could not refresh token: {e}")
                # Remove invalid token file
                if os.path.exists('token.pickle'):
                    os.remove('token.pickle')
                creds = None
        
        if not creds:
            try:
                print(f"🔐 Starting Google Calendar authentication using {credentials_file}...")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                print("✅ Google Calendar authentication successful!")
                
            except Exception as e:
                error_msg = f"❌ Google Calendar authentication failed: {str(e)}\n\nPlease check your credentials.json file and try again."
                return error_msg

    try:
        # Create Google Calendar API service
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        return f"Error creating Google Calendar service: {str(e)}"

def list_calendars() -> str:
    """
    List all calendars accessible to the user.
    
    Returns:
        str: JSON string of calendar list or error message
    """
    try:
        service = get_calendar_service()
        if isinstance(service, str):
            return service  # Return error message
        
        calendars = service.calendarList().list().execute()
        calendar_list = []
        
        for calendar in calendars.get('items', []):
            calendar_info = {
                'id': calendar['id'],
                'summary': calendar.get('summary', 'No title'),
                'description': calendar.get('description', ''),
                'primary': calendar.get('primary', False),
                'accessRole': calendar.get('accessRole', ''),
                'backgroundColor': calendar.get('backgroundColor', ''),
                'foregroundColor': calendar.get('foregroundColor', '')
            }
            calendar_list.append(calendar_info)
            
        return str(calendar_list)
    except Exception as e:
        return f"Error listing calendars: {str(e)}"

def list_events(calendar_id: str = "primary", max_results: int = 10, time_min: str = "", time_max: str = "", query: str = "") -> str:
    """
    List events from a calendar.
    
    Args:
        calendar_id: Calendar ID (default: "primary")
        max_results: Maximum number of events to return
        time_min: Start time in ISO format (default: now)
        time_max: End time in ISO format (default: 7 days from now)
        query: Search query for events
    Returns:
        str: JSON string of event list or error message
    """
    try:
        service = get_calendar_service()
        if isinstance(service, str):
            return service  # Return error message
        
        # Set default values if not provided
        if not calendar_id:
            calendar_id = "primary"
        if not max_results:
            max_results = 10
        
        # Set default time range if not provided
        now = datetime.utcnow()
        if not time_min:
            time_min = now.isoformat() + 'Z'
        if not time_max:
            time_max = (now + timedelta(days=7)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            q=query,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        event_list = []
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            event_info = {
                'id': event['id'],
                'summary': event.get('summary', 'No title'),
                'description': event.get('description', ''),
                'start': start,
                'end': end,
                'location': event.get('location', ''),
                'attendees': [attendee['email'] for attendee in event.get('attendees', [])],
                'htmlLink': event.get('htmlLink', ''),
                'status': event.get('status', '')
            }
            event_list.append(event_info)
            
        return str(event_list)
    except Exception as e:
        return f"Error listing events: {str(e)}"

def create_event(calendar_id: str = "primary", summary: str = "", start_time: str = "", end_time: str = "", description: str = "", location: str = "", attendees: str = "") -> str:
    """
    Create a new calendar event.
    
    Args:
        calendar_id: Calendar ID (default: "primary")
        summary: Event title/summary
        start_time: Start time in ISO format
        end_time: End time in ISO format
        description: Event description
        location: Event location
        attendees: Comma-separated list of attendee emails
    Returns:
        str: Success message with event ID or error message
    """
    try:
        service = get_calendar_service()
        if isinstance(service, str):
            return service  # Return error message
        
        # Set default values if not provided
        if not calendar_id:
            calendar_id = "primary"
        if not description:
            description = ""
        if not location:
            location = ""
        
        event = {
            'summary': summary,
            'description': description,
            'location': location,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Los_Angeles',  # PST timezone
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Los_Angeles',  # PST timezone
            },
        }
        
        # Add attendees if provided
        if attendees:
            attendee_list = [{'email': email.strip()} for email in attendees.split(',')]
            event['attendees'] = attendee_list
        
        event = service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()
        
        return f"Event created successfully! Event ID: {event['id']}, Link: {event.get('htmlLink', 'N/A')}"
    except Exception as e:
        return f"Error creating event: {str(e)}"

def update_event(calendar_id: str, event_id: str, summary: str = "", start_time: str = "", end_time: str = "", description: str = "", location: str = "") -> str:
    """
    Update an existing calendar event.
    
    Args:
        calendar_id: Calendar ID
        event_id: Event ID to update
        summary: New event title/summary
        start_time: New start time in ISO format
        end_time: New end time in ISO format
        description: New event description
        location: New event location
    Returns:
        str: Success message or error message
    """
    try:
        service = get_calendar_service()
        if isinstance(service, str):
            return service  # Return error message
        
        # Get the existing event
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        
        # Update only the fields that are provided
        if summary:
            event['summary'] = summary
        if start_time:
            event['start']['dateTime'] = start_time
        if end_time:
            event['end']['dateTime'] = end_time
        if description:
            event['description'] = description
        if location:
            event['location'] = location
        
        updated_event = service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event
        ).execute()
        
        return f"Event updated successfully! Event ID: {updated_event['id']}"
    except Exception as e:
        return f"Error updating event: {str(e)}"

def delete_event(calendar_id: str, event_id: str) -> str:
    """
    Delete a calendar event.
    
    Args:
        calendar_id: Calendar ID
        event_id: Event ID to delete
    Returns:
        str: Success message or error message
    """
    try:
        service = get_calendar_service()
        if isinstance(service, str):
            return service  # Return error message
        
        service.events().delete(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        
        return f"Event {event_id} deleted successfully"
    except Exception as e:
        return f"Error deleting event: {str(e)}"

def get_event(calendar_id: str, event_id: str) -> str:
    """
    Get details of a specific calendar event.
    
    Args:
        calendar_id: Calendar ID
        event_id: Event ID to retrieve
    Returns:
        str: Event details as JSON string or error message
    """
    try:
        service = get_calendar_service()
        if isinstance(service, str):
            return service  # Return error message
        
        event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        
        event_info = {
            'id': event['id'],
            'summary': event.get('summary', 'No title'),
            'description': event.get('description', ''),
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'location': event.get('location', ''),
            'attendees': [attendee['email'] for attendee in event.get('attendees', [])],
            'htmlLink': event.get('htmlLink', ''),
            'status': event.get('status', ''),
            'created': event.get('created', ''),
            'updated': event.get('updated', '')
        }
        
        return str(event_info)
    except Exception as e:
        return f"Error getting event: {str(e)}"

def create_calendar(summary: str = "", description: str = "", time_zone: str = "America/Los_Angeles") -> str:
    """
    Create a new secondary calendar.
    
    Args:
        summary: Calendar name/title
        description: Calendar description
        time_zone: Calendar timezone (default: PST)
    Returns:
        str: Success message with calendar ID or error message
    """
    try:
        service = get_calendar_service()
        if isinstance(service, str):
            return service  # Return error message
        
        # Set default values if not provided
        if not description:
            description = ""
        if not time_zone:
            time_zone = "America/Los_Angeles"
        
        calendar = {
            'summary': summary,
            'description': description,
            'timeZone': time_zone
        }
        
        created_calendar = service.calendars().insert(body=calendar).execute()
        
        return f"Calendar created successfully! Calendar ID: {created_calendar['id']}, Summary: {created_calendar['summary']}"
    except Exception as e:
        return f"Error creating calendar: {str(e)}"

def delete_calendar(calendar_id: str) -> str:
    """
    Delete a secondary calendar.
    
    Args:
        calendar_id: Calendar ID to delete
    Returns:
        str: Success message or error message
    """
    try:
        service = get_calendar_service()
        if isinstance(service, str):
            return service  # Return error message
        
        service.calendars().delete(calendarId=calendar_id).execute()
        
        return f"Calendar {calendar_id} deleted successfully"
    except Exception as e:
        return f"Error deleting calendar: {str(e)}"

# Direct testing
if __name__ == "__main__":
    print("\nTesting Google Calendar API functions:")
    try:
        # Test listing calendars
        print("\nTesting list_calendars:")
        result = list_calendars()
        print(f"List calendars result: {result}")
        
        # Test listing events
        print("\nTesting list_events:")
        events_result = list_events(max_results=5)
        print(f"List events result: {events_result}")
        
    except Exception as e:
        print(f"Test failed: {str(e)}") 