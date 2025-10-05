#!/usr/bin/python3
import sys
import os

# Adiciona o diretório do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Cria a aplicação Flask e SocketIO
app, socketio = create_app()

# Para produção, usamos apenas o app Flask
# O SocketIO será configurado via static files
application = app

if __name__ == "__main__":
    # Para desenvolvimento local
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)








