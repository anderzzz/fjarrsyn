'''Sampler classes that extract some subset of system features for easy
digestion, analysis or writing to disk. The samplers include agent properties,
environment properties and system topological properties.

'''
import os
import pandas as pd
from pandas import DataFrame
from collections import Iterable
import networkx as nx
import operator

class AgentSampler(object):
    '''Given an Agent Management System, the state of the agents are sampled in
    an easy to use data format.

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
    matcher : callable, optional
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

    Raises
    ------
    TypeError
        If the resource, essence or belief argument semantics is defined in
        other format than specified.
    TypeError
        If the matcher is not a callable

    '''
    def __call__(self, ams, generation=0):
        '''Perform a sampling of agents of a system

        Notes
        -----
        The sampling data is in the form of a pandas DataFrame. The Pandas
        library provides several methods to filter and reformat the data if
        desired. The sampled data is easily turned into a CSV file by invoking
        the method `.to_csv('output.csv')` to the DataFrame output.

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
            A stacked pandas DataFrame of sampled agent data. 

        '''
        #
        # Loop pver agents in system
        #
        rows = []
        for agent, aux in ams:

            is_there_match = True
            if not self.matcher is None:
                is_there_match = self.matcher(agent)

            #
            # If agent is supposed to be sampled, proceed here
            #
            if is_there_match:
                d_out = {self.indexer[0] : generation,
                         self.indexer[1] : agent.name,
                         self.indexer[2] : agent.agent_id_system}

                #
                # Loop over the imprint types of an Agent
                #
                for imprint_type in ['resource', 'essence', 'belief']:

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

                df_row = pd.Series(d_out)
                rows.append(df_row)

        #
        # 1. Create a DataFrame, pivotted, such that there is one row per agent
        # 2. Stack the data columns, such that there is one row per data entry
        # 3 & 4. Adjust labels and ordering of rows to be intuitive
        #
        df = pd.DataFrame(rows)
        df = df.melt(id_vars=self.indexer)
        df = df.set_index(self.indexer + ['variable'])
        df = df.sort_values(self.indexer)

        return df

    def __init__(self, resource_args=None, essence_args=None, belief_args=None,
                 matcher=None, sample_steps=1):

        self.indexer = ['generation', 'name', 'agent_index']

        for imprint_type in ['resource', 'essence', 'belief']:
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

        if not matcher is None:
            if not callable(matcher):
                raise TypeError('The matcher should be a callable')
            self.matcher = matcher
        else:
            self.matcher = lambda x: True

        self.sample_steps = sample_steps

class EnvSampler(object):
    '''Basic Environment sampler

    Bla BLA

    '''
    def __call__(self, ams, generation=0):
        '''Bla bla

        '''
        if not self.common_env is None:

            df = pd.DataFrame(self.sampler_func(ams.common_env),
                     index=pd.Index([generation], name='generation'))

        else:

            rows = []
            for agent, aux in ams:

                is_there_match = True
                if not self.matcher is None:
                    is_there_match = self.matcher(agent)

                if is_there_match:
                    d_out = {self.indexer[0] : generation,
                             self.indexer[1] : agent.name,
                             self.indexer[2] : agent.agent_id_system}

                    data_dict = self.sampler_func(aux)
                    d_out.update(data_dict)

                    df_row = pd.Series(d_out)
                    rows.append(df_row)

            df = pd.DataFrame(rows)
            df = df.melt(id_vars=self.indexer)
            df = df.set_index(self.indexer + ['variable'])
            df = df.sort_values(self.indexer)

        return df

    def __init__(self, sampler_func, 
                 common_env=None, 
                 agent_matcher=None, agent_data_index=['generation'],
                 sample_steps=1):

        self.sampler_func = sampler_func
        
        self.common_env = common_env
        self.indexer = ['generation', 'name', 'agent_index']

        if not agent_matcher is None:
            if not callable(agent_matcher):
                raise TypeError('The matcher should be a callable')
            self.matcher = agent_matcher

        else:
            self.matcher = lambda x: True
        self.agent_data_index = agent_data_index

        self.sample_steps = sample_steps

class GraphSampler(object):
    '''Bla bla

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

        network_agent_labels = nx.relabel_nodes(network, mapping)

        if nx.number_of_nodes(network_agent_labels) != nx.number_of_nodes(network):
            raise RuntimeError('After relabelling number of nodes changes. ' + \
                               'Likely an edge-case in the key functions')

        return network_agent_labels

    def __call__(self, ams, generation=0):
        '''Bla bla

        '''
        network_labels_only = self._make_labels_only(ams.agents_graph)
        
        return network_labels_only

    def __init__(self, 
                 key_occ_node='agent_id_system', 
                 key_unocc_node='unoccupied', 
                 report_empty_to_empty=True, sample_steps=1):

        if isinstance(key_occ_node, str):
            self.key_occ_ = lambda x: x.agent_content.agent_id_system

        elif callable(key_occ_node):
            self.key_occ_ = key_occ_node

        else:
            raise TypeError('The `key_occ_node` argument must be string or callable')

        if isinstance(key_unocc_node, str):
            self.key_unocc_ = lambda x: key_unocc_node

        elif callable(key_unocc_node):
            self.key_unocc_ = lambda x: getattr(x, key_unocc_node)

        else:
            raise TypeError('The `key_unocc_node` argument must be string or callable')

        self.report_empty_to_empty = report_empty_to_empty
        self.sample_steps = sample_steps

class SystemIO(object):
    '''Bla bla

    '''
    def stamp(self, system, generation, sampler, io_method, filename, io_method_kwargs={}):
        '''Bla bla

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
        '''Bla bla

        '''
        stamped_one = False
        for args in self._samplers_to_sample_at_(generation):
            self.stamp(system, generation, *args)
            stamped_one = True

        return stamped_one

    def _samplers_to_sample_at_(self, generation):
        '''Bla bla

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

    def set_write_rule(self, name, method_key, sampler, method_kwargs={}):
        '''Bla bla

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
