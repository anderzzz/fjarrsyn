'''Agent Management System

'''
from uuid import uuid4
from collections import OrderedDict

from core.graph import Graph

class AgentManagementSystem(object):
    '''Bla bla

    '''
    def graph_neighbours_to(self, agent_index):
        '''Method to extract the agent objects neighbours in the graph to the
        agent of a certain system identifier

        Parameters
        ----------
        agent_index : str
            The agent identifier within the system, available from the
            `agent_id_system` attribute

        Returns
        -------
        agents_hood : set
            Set of agents directly adjacent to the given agent

        '''
        #TBD: REFACTOR TO USE __GETITEM__ FUNCTIONALITY OF GRAPH
        adjacency_list = self.agents_graph.get_adjacency_list()

        ret_list = []
        for ind, connection_tuple in adjacency_list.iteritems():
            agent_id1 = connection_tuple[0].content.agent_id_system
            agent_id2 = connection_tuple[1].content.agent_id_system
           
            if agent_id1 == agent_index:
                ret_list.append(connection_tuple[1].agent_content)
            elif agent_id2 == agent_index:
                ret_list.append(connection_tuple[0].agent_content)

        return set(ret_list)

    def iteritems(self):
        '''Iterator over the agents of the agent management system in no
        particular order

        Returns
        -------
        agent_iter 
            Agent iterator

        '''
        return iter(self.agents_in_scope.values())

    def __len__(self):

        return len(self.agents_in_scope)

    def __getitem__(self, key):

        return list(self.agents_in_scope.values())[key]

    def __init__(self, name, agents, full_agents_graph=None):

        self.name = name

        self.agents_in_scope = OrderedDict() 
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

class AgentSystemSummarizer(object):
    '''Bla bla

    '''
    def nnodes(self):
        '''Bla bla

        '''
        return len(self.system)

    def graph_properties(self):
        '''Bla bla

        '''
        # Return a namedtuple with descriptive data of graph
        pass

    def __init__(self, agent_ms):

        self.system = agent_ms
