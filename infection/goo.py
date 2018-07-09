'''Bla bla

'''
import copy
import random

from core.agent_ms import AgentManagementSystem
from core.graph import CubicGrid

class Goo(AgentManagementSystem):
    '''Bla bla

    '''
    def _gulp_environment(self, agent_index):
        '''Bla bla

        '''
        pass

    def _share_molecules(self, agent_index):
        '''Bla bla

        '''
        pass

    def _obtain_neighbour_surface(self, agent_index):
        '''Bla bla

        '''
        pass

    def __init__(self, name, beaker_length, bacterial_agents, env_agent):

        matrix = CubicGrid(n_slots=beaker_length) 
        matrix_size = len(matrix)

        env_agents = [copy.deepcopy(env_agent) for k in range(matrix_size)]
        random_index = random.sample(range(matrix_size), 
                                     len(bacterial_agents))

        for ind, env_agent in enumerate(env_agents):
            if ind in random_index:
                bact_agent = bacterial_agents.pop(0)
                matrix.nodes[ind].content = {'bacteria':bact_agent,
                                             'env':env_agent}
            else:
                matrix.nodes[ind].content = {'bacteria':None,
                                             'env':env_agent}

        # WORK HERE
        for bacteria in bacterial_agents:
            bacteria.set_actuator('take_nutrients', self._take_nutrients)

        agents = bacterial_agents + env_agents
        super().__init__(name, agents, matrix)

