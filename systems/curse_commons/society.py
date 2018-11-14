'''Basic Curse of the Commons

'''
from core.agent import Agent
from core.instructor import Interpreter, Moulder
from core.message import Belief, Direction, Resource, Essence
from core.policy import Clause, Heartbeat, AutoBeliefCondition, \
                        AutoResourceCondition

class Village(Agent):

    def inspect_storage(self, n_fishes, n_people):

        storage_ratio = float(n_fishes) / float(n_people)

        if storage_ratio < self.essence['how_low'] * 0.3:
            ret = 'very low'

        elif storage_ratio < self.essence['how_low'] * 0.6:
            ret = 'quite low'

        elif storage_ratio < self.essence['how_low']:
            ret = 'low'

        else:
            ret = 'OK'

        return ret

    def fish_instr(self, assessment):

        upper_limit = self.essence['max_extraction']
        if assessment == 'very low':
            send_n_boats = 1 + int(self.resource['n_people'] * 0.55)

        elif assessment == 'quite low':
            send_n_boats = 1 + int(self.resource['n_people'] * 0.30)

        elif assessment == 'low':
            send_n_boats = 1 + int(self.resource['n_people'] * 0.10)

        else:
            send_n_boats = 0 

        return send_n_boats, upper_limit

    def __call__(self):
        
        if self.pump():
            if self.clause['fish now?'].apply_to(self):
                self.clause['go'].apply_to(self)

        else:
            self.heartbeat.inert = True

    def __init__(self, name, n_people, n_fishes, how_low, max_fish):

        super().__init__(name)

        disposition = Essence('disposition', ['how_low', 'max_extraction'])
        disposition.set_values([how_low, max_fish])
        self.set_scaffold(disposition)

        village_resource = Resource('village items', 
                                    ['n_fishes', 'n_people'])
        village_resource.set_values([n_fishes, n_people])
        self.set_scaffold(village_resource)

        storage_status = Belief('must add to stock', ['assessment'])
        stock_ok = Interpreter('should we go fish', self.inspect_storage, 
                                village_resource, storage_status)
        direct_fishing_act = Direction('go fish like this', 
                                       ['number_boats', 'upper_limit'])
        go_fishing = Moulder('go fish', self.fish_instr, storage_status,
                             direct_fishing_act)
        self.set_organs(stock_ok, go_fishing)

        belief_cond = AutoBeliefCondition('warehouse status', 
                                          lambda x: x != 'OK',
                                          'must add to stock')
        clause_1 = Clause('fish now?', ('should we go fish',), belief_cond)
        clause_2 = Clause('go', ('go fish', 'fish from lake'))
        self.set_policies(clause_1, clause_2)

        heart_cond = AutoResourceCondition('still alive', 
                                           lambda x: x > 0,
                                           ('n_people',))
        heart = Heartbeat('alive', (heart_cond,))
        self.set_policies(heart)

class Institution(Agent):
    '''Bla bla

    '''
    def __init__(self, name):

        super().__init__(name)
