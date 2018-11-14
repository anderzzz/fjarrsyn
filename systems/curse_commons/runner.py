from core.simulator import FiniteSystemRunner

from propagator import Propagator
from ams import World, Lake
from society import Village

N_VILLAGES = 1

INIT_PEOPLE = 10
INIT_FISHES = 0
INIT_HOW_LOW = 2.0
INIT_MAX_EXTRACTION = 9999999999999
INIT_FISHES_LAKE = 500
LAKE_SIZE = 25
CAPACITY = 1000
SPAWN_PROB = 0.3

collection = []
for k_village in range(N_VILLAGES):
    village = Village('Village %s' %(str(k_village)),
                      INIT_PEOPLE, INIT_FISHES, INIT_HOW_LOW,
                      INIT_MAX_EXTRACTION)
    collection.append(village)

lake = Lake(INIT_FISHES_LAKE, LAKE_SIZE, SPAWN_PROB, CAPACITY)
world = World('Around the Lake', collection, lake)

propagator = Propagator()
runner = FiniteSystemRunner(n_iter=10, n_sample_steps=5,
                            system_propagator=propagator)

runner(world)

