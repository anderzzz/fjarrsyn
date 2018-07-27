'''Agent Management System

'''
from uuid import uuid4
from collections import OrderedDict
import random

from core.graph import Graph, Node
from core.agent import Agent

class AgentManagementSystem(object):
    '''Base class for the medium in which agents interacts with other agents or
    other external objects. 
    
    Notes 
    -----
    The agent management system is an abstract object in which the agent 
    affordances are implemented and transplanted into the relevant agent
    organs. Any spatial network relations between agents are part of this
    system. Agents part of the system are assinged a unique ID.

    Parameters
    ----------
    name : str
        Name of the agent management system
    agents
        Iterable of agents to be part of the system, in no particular order.
    full_agents_graph : Graph, optional
        Optional Graph object that defines the spatial network relation between
        the agents of the system. If none given, a complete non-directional
        graph is used.

    Raises
    ------
    TypeError
        If a full agents graph is given that is not of the Graph class

    '''
    def neighbours_to(self, agent_index, agents_only=True):
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
        node_with_agent = self.agents_graph[agent_index]
        node_neighbours = self.agents_graph.get_neighbours(node_with_agent)
        node_neighbours = node_neighbours.tolist()
        if agents_only:
            ret_neighbours = [x.agent_content for x in node_neighbours]

        else:
            ret_neighbours = node_neighbours

        return set(ret_neighbours)
            
    def iteritems(self):
        '''Iterator over the agents of the agent management system in same
        order as they were entered during initialization.

        Returns
        -------
        agent_iter 
            Agent iterator

        '''
        return iter(self.agents_in_scope.values())

    def shuffle_iteritems(self):
        '''Iterator over the agents of the agent management system in
        randomized order

        Returns
        -------
        agent_iter
            Agent iterator

        '''
        all_agents = list(self.agents_in_scope.values())
        random.shuffle(all_agents)

        return iter(all_agents)

    def __len__(self):

        return len(self.agents_in_scope)

    def __getitem__(self, key):
        '''Bla bla

        '''

        return list(self.agents_in_scope.values())[key]

    def __setitem__(self, key, value):
        '''Bla bla

        '''
        if not isinstance(value, Agent):
            raise TypeError('Agent manager can only have members of the Agent class')

        self.agents_in_scope[key] = value

    def __delitem__(self, key):
        '''Bla bla

        '''
        if not key in self.agents_in_scope:
            raise KeyError('Unknown agent id: %s' %(key))

        node = self.agents_graph[key]
        node.agent_content = None

        agent = self.agents_in_scope[key]
        agent.agent_id_system = None

        del self.agents_in_scope[key]

    def __init__(self, name, agents, full_agents_graph=None):

        self.name = name

        #
        # Agents in scope are put into an ordered dictionary keyed on a random
        # and unique string identifier.
        #
        self.agents_in_scope = OrderedDict() 
        for agent in agents:
            agent.agent_id_system = str(uuid4())
            self.agents_in_scope[agent.agent_id_system] = agent

        #
        # The agent to agent network relation is defined, which is a complete
        # graph in case nothing specific is given.
        #
        if full_agents_graph is None:
            self.agents_graph = Graph()
            nodes = [Node('agent_%s'%(str(k)), agent) for k, agent in enumerate(agents)]
            self.agents_graph.build_complete_nondirectional(nodes)

        else:
            if isinstance(full_agents_graph, Graph):
                self.agents_graph = full_agents_graph

            else:
                raise TypeError('Agent Management System given graph not ' + \
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
