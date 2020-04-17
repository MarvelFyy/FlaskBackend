from fullstack import db, app
from fullstack.Models.Food import Food
from fullstack.Models.FoodStockChangeLog import FoodStockChangeLog
from fullstack.utils import getCurrentTime

class FoodService():

    @staticmethod
    def setStockChangeLog( food_id = 0,quantity = 0,note = '' ):

        if food_id<1:
            return False
        
        food_info=Food.query.filter_by(id=food_id).first()
        if not food_info:
            return False
        
        stockChange=FoodStockChangeLog()
        stockChange.food_id=food_id
        stockChange.unit=quantity
        stockChange.total_stock=food_info.stock
        stockChange.note=note
        stockChange.created_time=getCurrentTime()
        db.session.add(stockChange)
        db.session.commit()

        return True
