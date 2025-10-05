#!/usr/bin/python3
"""
Arquivo principal para Replit
"""

import os
import sys

# Adiciona o diretório atual ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Cria a aplicação Flask
app = create_app()

if __name__ == "__main__":
    # Replit usa a porta da variável de ambiente PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)









