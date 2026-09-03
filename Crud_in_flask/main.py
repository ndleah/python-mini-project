import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sqlite'

def get_db_connection():
    """Get SQLite connection and ensure products table schema exists."""
    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, 'database.db')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Ensure products table exists
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    return conn

def get_products(products_id):
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE id = ?', (products_id,)).fetchone()
    conn.close()
    if products is None:
        abort(404)
    return products

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')

        if not title:
            flash('Title is required!')
        elif not price:
            flash('Price is required!')
        else:
            try:
                price_val = float(price)
                conn = get_db_connection()
                conn.execute('INSERT INTO products (title, price) VALUES (?, ?)', (title, price_val))
                conn.commit()
                conn.close()
                flash('Product created successfully!')
                return redirect(url_for('index'))
            except ValueError:
                flash('Price must be a valid number!')

    return render_template('create.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    products = get_products(id)

    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')

        if not title:
            flash('Title is required!')
        elif not price:
            flash('Price is required!')
        else:
            try:
                price_val = float(price)
                conn = get_db_connection()
                conn.execute('UPDATE products SET title = ?, price = ? WHERE id = ?', (title, price_val, id))
                conn.commit()
                conn.close()
                flash('Product updated successfully!')
                return redirect(url_for('index'))
            except ValueError:
                flash('Price must be a valid number!')

    return render_template('edit.html', products=products)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    products = get_products(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash(f'"{products["title"]}" was successfully deleted!')
    return redirect(url_for('index'))

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)

