from flask import Flask
import azure.functions as func
from main import PaperTrading  # Import existing trading logic

app = Flask(__name__)
trading_system = PaperTrading()

@app.route('/')
def health_check():
    return "Trading System Operational", 200

@app.route('/balance')
def get_balance():
    return {'balance': trading_system.get_balance()}, 200

@app.route('/positions')
def get_positions():
    return {'positions': trading_system.get_positions()}, 200

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.WSGIHandler(app).handle(req, context)
