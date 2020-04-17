import requests,hashlib,uuid,json,datetime
import xml


class PayService():
    def __init__(self):
        pass

    def create_sign(self,pay_data):
        '''
        生产签名
        :param pay_data
        :return
        '''
        stringA="&".join(["{0}={1}".format(k,pay_data.get(k)) for k in sorted(pay_data)])
        
    
    def get_pay_info(self):
        pass
