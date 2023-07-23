from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap

#create the app
app = Flask(__name__)
bootstrap = Bootstrap(app)

#the database
todos = []
#routes
@app.route('/')
def index():
    return render_template('index.html', todos=todos)
@app.route('/add', methods=['POST'])
def add():
    task = request.form['todo']
    todos.append({"task":task, "done":False})
    return redirect(url_for('index'))
@app.route('/remove/<int:index>', methods=['GET'])
def remove(index):
    del todos[index]
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if request.method == 'GET':
        todo = todos[index]
        return render_template('edit.html', todo=todo, index=index)
    else:
        task = request.form['todo']
        todo = todos[index]
        todo['task'] = task
        return redirect(url_for('index'))

#run the app
app.run(debug=True)
