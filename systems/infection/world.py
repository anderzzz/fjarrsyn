'''The World in which units reside, the AMS

'''
from core.agent_ms import AgentManagementSystem

from core.instructor import Sensor, Actuator
from core.message import MessageOperator
from core.scaffold_maps import ResourceMap, MapCollection

import numpy as np

class World(AgentManagementSystem):

    def _cmp_neighbour_coop(self, calling_agent_id):
        '''Bla bla

        '''
        neighbour_nodes = self.neighbours_to(calling_agent_id, agents_only=False)
        node = np.random.choice(list(neighbour_nodes))
        if node is None:
            return None

        else:
            return node.tickle('Reveal Cooperation')

    def _cmp_alter_env_resources(self, da, db, dc, calling_agent_id):
        '''Bla bla

        '''
        neighbour_nodes = self.neighbours_to(calling_agent_id, agents_only=False)
        n_neighbours = len(neighbour_nodes)

        for node in neighbour_nodes:
            node.aux_content.container['info_a'] += da / n_neighbours
            node.aux_content.container['info_b'] += db / n_neighbours
            node.aux_content.container['info_c'] += dc / n_neighbours

    def _cmp_gulp_env(self, f_gulp, calling_agent_id):
        '''Bla bla

        '''
        pass

    def __init__(self, name, agents, local_ambient):

        super().__init__(name, agents, agent_env=local_ambient)

        for agent in agents:
            
            #
            # Sensor
            sensor = Sensor('Feel Neighbour Surface', 
                            self._cmp_neighbour_coop,
                            agent.buzz['Neighbour Cooperator'],
                            agent_id_to_engine=True)
            agent.set_organ(sensor)

            #
            # Actuator
            a_resources = MessageOperator(agent.resources,
                              slice_labels=['info_a', 'info_b', 'info_c'])
            a_a_subtract = ResourceMap('Consume A', 'delta', 'info_a', ('removal',))
            a_b_subtract = ResourceMap('Consume B', 'delta', 'info_b', ('removal',))
            a_c_subtract = ResourceMap('Consume C', 'delta', 'info_c', ('removal',))
            consume_resources = MapCollection([a_a_subtract, a_b_subtract, a_c_subtract])
            actuator = Actuator('Share Resources to Neighbours',
                                self._cmp_alter_env_resources,
                                agent.direction['Resources to Share'],
                                resource_map_output=consume_resources)
            agent.set_organ(actuator)

            actuator = Actuator('Gulp Environment',
                                self._cmp_gulp_env,
                                agent.direction['Gulp from Env'],
                                agent_id_to_engine=True,
                                resource_map_output=gulped_resources)
            agent.set_organ(actuator)
