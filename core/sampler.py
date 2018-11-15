'''Sampler classes that extract some subset of system features for easy
digestion, analysis or writing to disk. The samplers include agent properties,
environment properties and system topological properties.

'''
import os
import pandas as pd
from pandas import DataFrame
from collections import Iterable

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
                 matcher=None, sample_steps=None):

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
    pass

class GraphSampler(object):
    pass

class SystemIO(object):
    '''Bla bla

    '''
    def stamp(self, system, generation, sampler, io_method, filename, io_method_kwargs={}):
        '''Bla bla

        '''
        df = sampler(system, generation)

        getattr(df, io_method)(filename, **io_method_kwargs)

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
                filename = rule['filename'][:self.injection_point] + \
                           str(generation) + \
                           rule['filename'][self.injection_point:]
                io_method = rule['io_method']
                io_method_kwargs = rule['io_method_kwargs']

                yield sampler, io_method, filename, io_method_kwargs

    def __init__(self, io_objects=[]):

        self.io_rules = []
        for io_obj in io_objects:
            rule = {}

            try:
                write_method = getattr(DataFrame, io_obj[1])
                rule['io_method'] = io_obj[1] 
            except AttributeError:
                raise AttributeError('IO object must use one of the IO ' + \
                                     'of Pandas DataFrame, not %s' %(io_obj[1]))

            rule['filename'] = io_obj[0] + io_obj[1].replace('to_', '.')
            rule['sampler'] = io_obj[2]
            
            self.injection_point = len(io_obj[0])

            if len(io_objects) == 4:
                rule['io_method_kwargs'] = io_obj[4]
            else:
                rule['io_method_kwargs'] = {}

            self.io_rules.append(rule)

