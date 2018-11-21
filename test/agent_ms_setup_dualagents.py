'''Integration test of AMS where the AMS compels agents, but where the agents
are of different types and have different laws 

'''
from core.agent import Agent
from core.agent_ms import AgentManagementSystem
from core.message import Resource
from core.scaffold_map import ResourceMap, MapCollection
from core.instructor import Compulsion

REF1 = [30.8, 10.56, 7.04, 5.28]
REF2 = [0.0, 0.0, 0.0, 0.0, 92.0]

def interest_rate():
    return 1.0 - 0.08

def farm_name_test(name):
    return 'farmer' in name

resource = Resource('harvest', ('wheat', 'rye', 'barley', 'oats'))
resource.set_values([35.0, 12.0, 8.0, 6.0])
agent1 = Agent('farmer Joe', True)
agent1.set_scaffold(resource)

resource = Resource('food producer', ('wheat', 'rye', 'barley', 'oats', 
                                      'cash_on_hand'))
resource.set_values([0.0, 0.0, 0.0, 0.0, 100.0])
agent2 = Agent('yummy Inc', True)
agent2.set_scaffold(resource)

ams = AgentManagementSystem('food market', [agent1, agent2])
uuid_of_yummy = list(ams.agents_in_scope.values())[1].agent_id_system

mapper = ResourceMap('cash loss', 'scale', 'cash_on_hand', ('factor',))
amort = Compulsion('amortization', interest_rate, mapper)
ams.set_law(amort)

mapper_wheat = ResourceMap('loss of wheat', 'scale', 'wheat', ('factor',))
mapper_rye = ResourceMap('loss of rye', 'scale', 'rye', ('factor',))
mapper_barley = ResourceMap('loss of barley', 'scale', 'barley', ('factor',))
mapper_oats = ResourceMap('loss of oats', 'scale', 'oats', ('factor',))
mapper_cereal = MapCollection([mapper_wheat, mapper_rye, mapper_barley, mapper_oats])
sloppy = Compulsion('sloppy', lambda : 4*[0.88], mapper_cereal)
ams.set_law(sloppy)

ams.make_lawbook_entry(['sloppy'], agent_name_selector=farm_name_test)
ams.make_lawbook_entry(['amortization'], agent_ids=[uuid_of_yummy])

for agent in ams.cycle_nodes(True, 2):
    ams.engage_all_verbs(agent, validate_lawbook=True)

vals1 = agent1.resource.values()
vals2 = agent2.resource.values()

assert (vals1 == REF1)
assert (vals2 == REF2)

ams.compel(agent2, 'sloppy')

try:
    ams.compel(agent2, 'sloppy', validate_lawbook=True)
except RuntimeError as e:
    if 'Compulsion sloppy is not in law book' in str(e):
        pass
    else:
        raise AssertionError('Exception was not properly raised')

try:
    ams.compel(agent1, 'amortization')
except KeyError as e:
    if 'cash_on_hand' in str(e):
        pass
    else:
        raise AssertionError('Exception was not properly raised')
