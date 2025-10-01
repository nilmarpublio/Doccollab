#!/usr/bin/python3
"""
Arquivo principal para PythonAnywhere
"""

import os
import sys

# Adiciona o diretório atual ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Cria a aplicação Flask
application = create_app()

if __name__ == "__main__":
    application.run()


