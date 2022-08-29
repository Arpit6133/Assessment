from flask import Flask, request, jsonify, render_template
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_paginate import Pagination, get_page_args
import os
import datetime

# Init app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:Arpit@localhost/assessment"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False






    

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class user_master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    contact_number = db.Column(db.Integer)
    email_id = db.Column(db.String(50))
    blood_group = db.Column(db.String(2))
    city_id = db.Column(db.Integer)
    added_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<user_master %s>' % self.name


class city_master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50))
    city_state = db.Column(db.String(50))
    added_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<city_master %s>' % self.city_name


class user_masterSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "contact_number", "email_id", "blood_group",
                  "city_id", "added_date")


user_master_schema = user_masterSchema()
users_master_schema = user_masterSchema(many=True)


class city_masterSchema(ma.Schema):
    class Meta:
        fields = ("id", "city_name", "city_state", "added_date")


city_master_schema = city_masterSchema()
cities_master_schema = city_masterSchema(many=True)


class user_masterListResource(Resource):
    def get(self):
        users_master = user_master.query.all()
        rows = users_master_schema.dump(users_master)
        d = {"total": len(rows),
            "totalNotFiltered":len(rows),
            "rows":rows}
        return d

    def post(self):
        new_user_master = user_master(
            name=request.json['name'],
            contact_number=request.json['contact_number'],
            email_id=request.json['email_id'],
            blood_group=request.json['blood_group'],
            city_id=request.json['city_id'],
            added_date=datetime.datetime.now()
        )
        db.session.add(new_user_master)
        db.session.commit()
        return user_master_schema.dump(new_user_master)




class city_masterListResource(Resource):
    def get(self):
        cities_master = city_master.query.all()
        return cities_master_schema.dump(cities_master)

    def post(self):
        new_city_master = city_master(
            id=request.json['id'],
            city_name=request.json['city_name'],
            city_state=request.json['city_state'],
            added_date=request.json['added_date']
        )
        db.session.add(new_city_master)
        db.session.commit()
        return city_master_schema.dump(new_city_master)


class user_masterResource(Resource):
    def get(self, user_master_id):
        user_master_with_id = user_master.query.get_or_404(user_master_id)
        return user_master_schema.dump(user_master_with_id)

    def post(self):
        new_user_master = user_master(
            name=request.json['name'],
            contact_number=request.json['contact_number'],
            email_id=request.json['email_id'],
            blood_group=request.json['blood_group'],
            city_id=request.json['city_id'],
            added_date=datetime.datetime.now()
        )
        db.session.add(new_user_master)
        db.session.commit()
        return user_master_schema.dump(new_user_master)

    def put(self, user_master_id, contact_number):
        user_master_contact = user_master.query.get_or_404(user_master_id)

        if 'contact_number' in request.json:
            user_master_contact.contact_number = request.json['contact_number']

        db.session.commit()


class city_masterResource(Resource):
    def get(self, city_master_id):
        city_master_with_id = city_master.query.get_or_404(city_master_id)
        return city_master_schema.dump(city_master_with_id)

    def post(self):
        new_city_master = city_master(
            city_name=request.json['city_name'],
            city_state=request.json['city_state'],
            added_date=datetime.datetime.now()
        )
        db.session.add(new_city_master)
        db.session.commit()
        return city_master_schema.dump(new_city_master)


api.add_resource(user_masterResource, '/user_master/<int:user_master_id>/')
api.add_resource(user_masterListResource, '/users_master/')
api.add_resource(city_masterResource, '/city_master/add')
api.add_resource(city_masterListResource, '/cities_master/')


@app.route('/')
def display_users():
    
    return render_template('index.html')


records = user_master.query.all()
rows = users_master_schema.dump(records)

total = len(records)
dict_user = {"total":total,
            "totalNotFiltered":total,
            "rows":rows}

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
