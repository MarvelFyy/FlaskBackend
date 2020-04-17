# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.schema import FetchedValue
from fullstack import db



class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(100, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    priced = db.Column(db.Numeric(10, 2), nullable=False)
    imageName = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False)
    imageURL = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    description = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    stock = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    cover = db.Column(db.Integer, nullable=False)
    month_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    view_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    comment_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
