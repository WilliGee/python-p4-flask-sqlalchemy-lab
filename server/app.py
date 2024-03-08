#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)


@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get_or_404(id)
    response_body = f'''
        <h1>Information for {animal.name}</h1>
        <h2>Species: {animal.species}</h2>
        <h2>Zookeeper: {animal.zookeeper.name}</h2>
        <h2>Enclosure: {animal.enclosure.environment}</h2>
    '''
    return make_response(response_body, 200)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get_or_404(id)
    response_body = f'''
        <h1>Information for Zookeeper {zookeeper.name}</h1>
        <h2>Birthday: {zookeeper.birthday}</h2>
        <h2>Animals under care:</h2>
        <ul>
    '''
    for animal in zookeeper.animals:
        response_body += f'<li>{animal.name} ({animal.species})</li>'
    response_body += '</ul>'
    return make_response(response_body, 200)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get_or_404(id)
    response_body = f'''
        <h1>Information for Enclosure</h1>
        <h2>Environment: {enclosure.environment}</h2>
        <h2>Open to Visitors: {enclosure.open_to_visitors}</h2>
        <h2>Animals in enclosure:</h2>
        <ul>
    '''
    for animal in enclosure.animals:
        response_body += f'<li>{animal.name} ({animal.species})</li>'
    response_body += '</ul>'
    return make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
