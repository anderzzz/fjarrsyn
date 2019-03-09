'''The World in which units reside, the AMS

'''
from core.agent_ms import AgentManagementSystem

from core.instructor import Sensor, Actuator

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
