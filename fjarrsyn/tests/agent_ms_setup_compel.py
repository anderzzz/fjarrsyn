'''Integration test of AMS where the AMS compels one agent's resources a
certain way

'''
from fjarrsyn.core.agent import Agent
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.message import Resource
from fjarrsyn.core.scaffold_map import ResourceMap
from fjarrsyn.core.instructor import Compulsion

REF = [(10.0, 4.0), (4.0, 2.0), (2.0, 1.0), (1.0, 0.5), (0.5, 0.25)]

def simple_decline(poison_amount_getter, doodle):
    poison_amount = poison_amount_getter()
    return 1.0 / max(0.25 * poison_amount, doodle)

resource = Resource('poison in body', ['amount', 'kind'])
resource.set_values([10.0, 'mercury'])

agent = Agent('thin agent', strict_engine=True)
agent.set_scaffold(resource)

ams = AgentManagementSystem('exterior laws', [agent])

mapper = ResourceMap('scale down', 'scale', 'amount', ('factor',))
kwargs = {'poison_amount_getter' : lambda : agent.resource['amount'], 
          'doodle' : 2.0}
compulsion = Compulsion('natural decay', simple_decline, mapper,
                        compel_func_kwargs=kwargs)
ams.set_law(compulsion)

count = 0
for agent in ams.shuffle_nodes(True, 5, False):
    before = agent.resource['amount']
    ams.compel(agent, 'natural decay')
    after = agent.resource['amount']
    assert (before == REF[count][0])
    assert (after == REF[count][1])
    count += 1
