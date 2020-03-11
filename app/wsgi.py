from collections import defaultdict
from lib.flask_extended import Flask
from flask import render_template, session, redirect, url_for, request
from jinja2 import Template

app = Flask(__name__)
app.config.from_yaml('/data/config.yml')
app.config['index_pool'] = iter(range(1, int(app.config['USER_COUNT']) + 1))
app.config['index_map'] = {}
app.config['roster'] = defaultdict(lambda: {"name": "EMPTY"})

@app.route('/')
def index():
    if session.get('userid'):
        if session['userid'] != -1:
            update_roster(session['index'], \
                session['email'], session['title'], session['name'])
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and \
            request.form['inputPassword'] == app.config['USER_PASS']:
        session['email'] = request.form['inputEmail']
        session['userid'] = hash(session['email'].lower())
        session['title'] = request.form['inputTitle']
        session['name'] = request.form['inputName']
        session['index'] = get_index(session['userid'])
        session['admin'] = False
        return redirect('/')

    elif request.method == 'POST' and \
            request.form['inputPassword'] == app.config['ADMIN_PASS']:
        session['admin'] = True
        session['userid'] = -1
        session['index'] = int(app.config['USER_COUNT'])
        session['email'] = None
        session['title'] = None
        session['name'] = 'root'
        return redirect('/')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session['email'] = None
    session['userid'] = None
    session['title'] = None
    session['name'] = None
    session['index'] = None
    session['admin'] = None
    return redirect('/')

@app.route('/roster')
def roster():
    return repr(app.config['roster'])

def get_index(userid):
    uidx = app.config['index_map'].get(userid)
    if not uidx:
        try:
            uidx = next(app.config['index_pool'])
        except StopIteration:
            uidx = None
        app.config['index_map'][userid] = uidx
    return uidx

def update_roster(index, email, title, name):
    app.config['roster'].update(
        {index: {"email": email, "title": title, "name": name}})

@app.template_filter('render')
def render(value):
    return Template(value).render(session)
