# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from fullstack import db



class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
