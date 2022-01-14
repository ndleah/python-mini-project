import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sqlite'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_products(products_id):
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE id = ?',
                            (products_id,)).fetchone()
    conn.close()
    if products is None:
        abort(404)
    return products


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        if not title:
            flash('Title is required!')
        elif not price:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO products (title, price) VALUES (?, ?)', (title, price))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    products = get_products(id)

    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        if not title:
            flash('Title is required!')

        elif not price:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE products SET title = ?, price = ?'
                         ' WHERE id = ?',
                         (title, price, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', products=products)


@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    products = get_products(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(products['title']))
    return redirect(url_for('index'))


@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)
