from core.agent import Agent
from core.agent_ms import AgentManagementSystem
from core.graph import Node
import numpy

a1 = Agent('a1')
a2 = Agent('a2')
a3 = Agent('a3')
a4 = Agent('a4')

ams = AgentManagementSystem('dummy', [a1, a2, a3, a4])

stuff = []
for nn in ams.cycle_nodes(True, 12):
    assert (isinstance(nn, Agent))
    stuff.append(nn.name)

assert (len(stuff) == 12)

for k in range(3):
    assert (set(stuff[4 * k : 4 * (k + 1)]) == set(['a1', 'a2', 'a3', 'a4']))

count = 0
for nn in ams.shuffle_edges(False, 20, False):
    assert (len(nn) == 2)
    assert (isinstance(nn[0], Node))
    assert (isinstance(nn[1], Node))
    count += 1

stuff = []
for nn in ams.shuffle_nodes(True, 20, True):
    stuff.append(nn.name)

assert (len(stuff) == 20)
#
# Small chance this test fails randomly. This checks that sampling is mostly
# uneven, but randomly it can become even.
#
assert (not numpy.std([stuff.count('a1'), stuff.count('a2'), 
                       stuff.count('a3'), stuff.count('a4')])<0.01)

assert (isinstance(ams.choice_nodes(False), Node))
assert (isinstance(ams.choice_nodes(True), Agent))

assert (isinstance(ams.choice_edges(False)[0], Node))
assert (isinstance(ams.choice_edges(True)[0], Agent))
assert (len(ams.choice_edges(False)) == 2)
assert (len(ams.choice_edges(True)) == 2)
