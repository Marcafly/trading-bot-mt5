from flask import Flask, render_template, request, jsonify
import threading
import time
import random
from datetime import datetime
import os

app = Flask(__name__)

# Estado global simple
bot_state = {
    'running': False,
    'balance': 10000.0,
    'profit': 0.0,
    'orders': 0,
    'symbol': 'EURUSD'
}

def bot_worker():
    """Trabajador del bot - MUY SIMPLE"""
    while bot_state['running']:
        try:
            # Simular operación de trading
            if bot_state['orders'] < 20:  # Límite de órdenes
                # Precio simulado
                price = 1.0850 + random.uniform(-0.010, 0.010)
                price = round(price, 4)
                
                # Decisión simple: 50% compra, 50% venta
                if random.choice([True, False]):
                    operation = "COMPRA"
                    profit = random.uniform(1, 15)  # Más ganancias que pérdidas
                else:
                    operation = "VENTA" 
                    profit = random.uniform(-10, 5)  # Puede ganar o perder
                
                # Actualizar estado
                bot_state['balance'] += profit
                bot_state['profit'] += profit
                bot_state['orders'] += 1
                
                # Log en servidor
                print(f"✅ {datetime.now().strftime('%H:%M:%S')} | {operation} | EURUSD {price} | Ganancia: {profit:+.2f}")
            
            # Esperar 5-10 segundos
            time.sleep(random.uniform(5, 10))
            
        except Exception as e:
            print(f"❌ Error en bot: {e}")
            time.sleep(5)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/toggle_bot', methods=['POST'])
def toggle_bot():
    """Un solo endpoint para iniciar/detener"""
    try:
        if not bot_state['running']:
            # INICIAR BOT
            bot_state['running'] = True
            bot_state['orders'] = 0  # Resetear contador
            
            # Iniciar en hilo separado
            thread = threading.Thread(target=bot_worker)
            thread.daemon = True
            thread.start()
            
            print("🚀 BOT INICIADO - Operando automáticamente")
            return jsonify({
                'status': 'success',
                'message': '🚀 BOT ACTIVADO - Operando en EURUSD',
                'running': True,
                'balance': round(bot_state['balance'], 2),
                'profit': round(bot_state['profit'], 2),
                'orders': bot_state['orders']
            })
        else:
            # DETENER BOT
            bot_state['running'] = False
            print("🛑 BOT DETENIDO")
            return jsonify({
                'status': 'success', 
                'message': '🛑 BOT DETENIDO',
                'running': False,
                'balance': round(bot_state['balance'], 2),
                'profit': round(bot_state['profit'], 2),
                'orders': bot_state['orders']
            })
            
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        return jsonify({
            'status': 'error',
            'message': f'❌ Error: {str(e)}'
        })

@app.route('/get_state')
def get_state():
    """Obtener estado actual - MUY SIMPLE"""
    return jsonify({
        'running': bot_state['running'],
        'balance': round(bot_state['balance'], 2),
        'profit': round(bot_state['profit'], 2),
        'orders': bot_state['orders'],
        'symbol': bot_state['symbol']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
