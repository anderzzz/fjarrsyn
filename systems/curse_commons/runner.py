from core.simulator import FiniteSystemRunner
from core.sampler import AgentSampler, EnvSampler, SystemIO

from propagator import Propagator
from ams import World, Lake
from society import Village

N_VILLAGES = 2

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

village_sampler = AgentSampler(resource_args=[('village items', 'n_people')],
                               essence_args=[('disposition', 'max_extraction'),
                                             ('disposition', 'how_low')],
                               sample_steps=5,
                               matcher=lambda x : 'Village' in x.name)

lake = Lake(INIT_FISHES_LAKE, LAKE_SIZE, SPAWN_PROB, CAPACITY)
#lake_sampler = EnvSampler()

world = World('Around the Lake', collection, lake)

io = SystemIO([('villages', 'to_json', village_sampler)])
#io.append('villages', 'csv', village_sampler)
#io.append('lake', 'csv', lake_sampler)
propagator = Propagator()
runner = FiniteSystemRunner(10, propagator,
                            system_io=io)

runner(world)

