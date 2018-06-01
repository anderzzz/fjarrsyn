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

    def product_value_set(self, product_name, value):
        '''Bla bla

        '''
        self.buyer.internal_state[product_name] = value

    def product_value(self, pv_map, pv_map_randomize=None):
        '''Bla bla

        '''
        for product, value in pv_map.items():
            # ADD RANDOMIZATION
            self.product_value_set(product, value)

    def __init__(self, name):

        self.buyer = Agent(name)
        self.buyer.set_request_services('make_bid', self._request_make_a_bid)
            

class SellerAgent(object):
    '''Bla bla

    '''
    def _request_accept_an_offer(self):
        '''Bla bla

        '''
        return True

    def product_value_set(self, product_name, value):
        '''Bla bla

        '''
        self.seller.internal_state[product_name] = value

    def product_value(self, pv_map, pv_map_randomize=None):
        '''Bla bla

        '''
        for product, value in pv_map.items():
            # ADD RANDOMIZATION
            self.product_value_set(product, value)

    def __init__(self, name):
    
        seller = Agent(name)
        seller.set_request_services('accept_offer', self._request_accept_an_offer)

class Auction(object):
    '''Bla bla

    '''
    def _execute_vickrey(self):
        '''Bla bla

        '''
        pass

    def __call__(self):
        '''Bla bla

        '''
        if self.auction_type == 'vickrey':
            self._execute_vickrey()
        else:
            raise RuntimeError('Unknown auction type: %s' %(self.auction_type))

    def __init__(self, buyers, sellers, auction_type='vickrey', n_rounds=1):

        self.auction_type = auction_type

