'''Sampler classes that extract some subset of system features for easy
digestion, analysis or writing to disk. The samplers include agent properties,
environment properties and system topological properties.

'''
from pandas import DataFrame, Series, Index
from collections import Iterable
import networkx as nx
import operator

from core.constants import AGENT_IMPRINTS

class AgentSampler(object):
    '''Given an Agent Management System, the state of the agents are sampled in
    an easy to use data format.

    Parameters
    ----------
    resource_args : list or tuple, optional
        If provided, the container should include semantic elements, which
        define one resource of the agent that should be sampled. The format of 
        each semantic element is as defined in the Notes. 
    essence_args : list or tuple, optional
        If provided, the container should include semantic elements, which
        define one essence of the agent that should be sampled. The format of 
        each semantic element is as defined in the Notes. 
    belief_args : list or tuple, optional
        If provided, the container should include semantic elements, which
        define one belief of the agent that should be sampled. The format of 
        each semantic element is as defined in the Notes. 
    agent_matcher : callable, optional
        If provided, the callable takes one input, an Agent, and based on some
        of its attributes should compute a boolean return. If the returned
        boolean is True, this agent is to be sampled, if False, the agent
        should not be sampled. This is typically used if the system contains
        qualitatively very different agents, which should be sampled in
        separate ways. A convenient way is to match based on agent name. If not
        provided, all agents are sampled.
    sample_steps : int, optional
        Integer that instructs a simulator or IO class at what multiples of
        simulated steps to execute the Agent Sampler.

    Notes
    -----
    The Agent Sampler is typically used in conjunction with the System IO class
    wherein the data from the Agent Sampler is written to disk by the System IO
    instance. 

    The format of the semantic elements of the containers for `resource_args`,
    `essence_args` and `belief_args` is a two-membered tuple with semantic
    content as follows:

    (<imprint name>, <imprint semantic element>)

    For a belief defined as `Belief('Time', ('Season','Time of Day'))` the
    semantic elements can be ('Time', 'Season') or ('Time', 'Time of Day')

    Raises
    ------
    TypeError
        If the resource, essence or belief argument semantics is defined in
        other format than specified.
    TypeError
        If the matcher is not a callable

    '''
    def sample_one(self, agent, generation=0):
        '''Perform a sampling of specific agent

        Parameters
        ----------
        agent : Agent
            The agent to sample with the AgentSampler
        generation : int, optional
            If the sampling is part of a simulation, this parameter enables to
            provide the current generation or iteration of the sampling, such
            that this value becomes included as meta data in the sampling
            output

        Returns
        -------
        d_row : Series
            Pandas Series with sampled data, index being the type of data,
            value the data. The content of the Series is mostly specified in the
            initilization of the class instance. Exception is three entries
            that specifies the agent identity (name and agent system ID) and
            sample time (generation)

        '''
        #
        # If agent does not match criteria, return empty
        #
        if not self.matcher(agent):
            return None 

        d_out = {self.indexer[0] : generation,
                 self.indexer[1] : agent.name,
                 self.indexer[2] : agent.agent_id_system}

        #
        # Loop over the imprint types of an Agent
        #
        for imprint_type in AGENT_IMPRINTS:

            args = getattr(self, imprint_type + '_args')
            if args is None:
                continue

            #
            # Loop over imprint names and arguments
            #
            for array_name, arg_name in args:

                if imprint_type == 'belief': 
                    imprint = agent.belief[array_name]

                else:
                    imprint = getattr(agent, imprint_type)

                for key, value in imprint.items():

                    #
                    # If a match on all counts, construct the compact
                    # label and retrieve the corresponding value
                    #
                    if key == arg_name:
                        label = ':'.join([imprint_type, array_name, key])
                        d_out[label] = value

        return Series(d_out)

    def sample_many(self, ams, generation=0):
        '''Perform a sampling of agents of a system

        Parameters
        ----------
        ams : AgentManagementSystem
            An agent management system populated with Agents, not necessarily
            identical ones
        generation : int, optional
            If the sampling is part of a simulation, this parameter enables to
            provide the current generation or iteration of the sampling, such
            that this value becomes included as meta data in the sampling
            output

        Returns
        -------
        rows : list
            List of Pandas Series, each element in the list corresponds to an
            Agent, each Series contains data as specified in the sampler
            initialization, see ``sample_one`` for details.

        '''
        rows = []
        for node in ams:
            agent = node.agent_content

            if self.matcher(agent):
                
                df_row = self.sample_one(agent, generation)
                rows.append(df_row)

        return rows

    def __call__(self, x_obj, generation=0):
        '''Dynamic sampling of object by the AgentSampler class. The object
        that is sampled can be a single Agent or a system of Agents contained
        in an AgentManagementSYstem

        Parameters
        ----------
        x_obj
            An instance of either Agent or AgentManagementSystem from which to
            sample specified agent data
        generation : int, optional
            If the sampling is part of a simulation, this parameter enables to
            provide the current generation or iteration of the sampling, such
            that this value becomes included as meta data in the sampling
            output

        Returns
        -------
        df : Pandas DataFrame
            A stacked pandas DataFrame of sampled agent data. 

        Notes
        -----
        The sampling data is in the form of a pandas DataFrame. The Pandas
        library provides several methods to filter and reformat the data if
        desired. The sampled data is easily turned into a CSV file by invoking
        the method `.to_csv('output.csv')` to the DataFrame output.

        '''
        #
        # Agent cannot be iterated over, AgentManagementSystem can
        #
        if not hasattr(x_obj, '__iter__'):
            data = [self.sample_one(x_obj, generation)]

        else: 
            data = self.sample_many(x_obj, generation)

        #
        # 1. Create a DataFrame, pivotted, such that there is one row per agent
        # 2. Stack the data columns, such that there is one row per data entry
        # 3 & 4. Adjust labels and ordering of rows to be intuitive
        #
        df = DataFrame(data)
        df = df.melt(id_vars=self.indexer)
        df = df.set_index(self.indexer + ['variable'])
        df = df.sort_values(self.indexer)

        return df

    def __init__(self, name, 
                 resource_args=None, essence_args=None, belief_args=None,
                 agent_matcher=None, sample_steps=1):

        self.name = name
        self.indexer = ['generation', 'name', 'agent_index']

        for imprint_type in AGENT_IMPRINTS: 
            args = locals()[imprint_type + '_args']
            if not args is None:
                args_ok = False
                if isinstance(args, Iterable):
                    if all([len(x) == 2 for x in args]):
                        args_ok = True

                if not args_ok:
                    raise TypeError('Value to `%s_args` should be an ' %(imprint_type)+ \
                                    'iterable of two-membered tuples/lists ' + \
                                    'each element referring to one %s' %(imprint_type))

        self.resource_args = resource_args
        self.essence_args = essence_args
        self.belief_args = belief_args

        if not agent_matcher is None:
            if not callable(agent_matcher):
                raise TypeError('The agent_matcher should be a callable')
            self.matcher = agent_matcher
        else:
            self.matcher = lambda x: False if x is None else True 

        self.sample_steps = sample_steps

