from flask import Flask, request, jsonify
import threading
import time
import random
from datetime import datetime
import os

# Intentar importar MetaTrader5
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
    print("✅ MetaTrader5 disponible - Intentando conexión real")
except ImportError:
    MT5_AVAILABLE = False
    print("⚠️ MetaTrader5 no disponible - Modo simulación activado")

app = Flask(__name__)

# CONFIGURACIÓN REAL DE MT5 - TUS DATOS
MT5_CONFIG = {
    'account': 96707413,           # Tu número de cuenta
    'password': 'L-4aGtWq',        # Tu contraseña trader
    'server': 'MetaQuotes-Demo',   # Tu servidor
    'symbol': 'EURUSD',            # Confirmado en tu captura
    'lotage': 0.01,                # Tamaño de lote pequeño para demo
    'magic': 96707413              # Usamos tu número de cuenta como magic
}

class TradingBot:
    def __init__(self):
        self.running = False
        self.connected = False
        self.connection_type = "Simulación"  # "Real" o "Simulación"
        self.balance = 10000.0
        self.equity = 10000.0
        self.orders_count = 0
