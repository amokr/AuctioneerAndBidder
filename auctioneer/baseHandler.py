from tornado import web,gen
import json
from tornado.httpclient import AsyncHTTPClient,HTTPRequest
AUCTIONEERLIST = []
BIDDERLIST = []
ENDPOINT = "http://0.0.0.0:"
HEADERS = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
MINBIDPRICE = 0

class BaseHandler(web.RequestHandler):
    # Need to add status code for different type of response
    def build_response(self,body,statusCode=None):
        if isinstance(body,Exception):
            self.set_status(statusCode)
            self.write(body)
        else:
            self.set_status(statusCode)
            self.write(body)
        self.finish()

class RegisterBidder:
    def addBidder(self,port,id,url,name=''):
        global BIDDERLIST
        bidder = {
            'id':id,
            'port':port,
            'bid_url':url,
            'name':name
        }
        BIDDERLIST.append(bidder)
        return True


# {"bidder_id": ID,"bid_value":price}
class GetbidValue:
    def _create_request(self, *args, **kwargs):
        return HTTPRequest(*args, **kwargs)

    @gen.coroutine
    def getBidValue(self, urls):
        requests = []
        biddes_values = []
        for url in urls:
            requests.append(self._create_request(url= url,method='GET'))
        http_client = AsyncHTTPClient()
        waiter = gen.WaitIterator(*[http_client.fetch(request) for request in requests])
        while not waiter.done():
            try:
                response = yield waiter.next()
            except Exception as e:
                print("Error {0} from {1} while making \
                      the bidder call".format(e, waiter.current_future))
            else:
                r_body = json.loads(response.body)
                biddes_values.append(r_body)
                print("Result {0} received from {1} \
                      at {2}".format(json.loads(response.body),waiter.current_future,
                                     waiter.current_index))
        return biddes_values

    @gen.coroutine
    def bid(self):
        bidder_urls = []
        print("Added bidder list : {}".format(BIDDERLIST))
        for bidder in BIDDERLIST:
            bidder_urls.append(bidder['bid_url'])
        values = yield self.getBidValue(bidder_urls)
        result = {
            'bidder_id':'',
            'bid_value':MINBIDPRICE
        }
        for value in values:
            b_v = value['bid_value']
            if result['bid_value'] < b_v:
                result['bid_value'] = b_v
                result['bidder_id'] = value['bidder_id']
        return result