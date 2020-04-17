import decimal
import hashlib
import time
import random
from fullstack import db, app
from fullstack.Models.Food import Food
from fullstack.Models.PaymentOrder import PaymentOrder
from fullstack.Models.PaymentOrderItem import PaymentOrderItem
from fullstack.Models.PaymentOrderCallbackData import PaymentOrderCallbackData
from fullstack.WeChat.Service.FoodService import FoodService
from fullstack.utils import getCurrentTime, getDictFilterField, selectFilterObj


class PaymentService():
    def __init__(self):
        pass

    def createOrder(self, member_id, items=None, params=None):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}

        # 参数有效性判断
        pay_price = decimal.Decimal(0.00)
        continue_count = 0
        food_ids = []
        print(items)
        for item in items:
            if decimal.Decimal(item['price']) < 0:
                continue_count += 1
                continue

            pay_price = pay_price + \
                decimal.Decimal(item['price'])*int(item['number'])
            food_ids.append(item['id'])

        if continue_count >= len(items):
            response['code'] = -1
            response['msg'] = "商品items为空空"
            return response

        # 备注
        yun_price = params['yun_price'] if params and 'yun_price' in params else 0
        note = params['note'] if params and 'note' in params else 0  # 备注
        total_price = pay_price+yun_price

        # 并发操作 悲观锁
        # 利用数据库事务自带加锁功能 缺点是比较消耗数据库性能
        try:
            temp_food_list = db.session.query(Food).filter(Food.id.in_(food_ids))\
                .with_for_update().all()
            temp_food_stock_mapping = {}
            for item in temp_food_list:
                temp_food_stock_mapping[item.id] = item.stock

            paymentOrder = PaymentOrder()
            # 订单编号
            paymentOrder.order_sn = self.geneOrderSn()
            paymentOrder.member_id = member_id
            paymentOrder.total_price = total_price
            paymentOrder.yun_price = yun_price
            paymentOrder.pay_price = pay_price
            paymentOrder.note = note
            paymentOrder.status = -8  # -8 待支付
            paymentOrder.express_status = -8  # -8待支付
            paymentOrder.updated_time = paymentOrder.created_time = getCurrentTime()
            db.session.add(paymentOrder)

            for item in items:
                tmp_left_stock = temp_food_stock_mapping[item['id']]

                if decimal.Decimal(item['price']) < 0:
                    continue

                if int(item['number']) > int(tmp_left_stock):
                    raise Exception("该商品库存为%s,您要购买%s" %(tmp_left_stock, item['number']))

                tmp_ret = Food.query.filter_by(id=item['id']).update({"stock": int(tmp_left_stock) - int(item['number'])
                    })

                if not tmp_ret:
                    raise Exception("下单失败请重新下单")

                paymentOrderItem = PaymentOrderItem()
                paymentOrderItem.pay_order_id = paymentOrder.id
                paymentOrderItem.member_id = member_id
                paymentOrderItem.quantity = item['number']
                paymentOrderItem.price = item['price']
                paymentOrderItem.food_id = item['id']
                paymentOrderItem.note = note
                paymentOrderItem.updated_time = paymentOrderItem.created_time = getCurrentTime()
                db.session.add(paymentOrderItem)

                FoodService.setStockChangeLog(item['id'],-item['number'],"提交订单")

            db.session.commit()

            response['data'] = {
                'id': paymentOrder.id,
                'order_sn': paymentOrder.order_sn,
                'total_price': str(total_price)
            }
        except Exception as e:
            db.session.rollback()
            print('回滚')
            response['code'] = -1
            response['msg'] = "下单失败请重试"
            response['msg'] = str(e)

        return response

    # 生成订单编码 使用MD5

    def geneOrderSn(self):
        m = hashlib.md5()
        sn = None
        while True:
            str = "%s-%s" % (int(round(time.time()+1000)),random.randint(0, 9999999))
            m.update(str.encode("utf-8"))
            sn = m.hexdigest()
            if not PaymentOrder.query.filter_by(order_sn=sn).first():
                break

        return sn
