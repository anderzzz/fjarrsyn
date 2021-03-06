'''Integration test of finite simulation of a system of two agents

'''
import pytest

from fjarrsyn.simulation.simulator import FiniteSystemRunner

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.message import Belief, Resource, Essence
from fjarrsyn.core.instructor import Interpreter
from fjarrsyn.core.scaffold_map import ResourceMap
from fjarrsyn.core.mover import Mover

REF_ENERGY = [20.0, 120.0]
REF_BELIEF = [(11874.41406, 0.625), (11241.60156, 0.625)]

def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def propagator(system):
    for agent in system.cycle_nodes(True, len(system)):
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

        super().__init__(name, strict_engine=True)

        belief = Belief('The diameter of the world', ('value', 'precision'))
        belief.set_values([diameter_init, 10.0])

        resource = Resource('Dietary energy', ('value',))
        essence = Essence('Persistence', ('value',))
        resource.set_values(energy_init)
        essence.set_values(essence_value)
        self.set_scaffolds(resource, essence)

        metabolism = ResourceMap('Dietary energy adjustment', 'delta', 'value', ('shift',))
        interpreter = Interpreter('Contemplate', self.contemplation, belief, belief,
                          metabolism)
        self.set_organ(interpreter)


def test_main():
    '''Integration test: finite system simulation, two agents.

    '''
    agent_1 = Thinker('Alpha', 10000.0, 100.0, 2.0)
    agent_2 = Thinker('Beta', 8000.0, 200.0, 5.0)
    ams = AgentManagementSystem('Pair', [agent_1, agent_2])

    mover = Mover('move_thinker', propagator)
    runner = FiniteSystemRunner(4, mover)
    runner(ams)

    assert (isclose(agent_1.resource['value'], REF_ENERGY[0]))
    assert (isclose(agent_2.resource['value'], REF_ENERGY[1]))
    assert (isclose(agent_1.belief['The diameter of the world']['value'], REF_BELIEF[0][0]))
    assert (isclose(agent_1.belief['The diameter of the world']['precision'], REF_BELIEF[0][1]))
    assert (isclose(agent_2.belief['The diameter of the world']['value'], REF_BELIEF[1][0]))
    assert (isclose(agent_2.belief['The diameter of the world']['precision'], REF_BELIEF[1][1]))
