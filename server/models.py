from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Apartment(db.Model, SerializerMixin):
    __tablename__ = 'apartments'
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer)
    name = db.Column(db.String)
    leases = db.relationship('Lease', back_populates='apartment')
    tenants = association_proxy('apartments', 'tenant')
    # include cascade if apartment needs to be deleted and everything else in association needs to be deleted


class Tenant(db.Model, SerializerMixin):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    leases = db.relationship('Lease', back_populates='tenant')
    tenants = association_proxy('apartments', 'tenant')

    @validates('name')
    def validates_name(self, key, name):
        if not name:
            raise ValueError("Name must be provided.")
        return name

    @validates('age')
    def validates_age(self, key, age):
        if age < 18:
            raise ValueError("Tenant must be 18 or older.")
        return age


class Lease(db.Model, SerializerMixin):
    __tablename__ = 'leases'
    id = db.Column(db.Integer, primary_key=True)
    rent = db.Column(db.Integer)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    tenant = db.relationship('Tenant', back_populates='leases')
    apartment = db.relationship('Apartment', back_populates='leases')
