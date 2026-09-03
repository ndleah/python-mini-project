from flask import Flask, request, render_template, redirect, url_for, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'todo-secret'

try:
    from flask_bootstrap import Bootstrap
    bootstrap = Bootstrap(app)
except ImportError:
    print("Notice: flask_bootstrap library not installed. Running without Bootstrap extension.")

todos = []

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('todo', '').strip()
    if task:
        todos.append({"task": task, "done": False})
    return redirect(url_for('index'))

@app.route('/remove/<int:index>', methods=['GET', 'POST'])
def remove(index):
    if 0 <= index < len(todos):
        del todos[index]
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if not (0 <= index < len(todos)):
        return redirect(url_for('index'))

    if request.method == 'GET':
        todo = todos[index]
        return render_template('edit.html', todo=todo, index=index)
    else:
        task = request.form.get('todo', '').strip()
        if task:
            todos[index]['task'] = task
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

