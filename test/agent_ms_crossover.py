'''Integration test of cross-over between a pair of agents in order to generate
a third new agent

'''
import numpy as np
import numpy.random

from core.agent import Agent
from core.agent_ms import AgentManagementSystem
from core.graph import Node
from core.message import Belief, Direction, Buzz, Resource, Essence
from core.instructor import Sensor, Interpreter, Moulder, Actuator
from core.scaffold_map import EssenceMap, ResourceMap, universal_map_maker, \
                              MapCollection

class Person(Agent):

    def ejector(self, should_eject):

        e_map = universal_map_maker(self.essence, 'reset', ('value',)) 
        e_map.set_values(self.essence.values())

        r1_map = ResourceMap('item1', 'delta', 'item_1', ('value',))
        r2_map = ResourceMap('item2', 'delta', 'item_2', ('value',))
        r_map = MapCollection([r1_map, r2_map]) 

        split_half = [x / 2.0 for key, x in self.resource.items() if 'item' in key]
        r_map.set_values(split_half)

        ret = [(e_map, r_map)]
        ret.extend([-1.0 * x for x in split_half])

        return tuple(ret)

    def make_baby(self, dummy):

        the_baby = self.__class__('arnold', True, True, True, True)
        the_baby_essence_map = universal_map_maker(the_baby.essence, 'reset', ('value',)) 

        parent_1_essence_map, parent_1_resource_map = self.resource['External gene']

        parent_2_essence_map = universal_map_maker(self.essence, 'reset', ('value',)) 
        parent_2_essence_map.set_values(self.essence.values())

        container = []
        for scaffold_key in the_baby.essence.keys():
            array_1 = parent_1_essence_map[scaffold_key]
            array_2 = parent_2_essence_map[scaffold_key]
            array_transmit = np.random.choice([array_1, array_2])
            container.append(array_transmit.values()[0])

        the_baby_essence_map.set_values(container)

        the_baby_essence_map.apply_to(the_baby)
        parent_1_resource_map.apply_to(the_baby)

        return the_baby

    def __init__(self, name, rude, loud, big, foul):

        super().__init__(name, strict_engine=True)

        resource = Resource('Storage', ('item_1', 'item_2', 'External gene'))
        resource.set_values([2, 4, None])
        essence = Essence('Persona', ('rude', 'loud', 'big', 'foul'))
        essence.set_values([rude, loud, big, foul])

        self.set_scaffolds(resource, essence)

        buzz = Buzz('Env Feeling', ('gene_bump',))
        belief = Belief('Gene in Env', ('yes_no',))
        interpreter = Interpreter('Is gene in env?', lambda x: x, buzz, belief)
        direction_r = Direction('Receive', ('yes_no',))
        moulder_r = Moulder('Receive gene', lambda x: x, belief, direction_r)
        belief_eject = Belief('Time to eject', ('yes_no',))
        direction_e = Direction('Eject', ('payload',))
        r1_map = ResourceMap('item1', 'delta', 'item_1', ('value',))
        r2_map = ResourceMap('item2', 'delta', 'item_2', ('value',))
        r_map = MapCollection([r1_map, r2_map]) 
        moulder_e = Moulder('Eject gene', self.ejector, belief_eject,
                            direction_e, r_map)
        moulder_cross = Moulder('Make cross-over baby', self.make_baby,
                                belief_eject, direction_e)

        self.set_organs(interpreter, moulder_r, moulder_e, moulder_cross)
        self.set_messages(buzz, belief, direction_r, direction_e)

class SimpleEnv:

    def __init__(self, content=None):
        self.content = content

class Arena(AgentManagementSystem):

    def feeler(self, agent_index):
        
        aux_env = self.get(agent_index, get_aux=True)
        if not aux_env.content is None:
            return True
        else:
            return False

    def retriever(self, go_ahead, agent_index):
        if go_ahead:
            aux_env = self.get(agent_index, get_aux=True)

            return [aux_env.content]

        else:
            return [None]
            
    def ejecter(self, payload, agent_index):

        node_neighbours = list(self.neighbours_to(agent_index, False))
        node = np.random.choice(node_neighbours)
        aux_to_eject_to = node.aux_content

        aux_to_eject_to.content = payload 

    def birth(self, payload, agent_index):

        node_parent = self.get(agent_index, get_node=True)
        node = Node('child', None, SimpleEnv())
        self.agents_graph.add_node(node)
        self.agents_graph.add_edge(node, node_parent)
        self.situate(payload, node)

    def __init__(self, name, agents, env_atom):

        super().__init__(name, agents, agent_env=env_atom)

        for agent in agents:
            sensor = Sensor('Feel for gene in Env', self.feeler, 
                            agent.buzz['Env Feeling'])
            stuff = ResourceMap('Env Payload', 'reset', 'External gene', ('item',))
            actuator_r = Actuator('Suck up gene', self.retriever,
                                agent.direction['Receive'], stuff)
            actuator_e = Actuator('Eject gene', self.ejecter,
                                agent.direction['Eject'])
            actuator_b = Actuator('Birth baby', self.birth,
                                  agent.direction['Eject'])
            agent.set_organs(sensor, actuator_r, actuator_e, actuator_b)


person_1 = Person('A', True, True, True, True)
person_2 = Person('B', False, False, False, False)
ams = Arena('A Place', [person_1, person_2], SimpleEnv(None))

agent_1, dummy = ams.choice()
agent_1.mould('Eject gene')
agent_1.act('Eject gene')

agent_2 = ams.neighbours_to(agent_1.agent_id_system).pop()
agent_2.sense('Feel for gene in Env')
agent_2.interpret('Is gene in env?')
agent_2.mould('Receive gene')
agent_2.act('Suck up gene')
agent_2.mould('Make cross-over baby')
agent_2.act('Birth baby')

for a, e in ams:
    print (a)
    print (a.essence)

for a1, a2 in ams.agents_graph.edges:
    print (a1.agent_content.name, a2.agent_content.name)
