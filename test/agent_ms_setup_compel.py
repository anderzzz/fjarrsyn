'''Integration test of AMS where the AMS compels one agent's resources a
certain way

'''
from core.agent import Agent
from core.agent_ms import AgentManagementSystem
from core.message import Resource
from core.scaffold_map import ResourceMap
from core.instructor import Compulsion

REF = [(10.0, 4.0), (4.0, 2.0), (2.0, 1.0), (1.0, 0.5), (0.5, 0.25)]

def simple_decline(poison_amount, doodle):
    return 1.0 / max(0.25 * poison_amount, doodle)

resource = Resource('poison in body', ['amount', 'kind'])
resource.set_values([10.0, 'mercury'])

agent = Agent('thin agent')
agent.set_scaffold(resource)

ams = AgentManagementSystem('exterior laws', [agent])

mapper = ResourceMap('scale down', 'scale', 'amount', ('factor',))
compulsion = Compulsion('natural decay', simple_decline, mapper,
                        {'doodle' : 2.0})
ams.set_law(compulsion)

count = 0
for agent, aux in ams.shuffle_iter(5):
    before = agent.resource['amount']
    ams.compel(agent, 'natural decay')
    after = agent.resource['amount']
    assert (before == REF[count][0])
    assert (after == REF[count][1])
    count += 1
