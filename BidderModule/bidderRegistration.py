import uuid
import json
from tornado import gen
from tornado.httpclient import AsyncHTTPClient,HTTPRequest
from baseHandler import REGISTRATIONURL, HEADERS, ID

'''
{
    "id": "1",
    "port": "123",
    "bid_url": "/getValue",
    "name": ""
}'''

class BidderRegistration:
    def _create_request(self, *args, **kwargs):
        return HTTPRequest(*args, **kwargs)

    @gen.coroutine
    def bidderRegistration(self):
        http_client = AsyncHTTPClient()
        body = {"id":ID ,
                "port": 8001,
                "url": "/getValue",
                "name": ""
                }
        
        request = self._create_request(url= REGISTRATIONURL,
                                       method='PUT',
                                       headers=HEADERS,
                                       body=json.dumps(body)
                                       )
        try:
            response = yield http_client.fetch(request)
        except Exception as e:
            print("Error: %s" % e)
            return
        print(json.loads(response.body))
        return