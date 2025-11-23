"""
Configuração pytest para testes de aceitação.
Adiciona o diretório src ao path do Python antes de executar os testes.
"""

import sys
import os

# Adiciona o diretório src ao path ANTES de qualquer import dos módulos de teste
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