class EnvSampler(object):
    '''Given an Agent Management System, the state of the environment is
    sampled in an easy to use data format.

    Parameters
    ----------
    sampler_func : callable
        Function that given an instance of an environment class, however
        defined, returns a dictionary. Each entry in the dictionary extracts an
        attribute, or other property of the environment instance, and
        associates it with a string key that will be used in the data format of
        the sample.
    common_env : bool, optional
        If the sampler is of a common environment of the Agent Management
        System, set this argument to True, while if the sampler is of local
        agent environments, the argument should be set to False.
    agent_matcher : callable, optional
        If provided, the callable takes one input, an Agent, and based on some
        of its attributes should compute a boolean return. If the returned
        boolean is True, the local environment of this 
        agent is to be sampled, if False, the local environment of this agent
        should not be sampled. This is typically used if the system contains
        qualitatively very different agents, which should be sampled in
        separate ways. A convenient way is to match based on agent name. If not
        provided, all agents are sampled.
    sample_steps : int, optional
        Integer that instructs a simulator or IO class at what multiples of
        simulated steps to execute the Agent Sampler.
    
    Raises
    ------
    TypeError
        If the agent_matcher is not callable

    '''
    def sample(self, agent, generation=0):
        '''Bla bla

        '''

    def __call__(self, ams, generation=0):
        '''Perform a sampling of environment of a system

        Parameters
        ----------
        ams : AgentManagementSystem
            An agent management system populated with Agents, not necessarily
            identical ones
        generation : int, optional
            If the sampling is part of a simulation, this parameter enables to
            provide the current generation or iteration of the sampling, such
            that this value becomes included as meta data in the sampling
            output

        Returns
        -------
        df : Pandas DataFrame
            A stacked pandas DataFrame of sampled environment data. 

        Notes
        -----
        The sampling data is in the form of a pandas DataFrame. The Pandas
        library provides several methods to filter and reformat the data if
        desired. The sampled data is easily turned into a CSV file by invoking
        the method `.to_csv('output.csv')` to the DataFrame output.

        The construction of the environment class object is relatively 
        unconstrained, therefore the environment sampler relies on a
        user-defined sampler function that extracts the relevant data in a
        format required.

        '''
        #
        # If the sampling is done of a common environment, the data is
        # comprised of a single row indexed on generation only
        #
        if self.common_env:
            df = DataFrame(self.sampler_func(ams.common_env),
                     index=Index([generation], name='generation'))

        #
        # If the sampling is done of local environments to a subset of agents
        # of the system.
        #
        else:
            rows = []
            for node in ams:
                agent = node.agent_content
                aux = node.aux_content

                if self.matcher(agent): 
                    d_out = {self.indexer[0] : generation,
                             self.indexer[1] : agent.name,
                             self.indexer[2] : agent.agent_id_system}

                    data_dict = self.sampler_func(aux)
                    d_out.update(data_dict)

                    df_row = Series(d_out)
                    rows.append(df_row)

            #
            # 1. Create a DataFrame, pivotted, such that there is one row per agent
            # 2. Stack the data columns, such that there is one row per data entry
            # 3 & 4. Adjust labels and ordering of rows to be intuitive
            #
            df = DataFrame(rows)
            df = df.melt(id_vars=self.indexer)
            df = df.set_index(self.indexer + ['variable'])
            df = df.sort_values(self.indexer)

        return df

    def __init__(self, name, sampler_func, 
                 common_env=False, agent_matcher=None, 
                 sample_steps=1):

        self.name = name
        self.sampler_func = sampler_func
        
        self.common_env = common_env
        self.indexer = ['generation', 'name', 'agent_index']

        if not agent_matcher is None:
            if not callable(agent_matcher):
                raise TypeError('The matcher should be a callable')
            self.matcher = agent_matcher

        else:
            self.matcher = lambda x: False if x is None else True

        self.sample_steps = sample_steps

