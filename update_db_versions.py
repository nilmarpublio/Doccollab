#!/usr/bin/env python3
"""
Script to update the database with the new Version table.
Run this script to add the version history functionality to existing databases.
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Version

def update_database():
    """Update the database with the new Version table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Create the versions table
            db.create_all()
            print("Database updated successfully!")
            print("Version table created")
            
            # Check if there are any existing projects to migrate
            from models.project import Project
            projects = Project.query.all()
            
            if projects:
                print(f"Found {len(projects)} existing projects")
                print("Note: Existing projects will get version snapshots on their next compilation")
            else:
                print("No existing projects found")
                
        except Exception as e:
            print(f"Error updating database: {e}")
            return False
            
    return True

if __name__ == "__main__":
    print("Updating database with version history support...")
    success = update_database()
    
    if success:
        print("\nVersion history functionality is now available!")
        print("Features added:")
        print("   - Automatic version snapshots on compilation")
        print("   - Version history viewer")
        print("   - Version comparison tool")
        print("   - Version restoration")
        print("   - Version management (view, delete)")
    else:
        print("\nDatabase update failed!")
        sys.exit(1)
