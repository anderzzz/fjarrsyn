'''Bla bla

'''
from core.agent_ms import AgentManagementSystem

from core.graph import CubicGrid, Node

class Goo(AgentManagementSystem):
    '''Bla bla

    '''
    def __init__(self, name, agents):

        bacteria_matrix = CubicGrid(n_slots=3) 
        print (bacteria_matrix.grid_graph.get_adjacency_matrix())
        raise RuntimeError('dummy')
        nodes = [Node('bacteria_%s' %(str(k)), agent) for k, agent in enumerate(agents)]

        super().__init__(name, agents)
