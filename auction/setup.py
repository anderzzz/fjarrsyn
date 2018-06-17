'''Bla bla

'''
from core.agent import Agent
from core.agent_ms import AgentManagementSystem

class AuctionParticipant(Agent):
    '''Bla bla

    '''
    def _request_what_selling(self):
        '''Bla bla

        '''
        return self.database.keys()

    def _request_make_honest_bid(self, item_name):
        '''Bla bla

        '''
        belief_label = 'buy_' + item_name
        if belief_label in self.belief:
            bid = self.belief[belief_label]
        else:
            bid = None

        return bid

    def _request_accept_to_sell(self, item_name, price_offer):
        '''Bla bla

        '''
        belief_label = 'sell_' + item_name
        if belief_label in self.belief:
            valuation = self.belief[belief_label]
            threshold_accept = valuation <= price_offer
        else:
            threshold_accept = None

        return threshold_accept

    def __init__(self, name, items_on_hand={}, true_valuation={}):

        super().__init__(name)

        for thing, number_in_stock in items_on_hand.items():
            self.update_database(thing, new_value=number_in_stock)

        for thing, valuation in true_valuation.items():
            self.update_belief(thing, new_belief=valuation)

        self.set_service('what_is_sold', self._request_what_selling)
        self.set_service('make_honest_bid', self._request_make_honest_bid)
        self.set_service('accept_to_sell', self._request_accept_to_sell)

class Auction(AgentManagementSystem):
    '''Bla bla

    '''
    def _retrieve_items_on_sale(self):
        '''Bla bla

        '''
        items_to_sell = set([])
        for agent in self.agents_iter():
            (sales_items, yesno) = agent.request_service('what_is_sold')
            if yesno:
                items_to_sell |= sales_items

        return items_to_sell

    def _execute_vickrey(self):
        '''Bla bla

        '''
        items_to_sell = self._retrieve_items_on_sale()

        # CONTINUE BUILD LOGIC
        for item in items_to_sell:
            for agent in self.agents_iter():
                (honest_bid, yesno) = agent.request_service('make_honest_bid', {'item_name':item})
                print (item, agent.name, honest_bid)

        raise RuntimeError('FOOBAR')

    def __call__(self):
        '''Bla bla

        '''
        for k_round in range(0, self.n_rounds):
            self.run_auction()
            #for agent in agents:
            #    agent.refresh()

    def __init__(self, name, agents, auction_type='vickrey', n_rounds=1):

        super().__init__(name, agents)

        self.auction_type = auction_type
        self.n_rounds = n_rounds
        
        if self.auction_type == 'vickrey':
            self.run_auction = self._execute_vickrey
        else:
            raise RuntimeError('Unknown auction type: %s' %(self.auction_type))

