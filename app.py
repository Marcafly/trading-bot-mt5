from flask import Flask, render_template, request, jsonify
import threading
import time
import random
from datetime import datetime

app = Flask(__name__)

class TradingBot:
    def __init__(self):
        self.is_running = False
        self.connection_status = False
        self.balance = 10000.0
        self.total_profit = 0.0
        self.orders_count = 0
        self.symbol = "EURUSD"
        
    def connect_and_start(self):
        """Conectar y empezar TODO automáticamente"""
        try:
            print("🔄 INICIANDO CONEXIÓN AUTOMÁTICA...")
            
            # Simular conexión a MT5
            time.sleep(2)  # Simular tiempo de conexión
            self.connection_status = True
            print("✅ CONEXIÓN MT5 SIMULADA - EXITOSA")
            
            # Iniciar estrategia automáticamente
            self.is_running = True
            print("🚀 ESTRATEGIA INICIADA AUTOMÁTICAMENTE")
            
            # Ejecutar estrategia en segundo plano
            thread = threading.Thread(target=self.trading_strategy)
            thread.daemon = True
            thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def trading_strategy(self):
        """Estrategia de trading automática y simple"""
        print("🤖 ESTRATEGIA ACTIVA - OPERANDO...")
        
        while self.is_running:
            try:
                # Simular precio actual
                current_price = 1.0850 + random.uniform(-0.0050, 0.0050)
                current_price = round(current_price, 4)
                
                # Generar señal de trading (más frecuente)
                signal = random.choices(
                    ['COMPRA', 'VENTA', 'ESPERAR'], 
                    weights=[0.4, 0.4, 0.2], 
                    k=1
                )[0]
                
                if signal in ['COMPRA', 'VENTA'] and self.orders_count < 15:
                    # Ejecutar orden
                    profit = random.uniform(-3, 8)
                    self.balance += profit
                    self.total_profit += profit
                    self.orders_count += 1
                    
                    # Log detallado
                    current_time = datetime.now().strftime("%H:%M:%S")
                    log_msg = f"⏰ {current_time} | {signal} | EURUSD: {current_price} | Ganancia: {profit:+.2f} | Balance: {self.balance:.2f}"
                    print(log_msg)
                
                # Espera más corta para más acción
                time.sleep(8)  # 8 segundos entre operaciones
                
            except Exception as e:
                print(f"⚠️ Error en estrategia: {e}")
                time.sleep(5)
    
    def stop_all(self):
        """Detener todo"""
        self.is_running = False
        self.connection_status = False
        print("🛑 BOT DETENIDO")
        return True

# Instancia global del bot
bot = TradingBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auto_start', methods=['POST'])
def auto_start():
    """Un solo endpoint que hace TODO"""
    try:
        success = bot.connect_and_start()
        if success:
            return jsonify({
                "status": "success", 
                "message": "✅ CONEXIÓN EXITOSA | 🤖 BOT OPERANDO",
                "balance": round(bot.balance, 2),
                "profit": round(bot.total_profit, 2),
                "orders": bot.orders_count
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "❌ ERROR AL INICIAR"
            })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"❌ ERROR: {str(e)}"
        })

@app.route('/auto_stop', methods=['POST'])
def auto_stop():
    """Detener todo"""
    try:
        bot.stop_all()
        return jsonify({
            "status": "success", 
            "message": "🛑 BOT DETENIDO",
            "balance": round(bot.balance, 2),
            "profit": round(bot.total_profit, 2),
            "orders": bot.orders_count
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"❌ ERROR AL DETENER: {str(e)}"
        })

@app.route('/get_status')
def get_status():
    """Obtener estado actual"""
    return jsonify({
        "running": bot.is_running,
        "connected": bot.connection_status,
        "balance": round(bot.balance, 2),
        "profit": round(bot.total_profit, 2),
        "orders": bot.orders_count,
        "symbol": bot.symbol
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
