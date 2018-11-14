'''Basic Curse of the Commons

'''
import numpy as np
import numpy.random

from core.agent_ms import AgentManagementSystem
from core.instructor import Actuator, Compulsion
from core.scaffold_map import ResourceMap, MapCollection

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

        map_fish = ResourceMap('fish stock change', 'delta', 'n_fishes', ('adjust_fish',))
        map_people = ResourceMap('birth death', 'delta', 'n_people', ('adjust_people',))
        eat_love_death = MapCollection([map_fish, map_people])

        natural_reqs = Compulsion('survival demands', self.eat_life_die,
                                  eat_love_death)
        self.set_law(natural_reqs)

        for agent in agents:
            more_fish = ResourceMap('add_fish', 'delta', 'n_fishes', ('add_fishes',))
            fish_from_lake = Actuator('fish from lake', 
                                      self.extract_from_lake,
                                      agent.direction['go fish like this'],
                                      more_fish)
            agent.set_organ(fish_from_lake)

