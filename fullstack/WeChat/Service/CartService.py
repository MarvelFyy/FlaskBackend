import hashlib
import requests
import random
import string
import json
from fullstack import app, db
from fullstack.Models.ShoppingCart import ShoppingCart
from fullstack.utils import getCurrentTime


class CartService():

    @staticmethod
    def deleteItem(member_id=0, items=None):
        if member_id < 1 or not items:
            return False
        for item in items:
            ShoppingCart.query.filter_by(
                food_id=item['id'], member_id=member_id).delete()
        db.session.commit()
        return True

    @staticmethod
    def setItems(member_id=0, food_id=0, number=0):
        if member_id < 1 or food_id < 1 or number < 1:
            return False
        cart_info = ShoppingCart.query.filter_by(
            food_id=food_id, member_id=member_id).first()
        if cart_info:
            model_cart = cart_info
        else:
            model_cart = ShoppingCart()
            model_cart.member_id = member_id
            model_cart.created_time = getCurrentTime()

        model_cart.food_id = food_id
        model_cart.quantity = number
        model_cart.updated_time = getCurrentTime()
        db.session.add(model_cart)
        db.session.commit()
        return True

