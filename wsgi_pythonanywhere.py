# WSGI Configuration for PythonAnywhere
# DocCollab - Versão Final

import sys
import os

# Add your project directory to the Python path
path = '/home/123nilmarcastro/DocCollab'
if path not in sys.path:
    sys.path.append(path)

# Change to the project directory
os.chdir(path)

# Import your Flask app
from app import create_app

# Create the Flask app and SocketIO instance
app, socketio = create_app()

# For PythonAnywhere, we need to use the app directly
# SocketIO will be handled by the static file configuration
application = app

# Optional: Enable debug mode for development
if __name__ == "__main__":
    # This won't run on PythonAnywhere, but useful for local testing
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
