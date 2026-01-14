import os
import sys
from datetime import datetime

# 1. Asegúrate de que Sphinx pueda encontrar tu código
sys.path.insert(0, os.path.abspath('../src'))

# 2. Importa la versión desde tu archivo de metadatos
# Importamos así para no tener que instalar el paquete durante la compilación de la docu
about = {}
with open(os.path.abspath('../src/pygeko/__about__.py')) as f:
    exec(f.read(), about)

project = 'pyGEKO'
copyright = f'{datetime.now().year}, Jesús Cabrera'
author = 'jccsvq@gmail.com'

# 3. Usa los valores extraídos
release = about['__version__']  # Ejemplo: '0.9.0rc1'
version = '.'.join(release.split('.')[:2])  # Extrae '0.9' automáticamente