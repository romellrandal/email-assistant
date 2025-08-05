#!/usr/bin/env python3
"""
Force update assistant configuration script.
This will delete the existing assistant and create a new one with updated tools.
"""

import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import get_tool_definitions
from prompts import SUPER_ASSISTANT_INSTRUCTIONS

def force_update_assistant():
    """Force update assistant by deleting and recreating it."""
    
    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'), override=True)
    
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return
    
    client = OpenAI(api_key=api_key)
    assistant_id = os.getenv("ASSISTANT_ID")
    
    try:
        if assistant_id:
            print(f"🗑️  Deleting existing assistant: {assistant_id}")
            client.beta.assistants.delete(assistant_id)
            print("✅ Assistant deleted successfully")
        
        print("🔄 Creating new assistant with updated tools...")
        
        # Create new assistant
        new_assistant = client.beta.assistants.create(
            name="Super Assistant",
            instructions=SUPER_ASSISTANT_INSTRUCTIONS,
            model="gpt-4o-mini",
            tools=get_tool_definitions()
        )
        
        print(f"✅ New assistant created with ID: {new_assistant.id}")
        
        # Update .env file with new assistant ID
        env_file = '.env'
        env_content = ""
        
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if not line.startswith('ASSISTANT_ID='):
                        env_content += line
        
        env_content += f"ASSISTANT_ID={new_assistant.id}\n"
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ .env file updated with new assistant ID")
        
        # List all tools to verify they're included
        tools = get_tool_definitions()
        print(f"\n📋 Assistant now has {len(tools)} tools:")
        for i, tool in enumerate(tools, 1):
            if tool.get("type") == "function":
                print(f"  {i}. {tool['function']['name']}")
        
        print("\n🎉 Assistant update complete! You can now run: python main.py")
        
    except Exception as e:
        print(f"❌ Error updating assistant: {str(e)}")

if __name__ == "__main__":
    force_update_assistant() 