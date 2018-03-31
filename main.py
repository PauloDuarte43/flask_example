#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
db = SQLAlchemy(app)


class Base(object):
    def to_dict(self):
        columns = [column.key for column in getattr(self, '__table__').columns]
        columns_values = dict(
            [(str(column), getattr(self, column)) for column in columns])
        return columns_values


class Client(db.Model, Base):
    __tablename__ = 'client'

    client_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

db.drop_all()
db.create_all()

new_client = Client()
new_client.username = "teste"
new_client.email = "teste@teste.com"
db.session.add(new_client)
db.session.commit()

new_client2 = Client()
new_client2.username = "teste2"
new_client2.email = "teste2@teste.com"
db.session.add(new_client2)
db.session.commit()



@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/api/client', methods=['GET', 'POST'])
def api_client():
    if request.method == 'POST':
        client = db.session.query(Client).filter(Client.client_id == request.form['client_id']).first()
        if client:
            client = client.to_dict()
        else:
            client = {}
        return jsonify(client)
    else:
        client = db.session.query(Client).all()
        if client:
            client = [c.to_dict() for c in client]
        return jsonify(client)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True, threaded=True)
