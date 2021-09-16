import json
from tornado import gen
import uuid
import baseHandler
from baseHandler import BaseHandler,RegisterBidder, \
                        AUCTIONEERLIST,BIDDERLIST, GetbidValue, ENDPOINT

# Add the auctioneer, when the service get started
class RootHandler:
    def addAuctioneer(num):
        for i in range(0,num):
            # actioneer = {"id":str(uuid.uuid4()),"name": "Auction {}".format(i+1)}
            actioneer = {"id":i,"name": "Auction {}".format(i+1)}
            AUCTIONEERLIST.append(actioneer)
        print(AUCTIONEERLIST)

class AuctioneerList(BaseHandler):
    def get(self):
        auction_list = AUCTIONEERLIST
        if len(auction_list)<1:
            self.build_response({"msg": "There is no Auctioneer"},204)
        else:
            self.build_response({"LiveAuctioneers":auction_list},200)

class AddBidder(BaseHandler):
    def put(self):
        request_body = json.loads(self.request.body)
        # There are the mandatory field to and take capital and small both
        print(request_body)
        port_no = request_body.get('port',8001)
        bidder_id = request_body.get('id',None)
        bid_url = request_body.get('url',"/getValue")
        name = request_body.get('name','')
        bid_url = ENDPOINT+str(port_no)+bid_url
        print("port: {0}  bidder_id: {1} bid_url: {2} name: {3}".format(port_no,bidder_id,bid_url,name))
        if port_no and bidder_id and bid_url:
            # Need to impleament lock
            r_bidder = RegisterBidder()
            r_status=r_bidder.addBidder(port_no,bidder_id,bid_url,name)
            if r_status:
                self.build_response({"msg":"Success"},201)
            else:
                self.build_response({"msg":"Fail to register"},408)
        else:
            self.build_response({"msg":"Bad request please ",
                                 "reason":"port_no/bidder_id/bid_url are mandatory field"},
                                 400)

class StartBids(BaseHandler):
    @gen.coroutine
    def post(self):
        acutioneer_list = AUCTIONEERLIST
        bidder_list = BIDDERLIST
        is_present = False
        request_body = json.loads(self.request.body)
        # validate the response
        auctioneer_id = request_body.get('id',None)
        if auctioneer_id==None:
            return self.build_response({"error_msg":"auction_id is required"},400)    # Bad request
        if len(bidder_list)<1:
            return self.build_response({"msg":"Bidder is not available"},503)
        for a in acutioneer_list:
            for _,id in a.items():
                if auctioneer_id == id:
                    is_present = True

        if is_present:
            get_bid = GetbidValue()
            response = yield get_bid.bid() 
            return self.build_response(response,200)
        else:
            return self.build_response({"error_msg":"acutioner id not found"},404)
