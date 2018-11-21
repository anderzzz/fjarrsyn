'''Integration test of various agent and system sampling scenarios

'''
from core.agent import Agent
from core.agent_ms import AgentManagementSystem
from core.message import Belief, Essence, Resource, Buzz
from core.instructor import Interpreter, Sensor
from core.graph import Node
from core.sampler import AgentSampler, EnvSampler, GraphSampler, SystemIO

import networkx as nx
import numpy as np
import numpy.random
np.random.seed(79)
import os

class House(AgentManagementSystem):

    def feel_spectrum(self, agent_index):
        node = self.node_from_agent_id_[agent_index]
        sample = node.aux_content.sample_me()

        return sample

    def __init__(self, name, agents, graph):

        super().__init__(name, agents, full_agents_graph=graph)

        for node in self:
            agent = node.agent_content
            if agent is None:
                continue
            if agent.name == 'Coordinator':
                continue

            motion_sense = Sensor('Feel microwaves', self.feel_spectrum,
                                  agent.buzz['Power Spectrum Sample'],
                                  agent_id_to_engine=True)
            agent.set_organ(motion_sense)

class LocalEnv(object):

    def sample_me(self):

        return np.random.ranf() * 5.0, np.random.ranf() * 5.0

    def __init__(self, stuff):

        self.microwave_power_spectrum = None
        self.stuff = stuff

def env_stuff(aux):
    stuff = aux.stuff
    return {'env_stuff' : stuff}

def pw2obj(amp_max, f_mode):
    size = 'nothing'
    speed = 'n/a'
    if amp_max > 5.0:
        size = 'large'
        if f_mode > 5.0:
            speed = 'fast'

        elif f_mode > 1.0:
            speed = 'slow'

    elif amp_max > 1.0:
        size = 'small'
        if f_mode > 3.0:
            speed = 'fast'

        elif f_mode > 1.0:
            speed = 'slow'

    return size, speed

def _match(agent, name):
    if agent is None:
        return False
    else:
        if name in agent.name:
            return True
        else:
            return False

def _match_c(agent):
    return _match(agent, 'Coordinator')
def _match_l(agent):
    return _match(agent, 'Leaf')

agent_core = Agent('Coordinator')
essence = Essence('Coordinator Essence', ('param_1', 'param_2', 'param_3',
                                          'param_4', 'param_5', 'param_6'))
essence.set_values([1.0,2.0,3.0,4.0,5.0,6.0])
resource = Resource('Coordinator Resource', ('Energy Status',))
resource.set_values([75.0])
agent_core.set_scaffolds(essence, resource)

agents = [agent_core]
nodes = [Node('Central', agent_core)]

for k in range(4):
    agent = Agent('Sensor Leaf %s' %(str(k)), strict_engine=True)
    essence = Essence('Sensor Essence', ('Sensitivity', 'Quality'))
    essence.set_values([78.0 + float(k), 99.0])
    resource = Resource('Sensor Resource', ('Battery Power',))
    resource.set_values([100.0 - 3.0 * k])
    buzz = Buzz('Power Spectrum Sample', ('amplitude_max', 'freq_mode'))
    belief = Belief('Is There Motion', ('size', 'speed'))
    motion_classifier = Interpreter('From Freq to Object', pw2obj, buzz, belief)
    agent.set_scaffolds(essence, resource)
    agent.set_messages(buzz, belief)
    agent.set_organ(motion_classifier)

    agents.append(agent)
    nodes.append(Node('Sensor', agent, LocalEnv(k * k)))

nodes.append(Node('dummy', None))
nodes.append(Node('dummy', None))

star_graph = nx.generators.classic.star_graph(nodes)

ams = House('A House', agents, star_graph)
for node in ams:
    agent = node.agent_content
    if not agent is None:
        if 'Is There Motion' in agent.belief:
            agent.sense('Feel microwaves')
            agent.interpret('From Freq to Object')

central_a_sampler = AgentSampler(essence_args=[('Coordinator Essence', 'param_2'),
                                               ('Coordinator Essence', 'param_6')],
                                 resource_args=[('Coordinator Resource', 'Energy Status')],
                                 agent_matcher=_match_c)
leaf_a_sampler = AgentSampler(resource_args=[('Sensor Resource', 'Battery Power')],
                              belief_args=[('Is There Motion', 'size'),
                                           ('Is There Motion', 'speed')],
                              agent_matcher=_match_l)
env_sampler = EnvSampler(env_stuff, agent_matcher=_match_l)
graph_sampler = GraphSampler(lambda x: x.name)

io = SystemIO()
io.set_write_rule('central', central_a_sampler, 'to_csv')
io.set_write_rule('leaf', leaf_a_sampler, 'to_csv')
io.set_write_rule('env', env_sampler, 'to_json')
io.set_write_rule('graph_props', graph_sampler, 'gexf.write_gexf')

io.try_stamp(ams, 0)

exist_1 = os.path.isfile('central0.csv')
exist_2 = os.path.isfile('leaf0.csv')
exist_3 = os.path.isfile('env0.json')
exist_4 = os.path.isfile('graph_props0.gexf')
assert (exist_1)
assert (exist_2)
assert (exist_3)
assert (exist_4)

if exist_1:
    data = open('central0.csv').read()
    assert ('essence:Coordinator Essence:param_2,2.0' in data)
    assert ('essence:Coordinator Essence:param_6,6.0' in data)
    assert (not 'essence:Coordinator Essence:param_1' in data)
    assert (not 'essence:Coordinator Essence:param_3' in data)
    assert (not 'essence:Coordinator Essence:param_4' in data)
    assert (not 'essence:Coordinator Essence:param_5' in data)
    assert ('resource:Coordinator Resource:Energy Status,75.0' in data)
    os.remove('central0.csv')

if exist_2:
    data = open('leaf0.csv').read()
    assert ('0,Sensor Leaf 0,' in data)
    assert ('0,Sensor Leaf 1,' in data)
    assert ('0,Sensor Leaf 2,' in data)
    assert ('0,Sensor Leaf 3,' in data)
    assert ('belief:Is There Motion:size,small' in data)
    assert (not 'belief:Is There Motion:size,large' in data)
    assert ('belief:Is There Motion:speed,fast' in data)
    assert ('belief:Is There Motion:speed,slow' in data)
    assert ('belief:Is There Motion:speed,n/a' in data)
    os.remove('leaf0.csv')

if exist_3:
    data = open('env0.json').read()
    assert ('"[0,"Sensor Leaf 0"' in data)
    assert ('"[0,"Sensor Leaf 1"' in data)
    assert ('"[0,"Sensor Leaf 2"' in data)
    assert ('"[0,"Sensor Leaf 3"' in data)
    assert ('"env_stuff"]":0' in data)
    assert ('"env_stuff"]":1' in data)
    assert ('"env_stuff"]":4' in data)
    assert ('"env_stuff"]":9' in data)
    os.remove('env0.json')

if exist_4:
    data = open('graph_props0.gexf').read().split('\n')
    REFS = ['Sensor_0', 'Sensor_1', 'Sensor_2', 'Sensor_3', 
            'unoccupied_0', 'unoccupied_1']
    for row in data:
        if '<edge ' in row:
            assert ('"Central"' in row)
            for r in REFS:
                if r in row:
                    REFS.remove(r)
                    break
            else:
                raise AssertionError('Missed node %s' %(r))
    assert (len(REFS) == 0)
    os.remove('graph_props0.gexf')

