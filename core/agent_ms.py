'''Bla bla

'''
from uuid import uuid4

from core.graph import Graph

class AgentManagementSystem(object):
    '''Bla bla

    '''
    def agents_iter(self):
        '''Bla bla

        '''
        return iter(self.agents_in_scope.values())

    def __init__(self, name, agents, full_agents_graph=None, seed=42):

        self.name = name

        self.agents_in_scope = {}
        for agent in agents:
            agent.agent_id_system = str(uuid4())
            self.agents_in_scope[agent.agent_id_system] = agent


        if full_agents_graph is None:
            self.agents_graph = Graph()
            nodes = [Node('agent_%s'%(str(k)), agent) for k, agent in enumerate(agents)]
            self.agents_graph.build_complete_nondirectional(nodes)

        else:
            if isinstance(full_agents_graph, Graph):
                self.agents_graph = full_agents_graph
            else:
                raise RuntimeError('Agent Management System given graph not ' + \
                                   'of the Graph class')
