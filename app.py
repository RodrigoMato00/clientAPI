from flask import Flask, request, render_template, redirect, url_for, session
import requests
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = 'bxc7xebxf3[xdb8^xaex92kx88x18/xbd$xbexc92=xc0yxcfx1bx98|'

def load_users():
    with open('users.json') as file:
        users = json.load(file)
    return users

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        user = next((u for u in users if u['name'] == username and u['password'] == password), None)
        if user:
            session['logged_in'] = True
            session['username'] = username
            session['stores'] = user.get('stores', [])
            session['is_admin'] = user.get('isAdmin', False)
            if session['is_admin']:
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('index'))
        else:
            return 'Login Failed'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('stores', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', stores=session.get('stores', []))

@app.route('/ask', methods=['POST'])
@login_required
def ask():
    store_name = request.form['storeName']
    if store_name not in session.get('stores', []):
        return "Access Denied", 403
    question = request.form['question']
    api_response = make_api_request(question, store_name)
    answer = api_response.get('answer', 'No response received')
    sources = api_response.get('sources', '')
    return render_template('index.html', answer=answer, question=question, store_name=store_name, sources=sources, stores=session.get('stores', []))

def make_api_request(question, store_name):
    url = "http://zonaprub.xyz:8000/answer/"
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': 'TuTokenCSRF'
    }
    data = {
        "makequestion": question,
        "storeName": store_name
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        user = next((u for u in users if u['name'] == username and u['password'] == password), None)
        if user and user.get('isAdmin'):
            session['logged_in'] = True
            session['username'] = username
            session['is_admin'] = True
            return redirect(url_for('admin_panel'))
        else:
            return 'Admin Login Failed'
    return render_template('admin_login.html')


def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if not session.get('is_admin', False):
        return 'Access Denied', 403

    users = load_users()
    if request.method == 'POST':
        new_user = {
            "name": request.form['username'],
            "password": request.form['password'],
            "stores": request.form.getlist('stores'),
            "isAdmin": request.form.get('is_admin') == 'on'
        }
        users.append(new_user)
        save_users(users)
        return redirect(url_for('admin_panel'))

    return render_template('admin_panel.html', users=users)

@app.route('/admin/edit_user/<username>', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    if not session.get('is_admin', False):
        return 'Access Denied', 403

    users = load_users()
    user = next((u for u in users if u['name'] == username), None)

    if user is None:
        return 'User not found', 404

    if request.method == 'POST':
        user['password'] = request.form['password']
        user['stores'] = request.form.getlist('stores')
        user['isAdmin'] = request.form.get('is_admin') == 'on'
        save_users(users)
        return redirect(url_for('admin_panel'))

    return render_template('edit_user.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
