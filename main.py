from tornado import web
from tornado import ioloop
from auctioneer import RootHandler,AuctioneerList, StartBids, AddBidder


# Method verification method
def actionerAndBidderApp():
    return web.Application([
        (r"/startBid",StartBids),
        (r"/auctioneerList",AuctioneerList),
        (r"/bidderRegistration",AddBidder)
    ])

if __name__ == "__main__":
    # Adding the acutioneer
    RootHandler.addAuctioneer(2)
    app = actionerAndBidderApp()
    app.listen(8888)
    print("Auctioneer is listing on port 8888.....",end='\n')
    ioloop.IOLoop.current().start()

