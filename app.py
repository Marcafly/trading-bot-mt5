from flask import Flask, render_template, request, jsonify
import threading
import time
import random
from datetime import datetime
import os

app = Flask(__name__)

# Estado global - MUY SIMPLE
bot_active = False
balance = 10000.0
total_profit = 0.0
orders_count = 0

def trading_bot_worker():
    """Trabajador del bot - SUPER SIMPLE"""
    global bot_active, balance, total_profit, orders_count
    
    print("🤖 BOT INICIADO - Trabajando...")
    
    while bot_active:
        try:
            # Simular una operación de trading
            profit = random.uniform(-8, 12)  # Puede ganar o perder
            balance += profit
            total_profit += profit
            orders_count += 1
            
            # Log en el servidor
            current_time = datetime.now().strftime("%H:%M:%S")
            operation = "COMPRA" if profit > 0 else "VENTA"
            print(f"✅ {current_time} | {operation} | Ganancia: {profit:+.2f} | Balance: {balance:.2f}")
            
            # Esperar entre 3-8 segundos
            time.sleep(random.uniform(3, 8))
            
        except Exception as e:
            print(f"❌ Error en bot: {e}")
            time.sleep(5)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/toggle_bot', methods=['POST'])
def toggle_bot():
    """ÚNICO endpoint - Activa/desactiva TODO"""
    global bot_active
    
    try:
        if not bot_active:
            # ACTIVAR BOT (conecta e inicia automáticamente)
            bot_active = True
            
            # Iniciar el bot en un hilo separado
            thread = threading.Thread(target=trading_bot_worker)
            thread.daemon = True
            thread.start()
            
            print("🚀 BOT ACTIVADO - Conectado e iniciado automáticamente")
            
            return jsonify({
                'success': True,
                'message': '🚀 BOT ACTIVADO - Operando en EURUSD',
                'bot_active': True,
                'balance': round(balance, 2),
                'profit': round(total_profit, 2),
                'orders': orders_count
            })
        else:
            # DESACTIVAR BOT
            bot_active = False
            print("🛑 BOT DESACTIVADO")
            
            return jsonify({
                'success': True,
                'message': '🛑 BOT DESACTIVADO',
                'bot_active': False,
                'balance': round(balance, 2),
                'profit': round(total_profit, 2),
                'orders': orders_count
            })
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/get_status')
def get_status():
    """Obtener estado actual"""
    return jsonify({
        'bot_active': bot_active,
        'balance': round(balance, 2),
        'profit': round(total_profit, 2),
        'orders': orders_count
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
