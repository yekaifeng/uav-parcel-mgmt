# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from app import db


class ModelExample(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(250))
	content = db.Column(db.Text)
	date = db.Column(db.DateTime)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(500))
    email = db.Column(db.String(120), unique = True)
    # posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __init__(self, user):
        self.user = user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Parcel(db.Model):
    __tablename__ = 'parcel'
    attributes = ['id', 'package_id', 'package_status', 'created_office',
                  'customer_name', 'customer_phone', 'customer_address',
                  'create_pkg_time', 'send_pkg_time', 'receive_pkg_time',
                  'sign_reject_time', 'last_update_by', 'uav_name']
    id = db.Column(db.Integer, primary_key = True)
    package_id = db.Column(db.String(64), unique = True, nullable=False)
    package_status = db.Column(db.String(16))
    created_office = db.Column(db.String(16))
    customer_name = db.Column(db.String(32), nullable=False)
    customer_phone = db.Column(db.String(32))
    customer_address = db.Column(db.String(128))
    create_pkg_time = db.Column(db.DateTime)
    send_pkg_time = db.Column(db.DateTime)
    receive_pkg_time = db.Column(db.DateTime)
    sign_reject_time = db.Column(db.DateTime)
    date = db.Column(db.Date)
    last_update_by = db.Column(db.String(32))
    uav_name = db.Column(db.String(32))
    CONST_PKG_STATUS = {'received':u'已接单', 'depart':u'已发件', 'arrival':u'已代收',
                    'signed':u'已签收','reject':u'拒收','return':u'退回'}

    def __init__(self, package_id, customer_name, customer_phone, office,
                last_update_by, create_time, create_date,
                package_status=CONST_PKG_STATUS['received']):
        self.package_id = package_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.package_status = package_status
        self.created_office = office
        self.last_update_by = last_update_by
        self.create_pkg_time = create_time
        self.date = create_date

    def __repr__(self):
        return '<Package %r>' % (self.package_id)

class Uav(db.Model):
    __tablename__ = 'uav'
    attributes = ['id', 'uav_id', 'name', 'type', 'load', 'vendor']
    id = db.Column(db.Integer, primary_key = True)
    uav_id = db.Column(db.String(64), unique = True, nullable=False)
    name = db.Column(db.String(32))
    type = db.Column(db.String(16))
    load = db.Column(db.String(16))
    vendor = db.Column(db.String(16))

    def __init__(self, uav_id, name):
        self.uav_id = uav_id
        self.name = name

    def __repr__(self):
        return '<Uav %r>' % (self.uav_id)
