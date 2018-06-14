'''Bla bla

'''
from core.agent import Agent

class BuyerAgent(Agent):
    '''Bla bla

    '''
    def _request_make_honest_bid(self, item):
        '''Bla bla

        '''
        return self.internal_state[item]

    def __init__(self, name):

        super().__init__(name)

        self.set_request_services('make_honest_bid', self._request_make_honest_bid)
            

class SellerAgent(Agent):
    '''Bla bla

    '''
    def _request_accept_an_offer(self):
        '''Bla bla

        '''
        return True

    def _request_what_on_sale(self):
        '''Bla bla

        '''
        return set(self.internal_state.__iter__())

    def __init__(self, name):
    
        super().__init__(name)

        self.set_request_services('accept_offer', self._request_accept_an_offer)
        self.set_request_services('what_on_sale', self._request_what_on_sale)

class Auction(object):
    '''Bla bla

    '''
    def _retrieve_items_on_sale(self):
        '''Bla bla

        '''
        items_to_sell = set([])
        for agent in self.agents_of_auction:
            (sales_items, yesno) = agent.request('what_on_sale')
            if yesno:
                items_to_sell |= sales_items

        return items_to_sell

    def _execute_vickrey(self):
        '''Bla bla

        '''
        items_to_sell = self._retrieve_items_on_sale()

        # CONTINUE BUILD LOGIC
        for item in items_to_sell:
            for agent in self.agents_of_auction:
                (honest_bid, yesno) = agent.request('make_honest_bid', {'item':item})
                print (item, agent.name, honest_bid)

        raise RuntimeError('FOOBAR')

    def __call__(self):
        '''Bla bla

        '''
        for k_round in range(0, self.n_rounds):
            self.run_auction()
            #for agent in agents:
            #    agent.refresh()

    def __init__(self, agents, auction_type='vickrey', n_rounds=1):

        self.auction_type = auction_type
        self.n_rounds = n_rounds
        self.agents_of_auction = agents

        
        if self.auction_type == 'vickrey':
            self.run_auction = self._execute_vickrey
        else:
            raise RuntimeError('Unknown auction type: %s' %(self.auction_type))

