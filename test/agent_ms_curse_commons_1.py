'''Basic Curse of the Commons

'''
import numpy as np
import numpy.random

from core.agent import Agent
from core.agent_ms import AgentManagementSystem
from core.organs import Sensor, Interpreter, Moulder, Actuator
from core.array import Belief, Direction, Resource, Essence
from core.naturallaw import ResourceMap
from core.propagate import Clause, AutoBeliefCondition

class Lake(object):

    def regrowth(self):

        growth_rate = np.random.ranf() * self.max_growth_rate / 100.0
        self.n_fish += self.n_fish * (self.capacity - self.n_fish) * growth_rate

    def extract(self, maximum):

        n_extraction = min(int(np.random.ranf() * self.n_fish / self.size_units), maximum)
        self.n_fish -= n_extraction

        return n_extraction

    def __init__(self, n_fish, max_growth_rate, size):

        self.n_fish = n_fish
        self.max_growth_rate = max_growth_rate
        self.size_units = size

class Village(Agent):

    def inspect_storage(self, dummy):

        n_fishes, n_people = self.village_resource.values()
        n_people = self.n_people.values()
        storage_ratio = float(n_fishes) / float(n_people)

        if storage_ratio < self.essence['how_low'] * 0.5:
            ret = 'very low'

        elif storage_ration < self.essence['how_low'] * 0.75:
            ret = 'quite low'

        elif storage_ration < self.essence['how_low']:
            ret = 'low'

        else:
            ret = 'OK'

        return ret

    def fish_instr(self, assessment):

        upper_limit = self.essence['max_extraction']
        if assessment == 'very low':
            send_n_boats = 12

        elif assessment == 'quite low':
            send_n_boats = 6

        elif assessment == 'low':
            send_n_boats = 3

        else:
            send_n_boats = 0 

        return send_n_boats, upper_limit

    def __call__(self):

        if self.heartbeat():
            if self.clause['fish now?']:
                self.clause['go']

    def __init__(self, name, n_people, n_fishes, how_low, max_fish):

        super().__init__(name)

        disposition = Essence('disposition', ['how_low', 'max_extraction'])
        disposition.set_values([how_low, max_fish])
        self.set_scaffold(disposition)

        village_resources = Resource('village items', 
                                     ['n_fishes', 'n_people'])
        village_resource.set_values([n_fishes, n_people])
        self.set_scaffold(village_resources)

        storage_status = Belief('must add to stock', 'assessment')
        stock_ok = Interpreter('should we go fish', storage_status,
                               self.inspect_storage, storage_status)
        direct_fishing_act = Direction('go fish like this', 
                                       ['number_boats', 'upper_limit'])
        go_fishing = Moulder('go fish', storage_status, self.fish_instr,
                             direct_fishing_act)

        belief_cond = AutoBeliefCondition('warehouse status', 
                                          storage_status,
                                          lambda x: x != 'OK')
        clause_1 = Clause('fish now?', ('should we go fish',), belief_cond)
        clause_2 = Clause('go', ('go fish', 'fish from lake'))
        self.set_policies(clause_1, clause_2)

class World(AgentManagementSystem):

    def extract_from_lake(self, n_boats, max_extract, agent_index):

        if n_boats == 0:
            return 0

        n_total = 0
        effort_count = 0
        while n_total < max_extract:
            
            n_fishes = self.common_env.extract(max_extract)
            n_total += n_fishes
            effort_count += 1

            if effort_count > n_boats:
                break

        return n_total

    def __init__(self, name, agents, lake):

        super().__init__(name, agents)

        for agent in agents:
            more_fish = ResourceMap('add_fish', 'village_items', 'delta', ('n_fishes',))
            fish_from_lake = Actuator('fish from lake', 
                                      agent.direction['go fish like this'],
                                      self.extract_from_lake,
                                      'fish_results',
                                      more_fish)
            agent.add_organ(fish_from_lake)

        self.common_env = lake


village_1 = Village('Lakeside', 20, 20, 1.0, 10)
village_2 = Village('Bayside', 20, 20, 1.0, 10)

the_world = World('World around the lake', [village_1, village_2])
