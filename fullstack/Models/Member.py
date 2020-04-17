# coding: utf-8
from fullstack import db
from sqlalchemy import Column, DateTime, Integer, String, Numeric
from sqlalchemy.schema import FetchedValue




class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(11), nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    avatar = db.Column(db.String(200), nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    reg_ip = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    remain = db.Column(db.Numeric(10, 2), nullable=False)

