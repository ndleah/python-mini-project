from flask import Blueprint, render_template

portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/create')
def create_portfolio():
    # Your code for creating a portfolio goes here
    return render_template('create_portfolio.html')  # Render the HTML template


@portfolio_bp.route('/edit/<int:portfolio_id>')
def edit_portfolio(portfolio_id):
    # Your code for editing a portfolio goes here
    return render_template('edit_portfolio.html')  # Render the HTML template
