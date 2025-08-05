def get_tool_definitions():
    """Return the list of tool definitions for the assistant."""
    return [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the contents of a file from the working directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The name of the file to read"
                        }
                    },
                    "required": ["file_path"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Write content to a file in the working directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The name of the file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write to the file"
                        }
                    },
                    "required": ["file_path", "content"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_emails",
                "description": "List emails from Gmail inbox with optional search query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of emails to return (default: 10)"
                        },
                        "query": {
                            "type": "string",
                            "description": "Gmail search query string (optional)"
                        }
                    },
                    "required": ["max_results", "query"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "Send an email using Gmail API. Use this when the user asks to send an email message to someone. Do NOT use this for calendar events - use create_event instead.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject"
                        },
                        "body": {
                            "type": "string",
                            "description": "Email body content"
                        },
                        "content_type": {
                            "type": "string",
                            "description": "Content type (plain or html)",
                            "enum": ["plain", "html"]
                        }
                    },
                    "required": ["to", "subject", "body", "content_type"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_email",
                "description": "Read a specific email by its ID, including any attachments. Returns email content, headers, and attachment details (filename, size, type, and data).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message_id": {
                            "type": "string",
                            "description": "The ID of the email to read"
                        }
                    },
                    "required": ["message_id"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_email",
                "description": "Delete (move to trash) a specific email by its ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message_id": {
                            "type": "string",
                            "description": "The ID of the email to delete"
                        }
                    },
                    "required": ["message_id"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_calendars",
                "description": "List all calendars accessible to the user",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_events",
                "description": "List events from a calendar with optional time range and search query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "Calendar ID (uses 'primary' if not specified)"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of events to return (uses 10 if not specified)"
                        },
                        "time_min": {
                            "type": "string",
                            "description": "Start time in ISO format (uses current time if not specified)"
                        },
                        "time_max": {
                            "type": "string",
                            "description": "End time in ISO format (uses 7 days from now if not specified)"
                        },
                        "query": {
                            "type": "string",
                            "description": "Search query for events (optional)"
                        }
                    },
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_event",
                "description": "Create a new calendar event in Google Calendar. Use this when the user asks to add, create, schedule, or book an event or meeting in their calendar.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "Calendar ID (uses 'primary' if not specified)"
                        },
                        "summary": {
                            "type": "string",
                            "description": "Event title/summary"
                        },
                        "start_time": {
                            "type": "string",
                            "description": "Start time in ISO format"
                        },
                        "end_time": {
                            "type": "string",
                            "description": "End time in ISO format"
                        },
                        "description": {
                            "type": "string",
                            "description": "Event description (optional)"
                        },
                        "location": {
                            "type": "string",
                            "description": "Event location (optional)"
                        },
                        "attendees": {
                            "type": "string",
                            "description": "Comma-separated list of attendee emails (optional)"
                        }
                    },
                    "required": ["summary", "start_time", "end_time"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_event",
                "description": "Update an existing calendar event",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "Calendar ID"
                        },
                        "event_id": {
                            "type": "string",
                            "description": "Event ID to update"
                        },
                        "summary": {
                            "type": "string",
                            "description": "New event title/summary (optional)"
                        },
                        "start_time": {
                            "type": "string",
                            "description": "New start time in ISO format (optional)"
                        },
                        "end_time": {
                            "type": "string",
                            "description": "New end time in ISO format (optional)"
                        },
                        "description": {
                            "type": "string",
                            "description": "New event description (optional)"
                        },
                        "location": {
                            "type": "string",
                            "description": "New event location (optional)"
                        }
                    },
                    "required": ["calendar_id", "event_id"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_event",
                "description": "Delete a calendar event",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "Calendar ID"
                        },
                        "event_id": {
                            "type": "string",
                            "description": "Event ID to delete"
                        }
                    },
                    "required": ["calendar_id", "event_id"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_event",
                "description": "Get details of a specific calendar event",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "Calendar ID"
                        },
                        "event_id": {
                            "type": "string",
                            "description": "Event ID to retrieve"
                        }
                    },
                    "required": ["calendar_id", "event_id"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_calendar",
                "description": "Create a new secondary calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "Calendar name/title"
                        },
                        "description": {
                            "type": "string",
                            "description": "Calendar description (optional)"
                        },
                        "time_zone": {
                            "type": "string",
                            "description": "Calendar timezone (uses 'America/Los_Angeles' if not specified)"
                        }
                    },
                    "required": ["summary"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_calendar",
                "description": "Delete a secondary calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "Calendar ID to delete"
                        }
                    },
                    "required": ["calendar_id"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    ]