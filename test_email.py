import os
from tools.gmail_tools import send_email, get_gmail_service

def test_send_email():
    print("Sending test email...")
    try:
        result = send_email(
            to="romellrandal@gmail.com",
            subject="Test Email from Gmail API Integration",
            body="""
Hello!

This is a test email sent using the Gmail API integration.
If you receive this, the integration is working correctly!

Best regards,
Your AI Assistant
            """,
            content_type="plain"
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_send_email() 