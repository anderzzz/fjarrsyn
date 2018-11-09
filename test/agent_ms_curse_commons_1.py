'''Basic Curse of the Commons

'''
import numpy as np
import numpy.random

from core.agent import Agent
from core.agent_ms import AgentManagementSystem
from core.organ import Sensor, Interpreter, Moulder, Actuator
from core.array import Belief, Direction, Resource, Essence
from core.naturallaw import Compulsion, ResourceMap, ResourceMapCollection
from core.policy import Clause, Heartbeat, AutoBeliefCondition, \
                        AutoResourceCondition

class Lake(object):

    def regrowth(self):

        n_spawn = 0
        for fish in range(0, self.n_fish):
            n_attempt = int(np.random.ranf() + self.spawn_prob)
            n_crowding = int(np.random.ranf() + self.n_fish / self.capacity)
            if n_attempt == 1 and n_crowding == 0:
                n_spawn += 1

        self.n_fish = min(self.capacity, self.n_fish + n_spawn)

    def extract(self, maximum, extract_prob):

        which_unit_is_fish = np.random.randint(0, self.size_units, self.n_fish)
        select_unit = np.random.randint(0, self.size_units)
        max_available = sum([1 for x in which_unit_is_fish if x == select_unit])
        extract_attempt = [np.random.ranf() < extract_prob for k in range(max_available)]
        n_extracted = min(maximum, sum(extract_attempt))

        self.n_fish -= n_extracted
        
        return n_extracted

    def __init__(self, n_fish, size, spawn_prob, max_capacity):

        self.n_fish = n_fish
        self.spawn_prob = spawn_prob
        self.size_units = size
        self.capacity = max_capacity

class Village(Agent):

    def inspect_storage(self, dummy):

        n_fishes, n_people = self.resource.values()
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
            raise RuntimeError('Death of Village')

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
        stock_ok = Interpreter('should we go fish', storage_status,
                               self.inspect_storage, storage_status)
        direct_fishing_act = Direction('go fish like this', 
                                       ['number_boats', 'upper_limit'])
        go_fishing = Moulder('go fish', storage_status, self.fish_instr,
                             direct_fishing_act)
        self.set_organs(stock_ok, go_fishing)

        belief_cond = AutoBeliefCondition('warehouse status', 
                                          None,
                                          lambda x: x != 'OK')
        clause_1 = Clause('fish now?', ('should we go fish',), belief_cond)
        clause_2 = Clause('go', ('go fish', 'fish from lake'))
        self.set_policies(clause_1, clause_2)

        heart_cond = AutoResourceCondition('still alive', 
                                           'village items',
                                           ('n_people',),
                                           lambda x: x > 0)
        heart = Heartbeat('alive', (heart_cond,))
        self.set_policies(heart)

BIRTH_PROB = 0.10
BIRTH_PROB_CAUTION = BIRTH_PROB * 0.5
STARVE_PROB = 0.25

class World(AgentManagementSystem):

    def eat_life_die(self, people_current, fish_current):

        if fish_current <= people_current:
            n_starving = people_current - fish_current

            starve_test = [np.random.ranf() < STARVE_PROB for x in range(n_starving)]
            breed_test = [np.random.ranf() < BIRTH_PROB_CAUTION for x in range(fish_current)]

            delta_people = -1 * sum(starve_test) + sum(breed_test)
            delta_fish = -1 * fish_current

        elif fish_current >= people_current * 2:
            breed_test = [np.random.ranf() < BIRTH_PROB for x in range(people_current)]
            delta_people = sum(breed_test)
            delta_fish = -2 * people_current

        else:
            n_full = fish_current - people_current
            breed_test_1 = [np.random.ranf() < BIRTH_PROB for x in range(n_full)]
            breed_test_2 = [np.random.ranf() < BIRTH_PROB_CAUTION for x in range(people_current - n_full)]
            delta_people = sum(breed_test_1) + sum(breed_test_2)
            delta_fish = -1 * fish_current

        print (fish_current, delta_fish, people_current, delta_people)

        return delta_fish, delta_people

    def extract_from_lake(self, n_boats, max_extract, agent_index):

        if n_boats == 0:
            return 0

        n_total = 0
        effort_count = 0
        while n_total < max_extract:
            
            n_fishes = self.common_env.extract(max_extract, 0.5)
            n_total += n_fishes
            effort_count += 1

            if effort_count > n_boats:
                break

        print (n_total)
        return n_total

    def __init__(self, name, agents, lake):

        super().__init__(name, agents)
        self.common_env = lake

        map_fish = ResourceMap('fish stock change', 'n_fishes', 'delta', ('adjust_fish',))
        map_people = ResourceMap('birth death', 'n_people', 'delta', ('adjust_people',))
        eat_love_death = ResourceMapCollection([map_fish, map_people])

        natural_reqs = Compulsion('survival demands', ['n_people', 'n_fishes'], 
                                  self.eat_life_die, eat_love_death)
        self.set_law(natural_reqs)

        for agent in agents:
            more_fish = ResourceMap('add_fish', 'n_fishes', 'delta', ('add_fishes',))
            fish_from_lake = Actuator('fish from lake', 
                                      agent.direction['go fish like this'],
                                      self.extract_from_lake,
                                      'fish_results',
                                      more_fish)
            agent.set_organ(fish_from_lake)



village_1 = Village('Lakeside', 20, 50, 3.0, 4000)
village_2 = Village('Bayside', 20, 50, 3.0, 4000)
lake = Lake(200, 20, 0.1, 1000)
the_world = World('World around the lake', [village_1], lake)

for k in range(0, 1000):
    for agent, aux_content in the_world:

        agent()
        the_world.compel(agent, 'survival demands')
        the_world.common_env.regrowth()

        print (agent.name)
        print (agent.resource)
    print ('FISH IN LAKE:',lake.n_fish)