class GraphSampler(object):
    '''Perform a sampling of the agent systems network

    Parameters
    ----------
    key_occ_node : callable, optional
        If a callable, the function takes a Node object as input, the Node
        object containing an agent object, and returns a string key. Typically
        the agent name or agent ID is returned. If not set, the label
        substitution defaults to the agent ID.
    key_unocc_node : callable, optional
        If a callable, the function takes a Node object as input, the Node
        object being without an agent object, and returns a string key. 
        Typically this is a constant string, or some node attribute. If not 
        set, the label substitution defaults to string `unoccupied`.
    report_empty_to_empty : bool, optional
        If True, the entire graph is sampled, including edges between nodes
        that contain no Agent. If False, only the part of the graph with edges
        comprised of at least one node containing an Agent is sampled.
    sample_steps : int, optional
        Integer that instructs a simulator or IO class at what multiples of
        simulated steps to execute the Agent Sampler.
        
    Notes
    -----
    The graph sampling operates by replicating the network topology of the
    agent system, and by substituting the agent objects with labels for easy
    interpretation and cross-referencing. The mapping from agent object to
    label is defined during initialization.

    '''
    def _make_labels_only(self, network):
        '''Create a new network of identical topology, but with the nodes
        swapped for the agent label. This is needed to create a representation
        that can be serialized as a string

        Parameters
        ----------
        network 
            The reference network, from `networkx` library

        Returns
        -------
        network_agent_labels
            The new network with the label substitution, all else the same as
            the input network

        Raises
        ------
        RuntimeError
            If the number of nodes changes after re-labelling. This is caused
            by non-unique node labels. The method attempts to make labels
            unique, but in some edge-cases that include labels that end on
            `_<integer>`, this routine can conceivably fail.

        '''
        mapping = {}
        for node in network:

            if not node.agent_content is None:
                mapping[node] = self.key_occ_(node)

            else:
                mapping[node] = self.key_unocc_(node)

        #
        # In the event that node labels are identical, they are uniquified in a
        # predictable manner.
        #
        if len(set(mapping.values())) < nx.number_of_nodes(network):

            value_values = set(mapping.values())
            v_map = {}
            for v in value_values:
                n_vals = list(mapping.values()).count(v)
                if n_vals > 1:
                    v_unique = [v + '_%s'%(str(k)) for k in range(n_vals)]
                    v_map[v] = v_unique
                else:
                    v_map[v] = [v]

            mapping_unique = {}
            for key, value in mapping.items():
                mapping_unique[key] = v_map[value].pop(0)
            mapping = mapping_unique

        #
        # The relabelling
        #
        network_agent_labels = nx.relabel_nodes(network, mapping)

        if nx.number_of_nodes(network_agent_labels) != nx.number_of_nodes(network):
            raise RuntimeError('After relabelling number of nodes changes. ' + \
                               'Likely an edge-case in the key functions')

        return network_agent_labels

    def __call__(self, ams, generation=0):
        '''Perform a sampling of the system graph

        Parameters
        ----------
        ams : AgentManagementSystem
            An agent management system populated with Agents, not necessarily
            identical ones
        generation : int, optional
            If the sampling is part of a simulation, this parameter enables to
            provide the current generation or iteration of the sampling, such
            that this value becomes included as meta data in the sampling
            output

        Returns
        -------
        network_labels_only : networkx Graph
            A Graph object from the networkx library where all nodes have been
            substituted for unique string labels for easy writing

        Notes
        -----
        The sampling data is in the form of a networkx Graph. The networkx
        library provides several methods to analyze and reformat the data if
        desired. The sampled data is easily turned into a standardized network
        file by passing the return object to `networkx.readwrite.gexf.write_gexf` 
        for example.

        '''
        if not self.report_empty_to_empty:
            remove_set = []
            for node_1, node_2 in ams.agents_graph.edges:
                if node_1.agent_content is None and \
                   node_2.agent_content is None:
                    remove_set.append((node_1, node_2))

            graph_transform = ams.agents_graph.copy()
            graph_transform.remove_edges_from(remove_set)

        else:
            graph_transform = ams.agents_graph.copy()

        network_labels_only = self._make_labels_only(graph_transform)

        return network_labels_only

    def __init__(self, name,
                 key_occ_node=None,
                 key_unocc_node=None,
                 report_empty_to_empty=True, sample_steps=1):

        self.name = name

        if key_occ_node is None:
            self.key_occ_ = lambda x: x.agent_content.agent_id_system

        elif callable(key_occ_node):
            self.key_occ_ = key_occ_node

        else:
            raise TypeError('The `key_occ_node` argument must be string or callable')

        if key_unocc_node is None:
            self.key_unocc_ = lambda x: 'unoccupied'

        elif callable(key_unocc_node):
            self.key_unocc_ = lambda x: getattr(x, key_unocc_node)

        else:
            raise TypeError('The `key_unocc_node` argument must be string or callable')

        self.report_empty_to_empty = report_empty_to_empty
        self.sample_steps = sample_steps

