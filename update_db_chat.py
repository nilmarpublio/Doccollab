#!/usr/bin/env python3
"""
Script to update the database with the new ChatMessage table.
Run this script to add the chat functionality to existing databases.
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, ChatMessage

def update_database():
    """Update the database with the new ChatMessage table"""
    app, socketio = create_app()
    
    with app.app_context():
        try:
            # Create the chat_messages table
            db.create_all()
            print("Database updated successfully!")
            print("ChatMessage table created")
            
            # Check if there are any existing projects
            from models.project import Project
            projects = Project.query.all()
            
            if projects:
                print(f"Found {len(projects)} existing projects")
                print("Chat functionality is now available for all projects")
            else:
                print("No existing projects found")
                
        except Exception as e:
            print(f"Error updating database: {e}")
            return False
            
    return True

if __name__ == "__main__":
    print("Updating database with chat functionality...")
    success = update_database()
    
    if success:
        print("\nChat functionality is now available!")
        print("Features added:")
        print("   - Real-time chat in editor")
        print("   - Project-based chat rooms")
        print("   - Online user indicators")
        print("   - Typing indicators")
        print("   - Message history")
        print("   - SocketIO integration")
    else:
        print("\nDatabase update failed!")
        sys.exit(1)
