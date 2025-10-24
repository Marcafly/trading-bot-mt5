from flask import Flask, render_template, request, jsonify
import threading
import time
import random
from datetime import datetime

app = Flask(__name__)

# Simulación de MetaTrader5
class MockMT5:
    def __init__(self):
        self.connected = False
        self.prices = {
            "EURUSD": 1.0850,
            "GBPUSD": 1.2650,
            "USDJPY": 149.50,
            "XAUUSD": 1980.50
        }
    
    def initialize(self):
        print("✅ MT5 Simulado - Inicializado")
        return True
    
    def login(self, account, password, server):
        print(f"✅ MT5 Simulado - Login: account={account}, server={server}")
        self.connected = True
        return True
    
    def symbol_info_tick(self, symbol):
        # Simular fluctuación de precios
        if symbol in self.prices:
            change = random.uniform(-0.0010, 0.0010)
            self.prices[symbol] += change
            self.prices[symbol] = round(self.prices[symbol], 4)
        
        class Tick:
            def __init__(self, price):
                self.bid = price
                self.ask = price + 0.0002
                self.last = price
                self.volume = random.randint(100, 1000)
        
        return Tick(self.prices.get(symbol, 1.0850))
    
    def order_send(self, request):
        print(f"📊 Orden simulada: {request}")
        
        class Result:
            def __init__(self, success=True):
                self.retcode = 10009 if success else 10018
                self.order = random.randint(100000, 999999)
                self.volume = request.get('volume', 0.01)
                self.price = request.get('price', 1.0850)
                self.comment = "Orden simulada - Demo"
        
        success = random.random() > 0.05
        return Result(success)

# Instancia global de MT5 simulado
mock_mt5 = MockMT5()

# Configuración inicial del Bot
class TradingBot:
    def __init__(self):
        self.is_running = False
        self.symbol = "EURUSD"
        self.lotage = 0.01
        self.connection_status = False
        self.orders_count = 0
        self.balance = 10000.0
        self.total_profit = 0.0
        
    def connect_mt5(self):
        """Conectar con MetaTrader 5 Simulado"""
        try:
            if not mock_mt5.initialize():
                return False
            
            account = 12345678
            password = "password_demo"
            server = "BrokerDemo-Server"
            
            authorized = mock_mt5.login(account, password=password, server=server)
            if authorized:
                self.connection_status = True
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def simple_strategy(self):
        """Estrategia simple de compra/venta - MODO SIMULACIÓN"""
        print("🚀 Iniciando estrategia de trading simulada...")
        
        while self.is_running:
            try:
                # Obtener precio actual simulado
                tick = mock_mt5.symbol_info_tick(self.symbol)
                current_price = tick.bid
                
                # ESTRATEGIA MEJORADA - Más realista
                signal = self.generate_signal(current_price)
                
                if signal == 'buy' and self.orders_count < 10:
                    success = self.place_order("buy", current_price)
                    if success:
                        self.orders_count += 1
                elif signal == 'sell' and self.orders_count < 10:
                    success = self.place_order("sell", current_price)
                    if success:
                        self.orders_count += 1
                
                # Log de monitoreo
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"⏰ {current_time} | {self.symbol}: {current_price:.4f} | Señal: {signal} | Órdenes: {self.orders_count}")
                
                time.sleep(15)  # Revisar cada 15 segundos
                
            except Exception as e:
                print(f"❌ Error en estrategia: {e}")
                time.sleep(10)
    
    def generate_signal(self, current_price):
        """Generar señal de trading más inteligente"""
        # Estrategia basada en tendencia simulada
        trend = random.choice(['up', 'down', 'sideways'])
        
        if trend == 'up':
            return 'buy' if random.random() > 0.3 else 'hold'
        elif trend == 'down':
            return 'sell' if random.random() > 0.3 else 'hold'
        else:
            return 'hold'
    
    def place_order(self, order_type, price):
        """Ejecutar orden de trading simulada"""
        try:
            request = {
                "action": "TRADE_ACTION_DEAL",
                "symbol": self.symbol,
                "volume": self.lotage,
                "type": "BUY" if order_type.lower() == "buy" else "SELL",
                "price": price,
            }
            
            result = mock_mt5.order_send(request)
            
            if result.retcode == 10009:
                profit_loss = random.uniform(-2, 8)
                self.balance += profit_loss
                self.total_profit += profit_loss
                
                print(f"✅ Orden {order_type} | Precio: {price:.4f} | P&L: {profit_loss:+.2f} | Balance: {self.balance:.2f}")
                return True
            else:
                print(f"❌ Error en orden {order_type}")
                return False
                
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
        return jsonify({"status": "success", "message": "✅ Conectado a MT5 Simulado"})
    else:
        return jsonify({"status": "error", "message": "❌ Error de conexión MT5"})

@app.route('/start', methods=['POST'])
def start_bot():
    if not bot.connection_status:
        return jsonify({"status": "error", "message": "⚠️ Primero conecta a MT5"})
    
    bot.is_running = True
    thread = threading.Thread(target=bot.simple_strategy)
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "success", "message": "🚀 Bot iniciado - Modo Simulación"})

@app.route('/stop', methods=['POST'])
def stop_bot():
    bot.is_running = False
    return jsonify({"status": "success", "message": "🛑 Bot detenido"})

@app.route('/status')
def get_status():
    return jsonify({
        "running": bot.is_running,
        "connected": bot.connection_status,
        "symbol": bot.symbol,
        "balance": round(bot.balance, 2),
        "orders_count": bot.orders_count,
        "total_profit": round(bot.total_profit, 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
