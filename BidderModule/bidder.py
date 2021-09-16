from tornado import gen, web
import random
from baseHandler import BaseHandler,MAXPRICE, ID
class DoBidding(BaseHandler):
    @gen.coroutine
    def get(self):
        price = round(random.uniform(1, MAXPRICE),2)
        self.build_response({"bidder_id": ID,"bid_value":price},200)