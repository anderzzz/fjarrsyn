'''Bla bla

'''
from uuid import uuid4

from core.graph import Graph

class AgentManagementSystem(object):
    '''Bla bla

    '''
    def get_neighbours(self, agent_index):
        '''Bla bla

        '''
        adjacency_list = self.agents_graph.get_adjacency_list()

        ret_list = []
        for ind, connection_tuple in adjacency_list.iteritems():
            agent_id1 = connection_tuple[0].content.agent_id_system
            agent_id2 = connection_tuple[1].content.agent_id_system
           
            if agent_id1 == agent_index:
                ret_list.append(connection_tuple[1].content)
            elif agent_id2 == agent_index:
                ret_list.append(connection_tuple[0].content)

        return set(ret_list)

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
