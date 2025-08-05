#!/usr/bin/env python3
"""
Test script for Google Calendar integration.
Run this to verify the calendar tools are working correctly.
"""

import sys
import os

# Add the tools directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.calendar_tools import (
    list_calendars, list_events, create_event, update_event,
    delete_event, get_event, create_calendar, delete_calendar
)

def test_calendar_functions():
    """Test all calendar functions."""
    print("🧪 Testing Google Calendar Integration...")
    print("=" * 50)
    
    try:
        # Test 1: List calendars
        print("\n1. Testing list_calendars:")
        calendars_result = list_calendars()
        print(f"Result: {calendars_result}")
        
        # Test 2: List events from primary calendar
        print("\n2. Testing list_events:")
        events_result = list_events(
            calendar_id="primary",
            max_results=5,
            time_min="",
            time_max="",
            query=""
        )
        print(f"Result: {events_result}")
        
        # Test 3: Create a test event
        print("\n3. Testing create_event:")
        from datetime import datetime, timedelta
        
        # Create a test event for tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        end_time = tomorrow.replace(hour=11, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        
        create_result = create_event(
            calendar_id="primary",
            summary="Test Event - Calendar Integration",
            start_time=start_time,
            end_time=end_time,
            description="This is a test event to verify calendar integration",
            location="Test Location",
            attendees=""
        )
        print(f"Result: {create_result}")
        
        print("\n✅ Calendar integration test completed!")
        print("\nTo test with the assistant, run: python main.py")
        print("Then try commands like:")
        print("- 'List my calendars'")
        print("- 'Show my upcoming events'")
        print("- 'Create a meeting tomorrow at 2pm'")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure Credentials.json is in the correct directory")
        print("2. Delete token.pickle if it exists and try again")
        print("3. Check that Google Calendar API is enabled in Google Cloud Console")

if __name__ == "__main__":
    test_calendar_functions() 