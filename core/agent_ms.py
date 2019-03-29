'''Agent Management System

'''
import numpy as np
import numpy.random
import networkx as nx
import itertools

from collections import OrderedDict, Iterable
from uuid import uuid4

from core.agent import Agent
from core.graph import Node
from core.instructor import Compulsion, Mutation
from core.sampler import AgentSampler, EnvSampler, GraphSampler, SystemIO

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
    common_env : optional
        In case all agents have a common environment, provide the corresponding
        object here
    strict_engine : bool, optional
        If False, any exceptions from engine execution of instructors are
        non-fatal to the execution. If True, engine exceptions terminates
        execution

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
        agents_hood : list 
            Agents (or Nodes) directly adjacent to the given agent

        '''
        node_with_agent = self.node_from_agent_id_[agent_index]
        node_neighbours = self.agents_graph.neighbors(node_with_agent)
        node_neighbours = list(node_neighbours)
        if agents_only:
            ret_neighbours = [x.agent_content for x in node_neighbours]

        else:
            ret_neighbours = node_neighbours

        return ret_neighbours

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

    def _shuffle_items(self, items, max_iter, replace):
        '''Shuffled iterator over agent graph items.

        Notes
        -----
        This method of iteration requires the graph to remain as within the
        iteration. Nodes can therefore not be added or removed inside the loop,
        nor can agents be added or removed from nodes. For cases like that use
        an iteration over some variant of `_choice_items`.

        Parameters
        ----------
        items : Iterable
            The container of graph items, such as Nodes or Agents
        max_iter : int
            The number of entries the iterator should yield before termination. 
            If set to None, the iteration is infinite. 
        replace : bool, optional
            If True, the iterator selects items randomly with replacement such
            that an uneven sampling of the items can be generated. If False,
            the iterator selects items in random order, but guaranteed to
            generate an even sampling of the items.

        Yields
        ------
        item
            One item of the input items, that is a Node or Agent

        '''
        def _terminator(counter):
            if max_iter is None:
                return True
            elif counter < max_iter:
                return True
            else:
                return False

        shuffled = []
        counter = 0
        while _terminator(counter): 
            counter += 1

            if len(shuffled) == 0:
                shuffled = list(np.array(items)[np.random.choice(len(items),
                                                                 size=len(items), 
                                                                 replace=replace)])
            entry = shuffled.pop(0)

            yield entry

    def _cycle_items(self, items, max_iter):
        '''Ordered iterator over agent graph items

        Notes
        -----
        This method of iteration requires the graph to remain as within the
        iteration. Nodes can therefore not be added or removed inside the loop,
        nor can agents be added or removed from nodes. For cases like that use
        an iteration over some variant of `_choice_items`.

        Parameters
        ----------
        items : Iterable
            The container of graph items, such as Nodes or Agents
        max_iter : int
            The number of entries the iterator should yield before termination. 
            If set to None, the iteration is infinite. 

        Yields
        ------
        item
            One item of the input items, that is a Node or Agent

        '''
        if max_iter is None:
            return itertools.cycle(items)
        
        else:
            for n, element in enumerate(itertools.cycle(items)):
                if n < max_iter:
                    yield element

                else:
                    break

    def _choice_items(self, items):
        '''Select random item from the agent graph items

        Parameters
        ----------
        items : Iterable
            The container of graph items, such as Nodes or Agents

        Returns
        -------
        items
            One random item of the input items, that is a Node or Agent

        '''
        return items[np.random.randint(len(items))]

    def _strip_node_agent(self, agents_only, subset):
        '''Retrieve node graph items

        Parameters
        ----------
        agents_only : bool
            If True, extract Agents from graph. If False, extract Nodes
        subset : Iterable
            A subset of the graph to extract items from. If None, entire graph

        Returns
        -------
        items
            Collection of agents or nodes from the graph

        '''
        if subset is None:
            items = list(self.agents_graph.nodes)

        else:
            items = list(subset)

        if agents_only:
            items = []
            for x in map(lambda x: x.agent_content, self.agents_graph.nodes):
                if not x is None:
                    items.append(x)

        return items

    def _strip_edge_agent(self, agents_only, subset):
        '''Retrieve edge graph items

        Parameters
        ----------
        agents_only : bool
            If True, extract Agent-Agent edge pairs from graph. If False,
            extract Node-Node edge pairs
        subset : Iterable
            A subset of the graph to extract items from. If None, entire graph

        Returns
        -------
        items
            Collection of agent-agent or node-node edge pairs from the graph

        '''
        if subset is None:
            items = list(self.agents_graph.edges)

        else:
            items = list(subset)

        if agents_only:
            items = []
            for x in map(lambda x: (x[0].agent_content, x[1].agent_content),
                         self.agents_graph.edges):
                if not None in x:
                    items.append(x)

        return items

    def shuffle_nodes(self, agents_only, max_iter, replace, subset=None):
        '''Shuffled iterator over agent graph nodes

        Notes
        -----
        This method of iteration requires the graph to remain as within the
        iteration. Nodes can therefore not be added or removed inside the loop,
        nor can agents be added or removed from nodes. For cases like that use
        an iteration over `choice_nodes`.

        Parameters
        ----------
        agents_only : bool
            If True, extract Agents from graph. If False, extract Nodes from
            graph
        max_iter : int
            The number of entries the iterator should yield before termination. 
            If set to None, the iteration is infinite. 
        replace : bool, optional
            If True, the iterator selects nodes randomly with replacement such
            that an uneven sampling of the nodes can be generated. If False,
            the iterator selects nodes in random order, but guaranteed to
            generate an even sampling of the nodes.
        subset : Iterable
            A subset of the graph to extract items from. If None, entire graph

        Yields
        ------
        item
            Node or Agent of graph 

        '''
        return self._shuffle_items(self._strip_node_agent(agents_only, subset), 
                                   max_iter, replace)

    def shuffle_edges(self, agents_only, max_iter, replace, subset=None):
        '''Shuffled iterator over agent graph edges 

        Notes
        -----
        This method of iteration requires the graph to remain as within the
        iteration. Nodes can therefore not be added or removed inside the loop,
        nor can agents be added or removed from nodes. For cases like that use
        an iteration over `choice_edges`.

        Parameters
        ----------
        agents_only : bool
            If True, extract Agent-Agent pairs connect by edge from graph. If 
            False, extract Node-Node pairs connected by edge from graph
        max_iter : int
            The number of entries the iterator should yield before termination. 
            If set to None, the iteration is infinite. 
        replace : bool, optional
            If True, the iterator selects edges randomly with replacement such
            that an uneven sampling of the edges can be generated. If False,
            the iterator selects edges in random order, but guaranteed to
            generate an even sampling of the edges..
        subset : Iterable
            A subset of the graph to extract items from. If None, entire graph

        Yields
        ------
        item1
            A first Node or Agent
        items2
            A second Node or Agent connected via an edge to the first Node or
            Agent

        '''
        return self._shuffle_items(self._strip_edge_agent(agents_only, subset), 
                                   max_iter, replace)

    def cycle_nodes(self, agents_only, max_iter, subset=None):
        '''Ordered iterator over agent graph nodes

        Notes
        -----
        This method of iteration requires the graph to remain as within the
        iteration. Nodes can therefore not be added or removed inside the loop,
        nor can agents be added or removed from nodes. For cases like that use
        an iteration over `choice_nodes`.

        Parameters
        ----------
        agents_only : bool
            If True, extract Agents from graph. If False, extract Nodes from
            graph
        max_iter : int
            The number of entries the iterator should yield before termination. 
            If set to None, the iteration is infinite. 
        subset : Iterable
            A subset of the graph to extract items from. If None, entire graph

        Yields
        ------
        item
            Node or Agent of graph 

        '''
        return self._cycle_items(self._strip_node_agent(agents_only, subset),
                                 max_iter)

    def cycle_edges(self, agents_only, max_iter, subset=None):
        '''Ordered iterator over agent graph edges

        Notes
        -----
        This method of iteration requires the graph to remain as within the
        iteration. Nodes can therefore not be added or removed inside the loop,
        nor can agents be added or removed from nodes. For cases like that use
        an iteration over `choice_edges`.

        Parameters
        ----------
        agents_only : bool
            If True, extract Agent-Agent pairs connect by edge from graph. If 
            False, extract Node-Node pairs connected by edge from graph
        max_iter : int
            The number of entries the iterator should yield before termination. 
            If set to None, the iteration is infinite. 
        subset : Iterable
            A subset of the graph to extract items from. If None, entire graph

        Yields
        ------
        item1
            A first Node or Agent
        items2
            A second Node or Agent connected via an edge to the first Node or
            Agent

        '''
        return self._cycle_items(self._strip_edge_agent(agents_only, subset),
                                 max_iter)

    def choice_nodes(self, agents_only, subset=None):
        '''Select one random item from graph nodes

        Parameters
        ----------
        agents_only : bool
            If True, extract Agents from graph. If False, extract Nodes from
            graph
        subset : Iterable
            A subset of the graph to extract items from. If None, entire graph

        Yields
        ------
        item
            Node or Agent of graph 

        '''
        return self._choice_items(self._strip_node_agent(agents_only, subset))

    def choice_edges(self, agents_only, subset=None):
        '''Select one random item from graph edges

        Parameters
        ----------
        agents_only : bool
            If True, extract Agent-Agent pairs connected by edge from graph. If 
            False, extract Node-Node pairs connected by edge from graph
        subset : Iterable
            A subset of the graph to extract items from. If None, entire graph

        Yields
        ------
        item1
            A first Node or Agent
        items2
            A second Node or Agent connected via an edge to the first Node or
            Agent

        '''
        return self._choice_items(self._strip_edge_agent(agents_only, subset))

    def __iter__(self):
        '''Iterator over all nodes and their content of the agent system.

        Notes
        -----
        Graphs can contain nodes that are not populated by an agent. This
        manifest itself as `agent_content` being `None`. The loop using the
        iterator should therefore handle these cases. Also note that if nodes
        are added or deleted to the graph inside a loop using the iterator,
        bad behaviour can be produced. If such graph operations are to be
        performed, `choice_nodes` can be used to pick nodes one by one keeping
        the container up-to-date.

        Yields
        ------
        nodes : Node
            Nodes of the agent graph in deterministic order

        '''
        return self.cycle_nodes(False, len(self.agents_graph))

    def get(self, key, get_node=False, get_agent=False, get_aux=False):
        '''Get a selection of objects associated with a given key

        Parameters
        ----------
        key : str
            Agent system ID
        get_node : bool, optional
            If True, node will be returned
        get_agent : bool, optional
            If True, agent will be returned
        get_aux : bool, optional
            If True, agent environment will be returned

        Returns
        -------
        objects : tuple
            Container of the selected objects. The size depends on how many
            parameters are True. The order of objects in the tuple is, node
            precede agent precede aux.

        '''
        ret = []

        node = self.node_from_agent_id_[key]
        if get_node:
            ret.append(node)

        if get_agent:
            ret.append(node.agent_content)

        if get_aux:
            ret.append(node.aux_content)

        if len(ret) == 1:
            ret_this = ret[0]

        else:
            ret_this = tuple(ret)

        return ret_this 

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

    def terminate_agent(self, key):
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

    def cleanse_inert(self):
        '''Cleanse inert agents from the system, where inertness is defined as
        an agent attribute that typically is set by some automatic terminal
        condition

        '''
        clear_list = []
        for node in self:
            if isinstance(node.agent_content, Agent):
                if node.agent_content.inert is True:
                    clear_list.append(node.agent_content.agent_id_system)

        for key in clear_list:
            self.terminate_agent(key)

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

    def set_sampler(self, sampler):
        '''Bla bla

        '''
        raise NotImplementedError('AMS Samplers not implemented yet')

    def set_samplers(self, *samplers):
        '''Add samplers for system

        Parameters
        ----------
        samplers
            Argument tuple of the samplers to add to the system.

        '''
        for sampler in samplers:
            self.set_sampler(sampler)

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

    def sample(self, generation=0):
        '''Bla bla

        '''
        pass

    def switch_node_content(self, node_1, node_2, 
                            switch_agent=True, switch_aux=True):
        '''Switch content of a pair of nodes

        Parameters
        ----------
        node_1 : Node
            The first node to operate on in the switch
        node_2 : Node
            The second node to operate on in the switch
        switch_agent : bool, optional
            If True, the agents of the pair of nodes should be interchanged. If
            a node does not contain an agent, instead the empty None, that
            empty space is interchanged. If False, the agents of the nodes are
            not interchanged.
        switch_aux : bool, optional
            If True, the local environments of the pair of nodes should be
            interchanged. If a node does not contain a local environment,
            instead the empty None, the empty spots are interchanged. If False,
            the local environments are left as is.

        '''
        if switch_agent:
            agent_1 = node_1.agent_content
            agent_2 = node_2.agent_content
            node_1.agent_content = agent_2
            node_2.agent_content = agent_1
            
            if not agent_1 is None:
                self.node_from_agent_id_[agent_1.agent_id_system] = node_2
            if not agent_2 is None:
                self.node_from_agent_id_[agent_2.agent_id_system] = node_1

        if switch_aux:
            aux_1 = node_1.aux_content
            aux_2 = node_2.aux_content
            node_1.aux_content = aux_2
            node_2.aux_content = aux_1

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

        agent.apply_map(the_compulsion.scaffold_map_output)

        return did_it_compel

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

        agent.apply_map(the_mutation.scaffold_map_output)

        return did_it_mutate

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
        ret = True
        for law_type in self.law:
            for phrase, law in self.law[law_type].items():
                
                if validate_lawbook:
                    if not phrase in self.lawbook[agent.agent_id_system]:
                        continue

                if law_type == 'compulsion':
                    ret_tmp = self.compel(agent, phrase, validate_lawbook)
                    ret = ret and ret_tmp
                elif law_type == 'mutation':
                    ret_tmp = self.mutate(agent, phrase, validate_lawbook)
                    ret = ret and ret_tmp

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
        for agent in self.cycle_nodes(True, len(self)):
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

    def get_n_nodes(self):
        '''Return number of nodes in agent graph'''

        return nx.number_of_nodes(self.agents_graph)

    def get_n_edges(self):
        '''Return number of edges in agent graph'''

        return nx.number_of_edges(self.agents_graph)

    def get_n_agents(self):
        '''Return number of agents in the system'''

        return len(self.agents_in_scope)

    def __len__(self):
        '''Return number of agents in the system'''

        return self.get_n_agents() 

    def __init__(self, name, agents, full_agents_graph=None,
                 agent_env=None, common_env=None, 
                 restartable=False, strict_engine=False):

        self.name = name
        self.strict_engine = strict_engine

        #
        # The agent to agent network relation is defined, which is a complete
        # graph in case nothing specific is given.
        #
        if full_agents_graph is None:
            if not agent_env is None:
                if (not isinstance(agent_env, Iterable)) or isinstance(agent_env, str):
                    agent_envs = [agent_env] * len(agents)

                else:
                    if len(agent_env) != len(agents):
                        raise ValueError('An iterable of agent environments ' + \
                                         'of wrong length %s' %(str(len(agent_env))))

                    agent_envs = agent_env

            else:
                agent_envs = [None] * len(agents)

            nodes = []
            for k, (agent, agent_env) in enumerate(zip(agents, agent_envs)):
                nodes.append(Node('agent_%s'%(str(k)), agent, agent_env))
            self.agents_graph = nx.complete_graph(nodes)

        #
        # If a network is given it is assumed to contain all objects, and hence
        # swapped directly into the graph attribute
        #
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
                    'mutation' : self.mutation}
        self.lawbook = {}

        #
        # Initialize system samplers
        #
        self.sampler = {}

        #
        # Initialize for restartable AMS
        #
        if restartable:
            raise NotImplementedError('Restartable AMS not implemented')
