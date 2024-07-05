from flask import Flask
from routes.cart_routes import cart_blueprint
from routes.account_routes import account_blueprint
from routes.views_routes import views_blueprint
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def register_blueprints(app: Flask):
    app.register_blueprint(cart_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(views_blueprint)

