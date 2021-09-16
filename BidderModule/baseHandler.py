from tornado import web
import uuid
REGISTRATIONURL = 'http://0.0.0.0:8888/bidderRegistration'
HEADERS = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
MAXPRICE = 999999999
ID = str(uuid.uuid4())

class BaseHandler(web.RequestHandler):
    def build_response(self,body,statusCode=None):
        if isinstance(body,Exception):
            self.set_status(statusCode)
            self.write(body)
        else:
            self.set_status(statusCode)
            self.write(body)
        self.finish()
