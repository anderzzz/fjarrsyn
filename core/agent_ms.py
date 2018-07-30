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
            
    def shuffle_agents(self, max_iter):
        '''Iterator over agents in system in random order. 

        Notes
        -----
        The element is generated in each iteration from the current set of
        agents in scope. Therefore, this iterator is stable to additions or
        deletions of agents of the system during the iteration.

        Parameters
        ----------
        max_iter : int
            The number of entries the iterator should yield. If set to negative
            number the iteration is infinite.

        Yields
        ------
        entry : Agent
            Random agent from the system

        Raises
        ------
        StopIteration
            In case the system is void of agents

        '''
        def _terminator(counter):
            if (counter < max_iter) or (max_iter < 0):
                return True
            else:
                return False
            
        counter = 0
        while _terminator(counter): 
            counter += 1

            if len(self.agents_in_scope.values()) > 0:
                entry = random.choice(list(self.agents_in_scope.values()))

            else:
                raise StopIteration('No agents left in system')

            yield entry

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

        node = self.agents_graph[key]
        node.agent_content = None

        agent = self.agents_in_scope[key]
        agent.agent_id_system = None

        del self.agents_in_scope[key]

    def append(self, agent):
        '''Append an agent to the system. This assigns a new agent ID

        Parameters
        ----------
        agent : Agent
            Agent to append to system

        '''
        if not isinstance(agent, Agent):
            raise TypeError('Only instances of the Agent class can be ' + \
                            'appended to an Agent System')

        agent.agent_id_system = str(uuid4())
        self.agents_in_scope[agent.agent_id_system] = agent

    def __init__(self, name, agents, full_agents_graph=None):

        self.name = name

        #
        # Agents in scope are put into an ordered dictionary keyed on a random
        # and unique string identifier.
        #
        self.agents_in_scope = OrderedDict() 
        for agent in agents:
            self.append(agent)

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
