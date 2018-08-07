'''Agent Management System

'''
from uuid import uuid4
from collections import OrderedDict
import numpy as np
import numpy.random
import networkx as nx

from core.graph import node_by_agent_id 
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
        node_with_agent = node_by_agent_id(agent_index, self.agents_graph)
        node_neighbours = self.agents_graph.neighbors(node_with_agent)
        node_neighbours = list(node_neighbours)
        if agents_only:
            ret_neighbours = [x.agent_content for x in node_neighbours]

        else:
            ret_neighbours = node_neighbours

        return set(ret_neighbours)
            
    def shuffle_iter(self, max_iter):
        '''Iterator over node content in system in random order. 

        Notes
        -----
        The element is generated in each iteration from the current set of
        nodes. Therefore, this iterator is stable to additions or
        deletions of nodes or agents contained in nodes of the system 
        during the iteration.

        Parameters
        ----------
        max_iter : int
            The number of entries the iterator should yield. If set to negative
            number the iteration is infinite.

        Yields
        ------
        agent_content : Agent
            Agent of node. Is `None` in case no agent occupies the node
        aux_content 
            Any auxiliary content of the node

        Raises
        ------
        StopIteration
            In case the system is void of nodes

        '''
        def _terminator(counter):
            if (counter < max_iter) or (max_iter < 0):
                return True
            else:
                return False
            
        counter = 0
        while _terminator(counter): 
            counter += 1

            if len(self.agents_graph.number_of_nodes()) > 0:
                entry = np.random.choice(self.agents_graph.nodes)

            else:
                raise StopIteration('No nodes left in system')

            yield entry.agent_content, entry.aux_content

    def __len__(self):

        return len(self.agents_in_scope)

    def __iter__(self):
        '''Iterator over the nodes and their content of the agent system.

        Notes
        -----
        Graphs can contain nodes that are not populated by an agent. This
        manifest itself as `agent_content` being `None`. The loop using the
        iterator should therefore handle these cases. Also note that if nodes
        are added or deleted to the graph while the iterator is used, can
        create bad behaviour.

        Yields
        ------
        agent_content : Agent
            Agent of node. Is `None` in case no agent occupies the node
        aux_content 
            Any auxiliary content of the node

        '''
        for node in self.agents_graph:
            yield node.agent_content, node.aux_content

    def __getitem__(self, key):
        '''Return agent in agent system based on agent system id

        Parameters
        ----------
        key : str
            Agent system ID

        Returns
        -------
        agent : Agent
            Agent in system with given ID

        Raises
        ------
        KeyError
            If system does not contain an agent of given ID

        '''
        if not key in self.agents_in_scope:
            raise KeyError('Unknown agent id: %s' %(key))

        return self.agents_in_scope[key] 

    def __delitem__(self, key):
        '''Delete agent from system based on its key

        Notes
        -----
        The deletion of the agent includes both its deletion from the node it
        occupies as well as the dictionary of agents within the system scope.
        The deletion operation does not alter the graph topology.

        Parameters
        ----------
        key : str
            Agent system ID

        Raises
        ------
        KeyError
            If system does not contain an agent of given ID

        '''
        if not key in self.agents_in_scope:
            raise KeyError('Unknown agent id: %s' %(key))

        node = node_by_agent_id(key, self.agents_graph)
        node.agent_content = None

        agent = self.agents_in_scope[key]
        agent.agent_id_system = None

        del self.agents_in_scope[key]

    def bookkeep(self, agent):
        '''Add an agent to the book keeping of the agent management system

        Parameters
        ----------
        agent : Agent
            Agent to add to system

        '''
        if not isinstance(agent, Agent):
            raise TypeError('Only instances of the Agent class can be ' + \
                            'in Agent System book keeping')

        agent.agent_id_system = str(uuid4())
        self.agents_in_scope[agent.agent_id_system] = agent

    def situate(self, agent, node):
        '''Join an agent to a node and add it to the system book keeping

        Parameters
        ----------
        agent : Agent
            Agent to add to system
        node : Node
            Node of graph in which to situate the agent to

        '''
        self.bookkeep(agent)
        node.agent_content = agent

    def __init__(self, name, agents, full_agents_graph=None):

        self.name = name

        #
        # The agent to agent network relation is defined, which is a complete
        # graph in case nothing specific is given.
        #
        if full_agents_graph is None:
            nodes = [Node('agent_%s'%(str(k)), agent) for k, agent in enumerate(agents)]
            self.agents_graph = nx.complete_graph(nodes)

        else:
            if isinstance(full_agents_graph, nx.Graph):
                self.agents_graph = full_agents_graph

            else:
                raise TypeError('Agent Management System given graph not ' + \
                                'of the Graph class')

        self.agents_graph.name = 'Agents Graph of System %s' %(self.name)

        #
        # The agents are added to the system book keeping
        #
        self.agents_in_scope = OrderedDict()
        for agent in agents:
            self.bookkeep(agent)

        #
        # The Agent system can itself have natural constants. These are
        # assigned in child classes, the container declared here.
        #
        self.system_constants = {}

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
