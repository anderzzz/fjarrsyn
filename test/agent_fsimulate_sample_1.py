'''Integration test of finite simulation of a system

'''
import os

from core.simulator import FiniteSystemRunner
from core.sampler import AgentSampler, SystemIO

from core.agent import Agent
from core.agent_ms import AgentManagementSystem
from core.message import Belief, Resource, Essence
from core.instructor import Interpreter
from core.scaffold_map import ResourceMap

REF_ENERGY = [20.0, 120.0]
REF_BELIEF = [(11874.41406, 0.625), (11241.60156, 0.625)]

def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def propagator(system):
    for agent, aux_content in system:
        agent()

class Thinker(Agent):

    def contemplation(self, diameter_value, precision):

        diameter_value += (12742.0 - diameter_value) * 0.25 
        precision = precision * 0.5

        energy_cost = 20.0

        return diameter_value, precision, -1.0 * energy_cost

    def __call__(self):
        
        self.interpret('Contemplate')
        
    def __init__(self, name, diameter_init, energy_init, essence_value):

        super().__init__(name)

        belief = Belief('The diameter of the world', ('value', 'precision'))
        belief.set_values([diameter_init, 10.0])
        belief_dummy = Belief('Sky colour', ('colour_name',))
        belief_dummy.set_values(['blue'])
        self.set_message(belief_dummy)

        resource = Resource('Dietary energy', ('value',))
        essence = Essence('Persistence', ('value',))
        resource.set_values(energy_init)
        essence.set_values(essence_value)
        self.set_scaffolds(resource, essence)

        metabolism = ResourceMap('Dietary energy adjustment', 'delta', 'value', ('shift',))
        interpreter = Interpreter('Contemplate', self.contemplation, belief, belief,
                          metabolism)
        self.set_organ(interpreter)

agent_1 = Thinker('Alpha', 10000.0, 100.0, 2.0)
agent_2 = Thinker('Beta', 8000.0, 200.0, 5.0)
ams = AgentManagementSystem('Pair', [agent_1, agent_2])
agent_sampler_1 = AgentSampler(resource_args=[('Dietary energy', 'value')],
                               essence_args=[('Persistence', 'value')],
                               belief_args=[('The diameter of the world', 'value'),
                                            ('Sky colour', 'colour_name')],
                               sample_steps=2)
agent_sampler_2 = AgentSampler(essence_args=[('Persistence', 'value')],
                               sample_steps=3)
io = SystemIO([('tmp_1', 'to_csv', agent_sampler_1),
               ('tmp_2', 'to_json', agent_sampler_2)])

runner = FiniteSystemRunner(4, propagator, system_io=io)
runner(ams)

exist_1 = os.path.isfile('tmp_10.csv')
exist_2 = os.path.isfile('tmp_12.csv')
exist_3 = os.path.isfile('tmp_20.json')
exist_4 = os.path.isfile('tmp_23.json')
assert(exist_1)
assert(exist_2)
assert(exist_3)
assert(exist_4)

if exist_1:
    data = open('tmp_10.csv').read()
    assert ('belief:Sky colour:colour_name,blue' in data)
    assert ('belief:The diameter of the world:value,10685.5' in data)
    assert ('essence:Persistence:value,2.0' in data)
    assert ('resource:Dietary energy:value,80.0' in data)
    assert ('belief:The diameter of the world:value,9185.5' in data)
    assert ('essence:Persistence:value,5.0' in data)
    assert ('resource:Dietary energy:value,180.0' in data)
    os.remove('tmp_10.csv')

if exist_2:
    data = open('tmp_12.csv').read()
    assert ('belief:Sky colour:colour_name,blue' in data)
    assert ('belief:The diameter of the world:value,11585.21875' in data)
    assert ('essence:Persistence:value,2.0' in data)
    assert ('resource:Dietary energy:value,40.0' in data)
    assert ('belief:The diameter of the world:value,10741.46875' in data)
    assert ('essence:Persistence:value,5.0' in data)
    assert ('resource:Dietary energy:value,140.0' in data)
    os.remove('tmp_12.csv')

if exist_3:
    data = open('tmp_20.json').read()
    assert ('{"value":{"[0,"Alpha",' in data)
    assert ('"essence:Persistence:value"]":2.0' in data)
    assert ('"essence:Persistence:value"]":5.0' in data)
    assert (not 'belief' in data)
    assert (not 'resource' in data)
    os.remove('tmp_20.json')

if exist_4:
    data = open('tmp_23.json').read()
    assert ('{"value":{"[3,"Alpha",' in data)
    assert ('"essence:Persistence:value"]":2.0' in data)
    assert ('"essence:Persistence:value"]":5.0' in data)
    assert (not 'belief' in data)
    assert (not 'resource' in data)
    os.remove('tmp_23.json')
