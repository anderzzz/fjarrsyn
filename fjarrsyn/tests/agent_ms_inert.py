from fjarrsyn.core.agent import Agent
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.message import Essence, Belief, Direction
from fjarrsyn.core.instructor import Moulder, Actuator
from fjarrsyn.core.mover import Mover

from fjarrsyn.simulation.simulator import FiniteSystemRunner

import numpy as np
import numpy.random
np.random.seed(79)

KILLED = set([])

class Killer(Agent):

    def __init__(self, name, intent, strength, precision):

        super().__init__(name)

        essence = Essence('Skills', ('strength', 'precision'))
        essence.set_values([strength, precision])
        belief = Belief('Intent to kill', ('yes_no',))
        belief.set_values([intent])

        direction = Direction('Push spear outward', ('yes_no',))
        moulder = Moulder('Attempt to kill', lambda x: x, belief, direction)
        self.set_organ(moulder)
        self.set_messages(belief, direction)
        self.set_scaffold(essence)

class Coluseum(AgentManagementSystem):

    def kill_attempt(self, push_or_not, strength, precision, agent_id):

        if not push_or_not:
            pass

        else:
            test_metric = strength * precision
            if test_metric > np.random.ranf():
                nn = self.neighbours_to(agent_id)
                nn = [n for n in nn if not n is None]
                other_agent = nn[0]
                other_agent.inert = True

                KILLED.add(other_agent.agent_id_system)

    def __init__(self, name, agents):

        super().__init__(name, agents)

        for node in self:
            agent = node.agent_content

            actuator = Actuator('Kill stroke', self.kill_attempt,
                                agent.direction['Push spear outward'],
                                essence_op_input=agent.essence,
                                agent_id_to_engine=True)
            agent.set_organ(actuator)

def propagator(system):
    
    n_agents = len(system)
    for agent in system.cycle_nodes(True, n_agents):
        if not agent.inert:
            agent.mould('Attempt to kill')
            agent.act('Kill stroke')

    system.cleanse_inert()
    

agent_1 = Killer('maximus 1', True, 0.9, 0.7)
agent_2 = Killer('maximus 2', True, 0.6, 1.0)
agent_3 = Killer('maximus 3', True, 1.0, 0.3)
agent_4 = Killer('maximus 4', False, 0.2, 0.2)

coluseum = Coluseum('That Place', [agent_1, agent_2, agent_3, agent_4])
agents_start = set(coluseum.agents_in_scope.keys())

mover = Mover('play the game', propagator)
runner = FiniteSystemRunner(20, mover)
runner(coluseum)

alive = set([x.agent_content.agent_id_system for x in coluseum if not x.agent_content is None])

assert (KILLED & alive == set([]))
assert (KILLED | alive == agents_start)
assert (len(alive) == 1)
