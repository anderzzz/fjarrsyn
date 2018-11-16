'''Agent Management System

'''
from uuid import uuid4
from collections import OrderedDict
import numpy as np
import numpy.random
import networkx as nx

from core.agent import Agent
from core.graph import Node
from core.instructor import Compulsion, Mutation

class AgentManagementSystem(object):
    '''Base class for the medium in which agents interacts with other agents or
    other external objects. 
    
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

    Notes 
    -----
    The agent management system is an abstract object in which the agent 
    affordances are implemented and transplanted into the relevant agent
    organs. Any spatial network relations between agents are part of this
    system. Agents part of the system are assinged a unique ID.

    '''
    def neighbours_to(self, agent_index, agents_only=True):
        '''Method to extract the agent objects neighbours in the graph to the
        agent of a certain system identifier

        Parameters
        ----------
        agent_index : str
            The agent identifier within the system, available from the
            `agent_id_system` attribute
        agents_only : bool, optional
            If True, only the agents of the graph neighbours are returned,
            otherwise the entire Node object of the neighbours

        Returns
        -------
        agents_hood : set
            Set of agents (or Nodes) directly adjacent to the given agent

        '''
        node_with_agent = self.node_from_agent_id_[agent_index]
        node_neighbours = self.agents_graph.neighbors(node_with_agent)
        node_neighbours = list(node_neighbours)
        if agents_only:
            ret_neighbours = [x.agent_content for x in node_neighbours]

        else:
            ret_neighbours = node_neighbours

        return set(ret_neighbours)

    def edge_property(self, agent_index_1, agent_index_2):
        '''Determine property of edge, including if there is an edge at all

        Parameters
        ----------
        agent_index_1 : str
            Index of first agent in system
        agent_index_2 : str
            Index of second agent in system

        Returns
        -------

        '''
        node_agent_1 = self.node_from_agent_id_[agent_index_1]
        node_agent_2 = self.node_from_agent_id_[agent_index_2]

        there_is_edge = (node_agent_1, node_agent_2) in self.agents_graph.edges

        if not there_is_edge:
            return there_is_edge, None

        else:
            edge_attribute = self.agents_graph[node_agent_1][node_agent_2]
            return there_is_edge, edge_attribute

    def edge_edit(self, agent_index_1, agent_index_2, 
                  delete=False, add=False, weight=None):
        '''Edit the agent graph

        Notes
        -----
        The method does not verify if the graph operation makes sense given the
        current topology. If not, exceptions are raised in graph library
        method. 

        Parameters
        ----------
        agent_index_1 : str
            Index of first agent in system
        agent_index_2 : str
            Index of second agent in system
        delete : bool, optional
            If True, delete edge between the two agents
        add : bool, optional
            If True, add edge between the two agents
        weight : optional
            Add or set weight attribute of edge, either previously existing or
            just added

        Raises
        ------
        NetworkXError 
            If operations on the graph are meaningless in current topology

        '''
        node_agent_1 = self.node_from_agent_id_[agent_index_1]
        node_agent_2 = self.node_from_agent_id_[agent_index_2]

        if delete:
            self.agents_graph.remove_edge(node_agent_1, node_agent_2)

        if add:
            self.agents_graph.add_edge(node_agent_1, node_agent_2)

        if not weight is None:
            raise NotImplementedError('Weighted graphs not fully implemented')
            self.agents_graph.edges[node_agent_1, node_agent_2]['weight'] = weight

    def choice(self, require_agent=False):
        '''Pick one node at random

        Parameters
        ----------
        require_agent : bool, optional
            If True, the random selection is made from the subset of nodes that
            contain agents. If False, the random selection is made from the
            full set of nodes.

        Returns
        -------
        agent_content : Agent
            Agent of node. Is `None` in case no agent occupies the node
        aux_content 
            Any auxiliary content of the node

        '''
        if not require_agent:
            entry = np.random.choice(list(self.agents_graph.nodes))

        else:
            nodes_shuffle = np.random.choice(list(self.agents_graph.nodes),
                                             size=len(self.agents_graph.nodes))
            for node in nodes_shuffle:
                if not node.agent_content is None:
                    entry = node
                    break

            else:
                raise RuntimeError('The graph contains no nodes with agents')
            
        return entry.agent_content, entry.aux_content

    def shuffle_iter(self, max_iter, replace=False):
        '''Iterator over node content in system as a random selection with
        or without replacement. 

        Notes
        -----
        Graphs can contain nodes that are not populated by an agent. This
        manifest itself as `agent_content` being `None`. The loop using the
        iterator should therefore handle these cases. Also note that if nodes
        are added or deleted to the graph inside a loop using the iterator,
        bad behaviour can be produced. If such graph operations are to be
        performed, `choice` can be used to pick nodes one by one.

        Parameters
        ----------
        max_iter : int
            The number of entries the iterator should yield. If set to negative
            number the iteration is infinite.
        replace : bool, optional
            If True, the iterator selects nodes randomly with replacement such
            that an uneven sampling of the nodes can be generated. If False,
            the iterator selects nodes in random order, but guaranteed to
            generate an even sampling of the nodes.

        Yields
        ------
        agent_content : Agent
            Agent of node. Is `None` in case no agent occupies the node
        aux_content 
            Any auxiliary content of the node

        '''
        def _terminator(counter):
            if (counter < max_iter) or (max_iter < 0):
                return True
            else:
                return False
            
        shuffled = []
        counter = 0
        while _terminator(counter): 
            counter += 1

            if len(shuffled) == 0:
                shuffled = list(np.random.choice(list(self.agents_graph.nodes), 
                                                 size=len(self.agents_graph.nodes),
                                                 replace=replace))

            entry = shuffled.pop()

            yield entry.agent_content, entry.aux_content

    def __iter__(self):
        '''Iterator over all nodes and their content of the agent system.

        Notes
        -----
        Graphs can contain nodes that are not populated by an agent. This
        manifest itself as `agent_content` being `None`. The loop using the
        iterator should therefore handle these cases. Also note that if nodes
        are added or deleted to the graph inside a loop using the iterator,
        bad behaviour can be produced. If such graph operations are to be
        performed, `choice` can be used to pick nodes one by one.

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

        node = self.node_from_agent_id_[key]
        node.agent_content = None
        del self.node_from_agent_id_[key]

        agent = self.agents_in_scope[key]
        agent.agent_id_system = None
        del self.agents_in_scope[key]

    def set_law(self, law):
        '''Add a law for agents in the system

        Parameters
        ----------
        law
            The instructor class instance to add to the agent management
            system. The law must be one the known law classes

        Raises
        ------
        TypeError
            If the `law` that is given as input is not an instance of a known
            law class

        '''
        if isinstance(law, Compulsion):
            self.compulsion[law.name] = law

        elif isinstance(law, Mutation):
            self.mutation[law.name] = law

        else:
            raise TypeError('Unknown law type: %s' %(str(type(law))))

    def set_laws(self, *laws):
        '''Add laws for agents to the system

        Parameters
        ----------
        laws
            Argument tuple of the laws to add to the agent. Must be instances
            of known law classes

        '''
        for law in laws:
            self.set_law(law)

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
        self.node_from_agent_id_[agent.agent_id_system] = node

    def compel(self, agent, phrase, validate_lawbook=False):
        '''Verb for the agent management system to execute a Compulsion

        Notes
        -----
        The method collects the Compulsion associated with the input phrase and
        compels the given agent accordingly

        Parameters
        ----------
        agent : Agent
            Agent to be compelled
        phrase : str
            Name of the compulsion to execute
        validate_lawbook : bool, optional
            If True, validate that Compulsion of given phrase should be
            possible to apply to given agent. 

        Raises
        ------
        KeyError
            If system contains no compulsion with the phrase
        TypeError
            If it is not an agent that is compelled
        RuntimeError
            If the agent does not have the phrase in the law book

        '''
        if not isinstance(agent, Agent):
            raise TypeError('Only instances of the Agent class can be ' + \
                            'compelled by Agent System')

        if not phrase in self.compulsion:
            raise KeyError('Agent System lacks compulsion for %s' %(phrase))

        else:
            the_compulsion = self.compulsion[phrase]

        if validate_lawbook:
            if not phrase in self.lawbook[agent.agent_id_system]:
                raise RuntimeError('Compulsion %s is not in law book ' %(phrase) + \
                                   'for agent with ID %s' %(agent.agent_id_system))

        did_it_compel = the_compulsion(agent.agent_id_system)
        if self.strict_engine and (not did_it_compel is True):
            raise did_it_compel

        agent.apply_map(the_compulsion.scaffold_map)

    def mutate(self, agent, phrase, validate_lawbook=False):
        '''Verb for the agent management system to execute a Mutation or
        MultiMutation 

        Notes
        -----
        The method collects the Mutation (or MultiMutation) associated 
        with the input phrase and compels the given agent accordingly

        Parameters
        ----------
        agent : Agent
            Agent to be mutated 
        phrase : str
            Name of the mutation to execute
        validate_lawbook : bool, optional
            If True, validate that Mutation of given phrase should be
            possible to apply to given agent. 

        Raises
        ------
        KeyError
            If system contains no mutation with the phrase
        TypeError
            If it is not an agent that is mutated
        RuntimeError
            If the agent does not have the phrase in the law book

        '''
        if not isinstance(agent, Agent): 
            raise TypeError('Only instances of the Agent class can be ' + \
                            'mutated by Agent System')

        if not phrase in self.mutation:
            raise KeyError('Agent System lacks mutation for %s' %(phrase))

        else:
            the_mutation = self.mutation[phrase]

        if validate_lawbook:
            if not phrase in self.lawbook[agent.agent_id_system]:
                raise RuntimeError('Compulsion %s is not in law book ' %(phrase) + \
                                   'for agent with ID %s' %(agent.agent_id_system))

        did_it_mutate = the_mutation(agent.agent_id_system)
        if self.strict_engine and (not did_it_mutate is True):
            raise did_it_mutate

        agent.apply_map(the_mutation.scaffold_map)

    def engage_all_verbs(self, agent, validate_lawbook=False):
        '''Convenience function to apply all verbs to the given agent

        Parameters
        ----------
        agent : Agent
            The agent to apply verbs to
        validate_lawbook : bool, optional
            If True, the system law book is used to selectively apply only laws
            that have jurisdiction over the given agent

        '''
        for law_type in self.law:
            for phrase, law in self.law[law_type].items():
                
                if validate_lawbook:
                    if not phrase in self.lawbook[agent.agent_id_system]:
                        continue

                if law_type == 'compulsion':
                    self.compel(agent, phrase, validate_lawbook)
                elif law_type == 'mutation':
                    self.mutate(agent, phrase, validate_lawbook)

    def make_lawbook_entry(self, law_phrases, agent_name_selector=None, agent_ids=None):
        '''Enter a connection between agents as certain law phrases, such that
        the agent management system can enforce certain laws being applied to
        certain agents only

        Parameters
        ----------
        law_phrases : Iterable
            Collection of phrases, or names, of laws that have been added to
            the system
        agent_name_selector : callable, optional
            Function that receives an agent name and returns either True or
            False, where the former is interpreted as that the given law
            phrases apply to the corresponding set of agents of the system
        agent_ids : iterable, optional
            Collection of agent IDs, strings, for which the given law phrases
            apply. 

        Notes
        -----
        At least one of the `agent_name_selector` or `agent_ids` has to be
        given. 

        The method updates the law book, hence the method can be called
        multiple times in order to fully populate the law book. If an agent
        matches no law phrase, its entry is None.

        The law book is not required and is not enforced unless relevant
        methods, such as `compel` and `mutate`, are explicitly instructed to do
        so.

        '''
        for agent, aux in self:
            word = self.lawbook.setdefault(agent.agent_id_system, None)

            if not agent_name_selector is None:
                if agent_name_selector(agent.name):
                    word = law_phrases

            elif not agent_ids is None:
                if agent.agent_id_system in agent_ids:
                    word = law_phrases

            else:
                raise ValueError('One of agent_name_selector or agent_ids must be set')

            self.lawbook[agent.agent_id_system] = word

    def __len__(self):
        '''Return number of agents in the system'''

        return len(self.agents_in_scope)

    def __init__(self, name, agents, full_agents_graph=None,
                 common_env=None, strict_engine=False):

        self.name = name
        self.strict_engine = strict_engine

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

        self.common_env = common_env

        #
        # The agents are added to the system book keeping
        #
        self.agents_in_scope = OrderedDict()
        for agent in agents:
            self.bookkeep(agent)

        #
        # Initialize the look-up table for agent index and node. Provides
        # considerable speed up
        #
        self.node_from_agent_id_ = {}
        for node in self.agents_graph:
            if not node.agent_content is None:
                self.node_from_agent_id_[node.agent_content.agent_id_system] = node

        #
        # Initialize verbs for the Agent System
        #
        self.compulsion = {}
        self.mutation = {}
        self.law = {'compulsion' : self.compulsion,
                    'mutator' : self.mutation}
        self.lawbook = {}