class SystemIO(object):
    '''Write sampled data of the Agent System to disk by some control logic

    Parameters
    ----------
    io_objects : list, optional
        A list of io_objects. The io_objects are tuples that are passed as
        arguments to the class method `set_write_rule`. Therefore, the current
        input parameter is optional and is equivalent to a sequence of calls to
        said class method

    '''
    def stamp(self, system, generation, sampler, io_method, filename, io_method_kwargs={}):
        '''Perform the output operation to disk. The preferred public method is
        `try_stamp` preceeded by a set of write rules through `set_write_rule`.

        Parameters
        ----------
        system : AgentManagementSystem
            Agent system under study
        generation : int
            The generation or iteration of a simulation, or an arbitrary index
            in other contexts
        sampler : AgentSampler, EnvSampler or GraphSampler
            A sampler class instance that retrieves the data to write, as well
            as defines the frequency at which to sample and write the data
        method_key : str
            The library method to convert a sampled piece of data into a file
            of desired format. For agent and environment sampling, the
            available methods are all IO methods of a Pandas library DataFrame.
            For graph sampling, the available methods are all IO methods of a 
            networkx library Graph. See documentation for `set_write_rule` for
            further details.
        filename : str
            Full filename or path to write data to
        io_method_kwargs : dict, optional
            Named arguments to the method implied by the `method_key`

        Raises
        ------
        TypeError
            If unknown sampler type provided

        '''
        if isinstance(sampler, (AgentSampler, EnvSampler)):
            df = sampler(system, generation)
            getattr(df, io_method)(filename, **io_method_kwargs)

        elif isinstance(sampler, GraphSampler):
            network_strings_only = sampler(system, generation)
            io_func = operator.attrgetter(io_method)(nx.readwrite)
            io_func(network_strings_only, filename, **io_method_kwargs)

        else:
            TypeError('Unknown sampler type %s' %(str(type(sampler))))

    def try_stamp(self, system, generation):
        '''Attempt to stamp data onto disk. This is the preferred public method
        in a simulation context, since only if a multiple of the sampler
        frequency is provided does this method become an actual output
        operation

        Parameters
        ----------
        system : AgentManagementSystem
            Agent system under study
        generation : int
            The generation or iteration of a simulation against which a
            sampling frequency is compared

        Returns
        -------
        stamped_one : bool
            True if an output operation took place, False otherwise

        '''
        stamped_one = False
        for args in self._samplers_to_sample_at_(generation):
            self.stamp(system, generation, *args)
            stamped_one = True

        return stamped_one

    def _samplers_to_sample_at_(self, generation):
        '''Iterator over write rules given a generation index. If the
        generation is not a multiple of the sampling frequency set in any of
        the system samplers, the iterator yield is empty.

        Parameters
        ----------
        generation : int
            The generation or iteration of a simulation against which a
            sampling frequency is compared

        Returns
        -------
        sampler : AgentSampler, EnvSampler or GraphSampler
            A sampler class instance to retrieve data sample,
        io_method : str
            The library method to convert a sampled piece of data into a file
            of desired format. See documentation for `set_write_rule` for
            further details.
        filename : str
            Full filename or path to write data to
        io_method_kwargs : dict, optional
            Named arguments to the method implied by the `method_key`

        '''
        for rule in self.io_rules:
            sampler = rule['sampler']
            if generation % sampler.sample_steps == 0:
                injection_point = rule['injection_point']
                filename = rule['filename'][:injection_point] + \
                           str(generation) + \
                           rule['filename'][injection_point:]
                io_method = rule['io_method']
                io_method_kwargs = rule['io_method_kwargs']

                yield sampler, io_method, filename, io_method_kwargs

    def set_write_rule(self, name, sampler, method_key, method_kwargs={}):
        '''Define a write rule, that is how to acquire data from the an agent
        system, and where to write it.

        Parameters
        ----------
        name : str
            The file name prefix to which data is written
        sampler : AgentSampler, EnvSampler or GraphSampler
            A sampler class instance that retrieves the data to write, as well
            as defines the frequency at which to sample and write the data
        method_key : str
            The library method to convert a sampled piece of data into a file
            of desired format. For agent and environment sampling, the
            available methods are all IO methods of a Pandas library DataFrame.
            A partial list is provided in the Notes. For graph sampling, the
            available methods are all IO methods of a networkx library Graph. A
            partial list is provided in the Notes.
        method_kwargs : dict, optional
            Any named arguments to pass to the library IO method invoked.

        Raises
        ------
        AttributeError
            If an unknown `method_key` is provided
        TypeError
            If an unknown sampler type is provided

        Notes
        -----
        The complete list of available IO methods can be found in the Pandas
        and networkx library documentation. The following is a list of the most
        common formats

        `to_csv` : From Pandas, write in CSV format
        `to_json` : From Pandas, write in JSON format
        `to_pickle` : From Pandas, pickle the DataFrame
        `to_sql` : From Pandas, write to SQL database
        `edgelist.write_edgelist` : From networkx, write edge list as text file
        `gexf.write_gexf` : From networkx, write in GEXF format
        `gml.write_gml` : From networkx, write in GML format
        `gpickle.write_gpickle` : From networkz, pickle the network

        '''
        rule = {}

        if isinstance(sampler, (AgentSampler, EnvSampler)):

            try:
                write_method = getattr(DataFrame, method_key)
                rule['io_method'] = method_key
            except AttributeError:
                raise AttributeError('IO object must use one of the IO ' + \
                                     'of Pandas DataFrame, not %s' %(method_key))
            rule['filename'] = name + method_key.replace('to_', '.')
            rule['injection_point'] = len(name)

        elif isinstance(sampler, GraphSampler):
            
            try:
                write_method = operator.attrgetter(method_key)(nx.readwrite)
                rule['io_method'] = method_key
            except AttributeError:
                raise AttributeError('IO object must use one of the IO ' + \
                                     'of networkx, not %s' %(method_key))

            rule['filename'] = name + '.' + method_key.split('.')[0]
            rule['injection_point'] = len(name)

        else:
            raise TypeError('The sampler should be instance of one of ' + \
                            'the library samplers')

        rule['sampler'] = sampler
        rule['io_method_kwargs'] = method_kwargs
        
        self.io_rules.append(rule)

    def __init__(self, io_objects=[]):

        self.io_rules = []

        for io_obj in io_objects:
            self.set_write_rule(*io_obj)
