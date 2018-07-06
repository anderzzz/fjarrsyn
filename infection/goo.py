'''Bla bla

'''
from core.agent_ms import AgentManagementSystem

from core.graph import CubicGrid

class Goo(AgentManagementSystem):
    '''Bla bla

    '''
    def __init__(self, name, agents, beaker_length):

        bacteria_matrix = CubicGrid(n_slots=beaker_length) 
        for ind, agent in enumerate(agents):
            bacteria_matrix.nodes[ind].content = agent

        super().__init__(name, agents, bacteria_matrix)
