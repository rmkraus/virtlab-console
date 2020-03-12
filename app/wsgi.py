from lib.flask_extended import Flask
from flask import render_template, session, redirect, url_for, request
from jinja2 import Template
from pymongo import MongoClient
from tabulate import tabulate

app = Flask(__name__)
app.config.from_yaml('/data/config.yml')

db = MongoClient().virtlab


@app.route('/')
def index():
    if session.get('_id'):
        roster = _get_roster(session['admin'])
        return render_template('index.html', roster=roster)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    err = ''
    if request.method == 'POST':
        (err, user) = _authenticate(request.form)
        if user:
            session.update(user)
            return redirect('/')
    return render_template('login.html', err=err)

@app.route('/logout')
def logout():
    session['email'] = None
    session['_id'] = None
    session['title'] = None
    session['name'] = None
    session['index'] = None
    session['admin'] = None
    return redirect('/')

@app.route('/roster')
def roster():
    roster = _get_roster(session['admin'])
    _ = [rec.pop('_id', None) for rec in roster]
    _ = [rec.pop('admin', None) for rec in roster]
    return tabulate(roster, headers="keys", tablefmt="html")

def _authenticate(answers):
    if answers['inputPassword'] == app.config['USER_PASS']:
        return _authorize(answers)
    elif answers['inputPassword'] == app.config['ADMIN_PASS']:
        return ('',
                {"admin": True,
                 "_id": -1,
                 "index": int(app.config['USER_COUNT']),
                 "email": None,
                 "title": None,
                 "name": "root"})
    return ('Invalid Credentials', {})

def _authorize(answers):
    user_id = hash(answers['inputEmail'].lower())
    user = db.roster.find_one({"_id": user_id})

    # register new user
    if not user:
        # get avialable student number
        next_index = _get_index()
        if not next_index:
            return ('The classroom is full.', {})
        # register student
        user = {"admin": False,
                "_id": user_id,
                "index": next_index,
                "email": answers['inputEmail'],
                "title": answers['inputTitle'],
                "name": answers['inputName']}
        db.roster.insert_one(user)

    return ('', user)

def _get_index():
    rec = db.index_pool.find_one_and_delete({})
    if rec:
        return rec['value']
    return None

def _get_roster(is_admin):
    if is_admin:
        return [rec for rec in db.roster.find({})]
    return [session]

@app.template_filter('render')
def render(value):
    return Template(value).render(session)
