'''Agents of the Tragedy of Commons

'''
from fjarrsyn.core.agent import Agent
from fjarrsyn.core.instructor import Interpreter, Moulder
from fjarrsyn.core.message import Belief, Direction, Resource, Essence
from fjarrsyn.core.policy import Clause, Heartbeat, AutoBeliefCondition, \
                        AutoResourceCondition

class Village(Agent):
    '''The Village agent

    '''
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

    def __init__(self, name, n_people, n_fishes, n_potato, how_low, max_fish):

        super().__init__(name)

        #
        # Resources
        #
        village_resource = Resource('village items', 
                                    ['n_fishes', 'n_potato', 'n_people'])
        village_resource.set_values([n_fishes, n_potato, n_people])
        self.set_scaffold(village_resource)

        village_food = MessageOperator(village_resource, 
                           slice_labels=['n_fishes', 'n_potato'])

        #
        # Essence
        #
        disposition = Essence('disposition', ['how_low', 'max_extraction'])
        disposition.set_values([how_low, max_fish])
        self.set_scaffold(disposition)

        #
        # Belief
        #
        fish_status = Belief('must fish', ['assessment'])
        potato_status = Belief('must grow', ['assessment'])
        trust_in_neigh = Belief('trust of neighbours', ['degree'])
        self.set_messages(fish_status, potato_status, trust_in_neigh)

        food_belief = MessageOperator([fish_status, potato_status], extend=True)

        #
        # Flash messages
        #
        direct_fishing_act = Direction('go fish like this', 
                                       ['number_boats', 'upper_limit'])
        direct_grow_act = Direction('go grow field like this',
                                    ['number_farmers'])
        self.set_messages(direct_fishing_act, direct_grow_act)

        direct_food_acquisition = MessageOperator([direct_fishing_act,
                                                   direct_grow_act],
                                                  extend=True)

        #
        # Organs
        #
        stock_ok = Interpreter('storage conditions', self.check_storage, 
                               None, food_belief,
                               resource_op_input=village_food,
                               essence_op_input=XXX)
        get_food = Moulder('how to acquire food', self.food_instructions, 
                           food_belief, direct_food_acquisition)
        self.set_organs(stock_ok, get_food)

        #
        # Survival condition
        #
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
