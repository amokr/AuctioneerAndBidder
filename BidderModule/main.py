from tornado import gen, web
from tornado import ioloop
from bidderRegistration import BidderRegistration
from bidder import DoBidding

# Method verification method
def actionerAndBidderApp():
    return web.Application([
        (r"/getValue",DoBidding)
    ])
@gen.coroutine
def createBidder():
    bidder = BidderRegistration()
    try:
        yield bidder.bidderRegistration()
    except Exception as e:
        print("Error")


if __name__ == "__main__":
    port = [8001]
    createBidder()
    app = actionerAndBidderApp()
    app.listen(8001)
    print("Bidder is running on port 8001.....",end='\n')
    ioloop.IOLoop.current().start()
