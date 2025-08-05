import os
import pickle
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional, Any
from functools import lru_cache

# If modifying these scopes, delete the token.pickle file.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels'
]

def get_gmail_service():
    """Get or create Gmail API service."""
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
            "❌ Gmail authentication failed: Missing credentials file!\n\n"
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
                print(f"🔐 Starting Gmail authentication using {credentials_file}...")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                print("✅ Gmail authentication successful!")
                
            except Exception as e:
                error_msg = f"❌ Gmail authentication failed: {str(e)}\n\nPlease check your credentials.json file and try again."
                return error_msg

    try:
        # Create Gmail API service
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        return f"Error creating Gmail service: {str(e)}"

def get_attachment_data(service, user_id: str, message_id: str, attachment_id: str) -> Dict[str, Any]:
    """
    Get the attachment data for a specific attachment.
    
    Args:
        service: Gmail API service instance
        user_id: User's email address or 'me'
        message_id: ID of the email message
        attachment_id: ID of the attachment
    Returns:
        Dict containing attachment data and metadata
    """
    try:
        attachment = service.users().messages().attachments().get(
            userId=user_id,
            messageId=message_id,
            id=attachment_id
        ).execute()

        file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
        return {
            'data': file_data,
            'size': attachment.get('size'),
            'type': attachment.get('mimeType')
        }
    except Exception as e:
        return {'error': f"Error getting attachment: {str(e)}"}

def list_emails(max_results: int = 10, query: str = "") -> str:
    """
    List emails from Gmail inbox.
    
    Args:
        max_results: Maximum number of emails to return
        query: Gmail search query string
    Returns:
        str: JSON string of email list or error message
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me', 
            maxResults=max_results,
            q=query
        ).execute()
        
        messages = results.get('messages', [])
        email_list = []
        
        for message in messages:
            msg = service.users().messages().get(
                userId='me', 
                id=message['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = msg['payload']['headers']
            email_data = {
                'id': msg['id'],
                'threadId': msg['threadId']
            }
            
            for header in headers:
                name = header['name'].lower()
                if name in ['from', 'subject', 'date']:
                    email_data[name] = header['value']
            
            email_list.append(email_data)
            
        return str(email_list)
    except Exception as e:
        return f"Error listing emails: {str(e)}"

def send_email(to: str, subject: str, body: str, content_type: str = "plain") -> str:
    """
    Send an email using Gmail API.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        content_type: Content type (plain or html)
    Returns:
        str: Success message or error
    """
    try:
        service = get_gmail_service()
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject

        msg = MIMEText(body, content_type)
        message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        send_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        return f"Email sent successfully. Message Id: {send_message['id']}"
    except Exception as e:
        return f"Error sending email: {str(e)}"

def read_email(message_id: str) -> str:
    """
    Read a specific email by its ID, including attachments.
    
    Args:
        message_id: The ID of the email to read
    Returns:
        str: Email content including attachments or error message
    """
    try:
        service = get_gmail_service()
        message = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        payload = message['payload']
        headers = payload['headers']
        
        email_data = {
            'id': message['id'],
            'threadId': message['threadId'],
            'headers': {},
            'body': '',
            'attachments': []
        }
        
        # Get header information
        for header in headers:
            name = header['name'].lower()
            if name in ['from', 'to', 'subject', 'date']:
                email_data['headers'][name] = header['value']
        
        def process_parts(parts, email_data):
            """Process message parts recursively."""
            for part in parts:
                if part.get('filename'):
                    # This is an attachment
                    attachment_data = {
                        'id': part['body'].get('attachmentId'),
                        'filename': part['filename'],
                        'mimeType': part['mimeType'],
                        'size': part['body'].get('size', 0)
                    }
                    if attachment_data['id']:
                        # Get attachment data
                        attachment = get_attachment_data(
                            service, 'me', message_id, attachment_data['id']
                        )
                        attachment_data.update(attachment)
                    email_data['attachments'].append(attachment_data)
                elif part.get('mimeType') == 'text/plain':
                    # This is the email body
                    if 'data' in part['body']:
                        text = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
                        email_data['body'] += text
                elif part.get('parts'):
                    # Recursive call for nested parts
                    process_parts(part['parts'], email_data)

        # Process the email parts
        if 'parts' in payload:
            process_parts(payload['parts'], email_data)
        elif 'body' in payload and 'data' in payload['body']:
            email_data['body'] = base64.urlsafe_b64decode(
                payload['body']['data']
            ).decode('utf-8')
            
        return str(email_data)
    except Exception as e:
        return f"Error reading email: {str(e)}"

def delete_email(message_id: str) -> str:
    """
    Delete a specific email by its ID.
    
    Args:
        message_id: The ID of the email to delete
    Returns:
        str: Success or error message
    """
    try:
        service = get_gmail_service()
        service.users().messages().trash(userId='me', id=message_id).execute()
        return f"Email {message_id} moved to trash successfully"
    except Exception as e:
        return f"Error deleting email: {str(e)}"

# Direct testing
if __name__ == "__main__":
    print("\nTesting Gmail API functions:")
    try:
        # Test listing emails
        print("\nTesting list_emails:")
        result = list_emails(max_results=3)
        print(f"List emails result: {result}")
        
        # Test reading an email (requires a valid message_id)
        if isinstance(result, str) and "id" in result:
            message_id = eval(result)[0]['id']
            print("\nTesting read_email:")
            print(f"Read email result: {read_email(message_id)}")
            
    except Exception as e:
        print(f"Test failed: {str(e)}") 