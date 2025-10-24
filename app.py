from flask import Flask, render_template, request, jsonify
import MetaTrader5 as mt5
import pandas as pd
import threading
import time
import os

app = Flask(__name__)

# Configuración inicial
class TradingBot:
    def __init__(self):
        self.is_running = False
        self.symbol = "EURUSD"
        self.lotage = 0.01
        self.connection_status = False
        
    def connect_mt5(self):
        """Conectar con MetaTrader 5"""
        try:
            if not mt5.initialize():
                print("Error al inicializar MT5")
                return False
            
            # CONFIGURA TUS DATOS AQUÍ (los pondremos después)
            account = 12345678  # Cambiar por tu cuenta real
            password = "tu_password"  # Cambiar por tu password real
            server = "tu_servidor"  # Cambiar por tu servidor real
            
            authorized = mt5.login(account, password=password, server=server)
            if authorized:
                self.connection_status = True
                print("✅ Conectado a MT5 Demo")
                return True
            else:
                print("❌ Error en login MT5")
                return False
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def simple_strategy(self):
        """Estrategia simple de compra/venta - MODO PRUEBA"""
        while self.is_running:
            try:
                print("🤖 Bot ejecutándose - Modo prueba...")
                
                # SIMULACIÓN - Aquí iría la lógica real de trading
                # Por ahora solo mostramos que está funcionando
                current_time = time.strftime("%H:%M:%S")
                print(f"⏰ {current_time} - Revisando mercado...")
                
                # Espera 30 segundos entre revisiones (modo prueba)
                time.sleep(30)
                
            except Exception as e:
                print(f"❌ Error en estrategia: {e}")
                time.sleep(10)
    
    def place_order(self, order_type):
        """Ejecutar orden de trading - MODO PRUEBA"""
        try:
            print(f"📊 Orden simulada: {order_type} {self.symbol}")
            # En modo real, aquí iría el código para enviar órdenes a MT5
            return True
                
        except Exception as e:
            print(f"❌ Error colocando orden: {e}")
            return False

# Instancia global del bot
bot = TradingBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    if bot.connect_mt5():
        return jsonify({"status": "success", "message": "✅ Conectado a MT5"})
    else:
        return jsonify({"status": "error", "message": "❌ Error de conexión MT5"})

@app.route('/start', methods=['POST'])
def start_bot():
    if not bot.connection_status:
        return jsonify({"status": "error", "message": "⚠️ Primero conecta a MT5"})
    
    bot.is_running = True
    # Ejecutar en hilo separado
    thread = threading.Thread(target=bot.simple_strategy)
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "success", "message": "🚀 Bot iniciado - Modo Prueba"})

@app.route('/stop', methods=['POST'])
def stop_bot():
    bot.is_running = False
    return jsonify({"status": "success", "message": "🛑 Bot detenido"})

@app.route('/status')
def get_status():
    return jsonify({
        "running": bot.is_running,
        "connected": bot.connection_status,
        "symbol": bot.symbol
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
