'''Integration test for dynamic changes to network

'''
import math
import networkx as nx

from core.agent import Agent
from core.agent_ms import AgentManagementSystem
from core.instructor import Sensor, Interpreter, Moulder, Actuator, Cortex
from core.message import Direction, Belief, Buzz, Feature, Essence

REF_1 = [('Ant 1', 'Ant 4'), ('Ant 1', 'Ant 2'), ('Ant 4', 'Ant 2'), ('Ant 2', 'Ant 3')]
REF_2 = [('Ant 1', 'Ant 4'), ('Ant 1', 'Ant 2'), ('Ant 4', 'Ant 2'), ('Ant 2', 'Ant 3'), ('Ant 1', 'Ant 3')]

class Ant(Agent):

    def _revealer(self, f, r):

        return f * f + r * r

    def _smell_stimulus(self, p):

        return 1.0 / (1.0 + math.exp(-5.0 * (p - 1.0)))

    def _alteration(self, intensity):

        if intensity < 1.0 / 3.0:
            return 'break'

        elif intensity < 2.0 / 3.0:
            if self.essence['relationship builder'] > 2.0 / 3.0:
                return 'create'

            elif self.essence['relationship builder'] > 1.0 / 3.0:
                return 'keep'

            else:
                return 'break'

        else:
            return 'create'

    def __init__(self, name, food_finder, rel_builder, name_try):

        super().__init__(name, True)

        essence = Essence('Ant disposition', ('food finder', 'relationship builder'))
        essence.set_values([food_finder, rel_builder])
        self.set_scaffold(essence)

        belief = Belief('Who to connect with', ('name',))
        belief.set_values([name_try])
        self.set_message(belief)

        feature = Feature('Smell', ('profile',))
        cortex = Cortex('Reveal disposition', self._revealer, essence, feature)
        self.set_organ(cortex)

        buzz = Buzz('Smell perception', ('profile',))
        belief = Belief('Nice guy', ('intensity',))
        interpreter = Interpreter('Is this a good one?', self._smell_stimulus,
                                  buzz, belief)
        self.set_message(buzz)
        self.set_organ(interpreter)

        direction = Direction('Formation action', ('command',))
        moulder = Moulder('Should contact be altered?', self._alteration,
                          belief, direction)
        self.set_message(direction)
        self.set_organ(moulder)

        self.name_try = name_try

class AntColony(AgentManagementSystem):

    def _nose(self, agent_index):

        agent_calling = self[agent_index]

        while True:
            a_trial, aux = self.choice(True)
            if a_trial.name in agent_calling.belief['Who to connect with'].values():
                break

        sense_feature = a_trial.tickle('Reveal disposition')

        return sense_feature.values()

    def _change_network(self, command, agent_index):

        agent_calling = self[agent_index]

        while True:
            a_trial, aux = self.choice(True)
            if a_trial.name in agent_calling.belief['Who to connect with'].values():
                break

        agent_id_considered = a_trial.agent_id_system

        edge_here, dummy = self.edge_property(agent_index, agent_id_considered)

        if command == 'keep':
            pass

        elif command == 'break':
            if edge_here:
                self.edge_edit(agent_index, agent_id_considered, delete=True)

        elif command == 'create':
            if not edge_here:
                self.edge_edit(agent_index, agent_id_considered, add=True)

    def __init__(self, name, agents):

        super().__init__(name, agents)

        for agent, aux in sorted(self, key=lambda x: x[0].name):

            sensor = Sensor('Sense odour', self._nose, agent.buzz['Smell perception']) 
            agent.set_organ(sensor)

            actuator = Actuator('Change network', self._change_network,
                                agent.direction['Formation action'])
            agent.set_organ(actuator)

ant1 = Ant('Ant 1', 1.0, 1.0, 'Ant 3')
ant2 = Ant('Ant 2', 1.0, 1.0, 'Ant 1')
ant3 = Ant('Ant 3', 0.0, 0.0, 'Ant 4')
ant4 = Ant('Ant 4', 0.0, 0.8, 'Ant 1')

colony = AntColony('The Pile', [ant1, ant2, ant3, ant4])
assert (nx.number_of_edges(colony.agents_graph) == 6)

for agent, aux in colony:
    agent.sense('Sense odour')
    agent.interpret('Is this a good one?')
    agent.mould('Should contact be altered?')
    agent.act('Change network')


assert (nx.number_of_edges(colony.agents_graph) == len(REF_1))
for edge in nx.edges(colony.agents_graph):
    n1 = edge[0].agent_content.name
    n2 = edge[1].agent_content.name
    if (n1, n2) in REF_1 or (n2, n1) in REF_1:
        pass
    else:
        raise AssertionError('Misses (%s, %s)' %(n1, n2))

for agent, aux in colony:
    if agent.name == 'Ant 3':
        agent.belief['Who to connect with'].set_values(['Ant 1'])
    elif agent.name == 'Ant 4':
        agent.belief['Who to connect with'].set_values(['Ant 3'])
    elif agent.name == 'Ant 1':
        agent.belief['Who to connect with'].set_values(['Ant 2'])
    elif agent.name == 'Ant 2':
        agent.belief['Who to connect with'].set_values(['Ant 1'])

    agent.sense('Sense odour')
    agent.interpret('Is this a good one?')
    agent.mould('Should contact be altered?')
    agent.act('Change network')

assert (nx.number_of_edges(colony.agents_graph) == len(REF_2))
for edge in nx.edges(colony.agents_graph):
    n1 = edge[0].agent_content.name
    n2 = edge[1].agent_content.name
    if (n1, n2) in REF_2 or (n2, n1) in REF_2:
        pass
    else:
        raise AssertionError('Misses (%s, %s)' %(n1, n2))

