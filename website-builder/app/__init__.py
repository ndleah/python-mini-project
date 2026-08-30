from flask import Flask, redirect, url_for
from .routes import portfolio_routes
from config import DevelopmentConfig, ProductionConfig


def create_app():
    app = Flask(__name__)

    # Choose the configuration based on your environment
    app.config.from_object(DevelopmentConfig)  # For development environment
    # Uncomment the line below for production environment
    app.config.from_object(ProductionConfig)

    # Register the blueprint
    app.register_blueprint(portfolio_routes.portfolio_bp,
                           url_prefix='/portfolio')

    @app.route('/')
    def index():
        return redirect(url_for('portfolio.create_portfolio'))

    return app

