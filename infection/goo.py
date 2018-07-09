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

    def _obtain_bacteria_neighbours(self, agent_index):
        '''Bla bla

        '''
        #WORK HERE

    def _add_molecules_to_env(self, agent_index, dx_molecules):
        '''Bla bla

        '''
        env_agent = self.agents_in_scope[agent_index]
        for molecule, dx in dx_molecules.items():
            x = env_agent.scaffold[molecule]
            x_new =+ dx
            env_agent.set_data('scaffold', molecule, x_new)

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

        for bacteria in bacterial_agents:
            bacteria.set_organ('actuator', 'add_molecules_to_env',
                                           self._add_molecules_to_env)

        agents = bacterial_agents + env_agents
        super().__init__(name, agents, matrix)

