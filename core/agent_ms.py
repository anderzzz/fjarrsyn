'''Bla bla

'''
from uuid import uuid4

class AgentManagementSystem(object):
    '''Bla bla

    '''
    def agents_iter(self):
        '''Bla bla

        '''
        return iter(self.agents_in_scope.values())

    def __init__(self, name, agents, agents_graph=None):

        self.name = name

        self.agents_in_scope = {}
        for agent in agents:
            agent.agent_id_system = str(uuid4())
            self.agents_in_scope[agent.agent_id_system] = agent

        if agents_graph is None:
            agents_graph = Graph()
            nodes = [Node('dummy', agent) for agent in agents]
            agents_graph.build_complete_nondirectional(nodes)
