'''Bla bla

'''
from core.agent import Agent

class BuyerAgent(object):
    '''Bla bla

    '''
    def _request_make_a_bid(self):
        '''Bla bla

        '''
        return True

    def __init__(self, name):

        buyer = Agent(name)
        buyer.set_request_services('make_bid', self._request_make_a_bid)
            

class SellerAgent(object):
    '''Bla bla

    '''
    def _request_accept_an_offer(self):
        '''Bla bla

        '''
        return True

    def __init__(self, name):
    
        seller = Agent(name)
        seller.set_request_services('accept_offer', self._request_accept_an_offer)
