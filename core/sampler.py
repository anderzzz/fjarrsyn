'''Bla bla

'''
import os
import pandas as pd
from pandas import DataFrame
from collections import Iterable

class AgentSampler(object):
    '''Bla bla

    '''
    def __call__(self, ams, generation=0):
        '''Bla bla

        '''
        rows = []
        for agent, aux in ams:

            is_there_match = True
            if not self.matcher is None:
                is_there_match = self.matcher(agent)

            if is_there_match:
                d_out = {self.indexer[0] : generation,
                         self.indexer[1] : agent.name,
                         self.indexer[2] : agent.agent_id_system}

                for imprint_type in ['resource', 'essence', 'belief']:

                    args = getattr(self, imprint_type + '_args')
                    if args is None:
                        continue

                    for array_name, arg_name in args:

                        if imprint_type == 'belief': 
                            imprint = agent.belief[array_name]

                        else:
                            imprint = getattr(agent, imprint_type)

                        for key, value in imprint.items():

                            if key == arg_name:
                                label = ':'.join([imprint_type, array_name, key])
                                d_out[label] = value

                df_row = pd.Series(d_out)
                rows.append(df_row)

        df = pd.DataFrame(rows)
        df = df.melt(id_vars=self.indexer)
        df = df.set_index(self.indexer + ['variable'])
        df = df.sort_values(self.indexer)

        return df

    def __init__(self, resource_args=None, essence_args=None, belief_args=None,
                 matcher=None, sample_steps=None, other_attributes=None):

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

        self.other_attr = other_attributes

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

class AgentSystemIO(object):
    '''Bla bla

    '''
    def flatten_scaffold(self, scaffold):
        '''Rename imprint data by merging scaffold and beliefs with their
        respective labels. Typical label can be `scaffold_money`.

        Parameters
        ----------
        imprint : dict
            The imprint of an agent

        Returns
        -------
        flat_imprint : dict
            The dictionary where keys have been flattened

        '''
        flat_imprint = {}
        for scaffold_type, scaffold_data in scaffold.items():
            for unit_name, unit_value in scaffold_data.items():
                key_union = scaffold_type + '_' + unit_name
                flat_scaffold[key_union] = unit_value

        return flat_scaffold

    def write_state_of_(self, system, write_count):
        '''Write the agent states of the system

        Parameters
        ----------
        system
            The agent management system

        '''
        for agent_id, agent in system.agents_in_scope.items(): 

            for imprint_label in ['resource', 'essence', 'belief']:

                data_dict = getattr(agent, imprint_label)

            if any([not v is None for v in agent.scaffold.values()]):
                data_dict = self.flatten_scaffold(agent.scaffold)

            else:
                data_dict = {}

            data_dict['agent_id'] = agent_id
            data_dict['generation_count'] = str(write_count)
            
            self.writer.writerow(data_dict)

    def flush(self):
        '''Bla bla

        '''
        self.file_handle.flush()

    def close(self):
        '''Bla bla

        '''
        self.file_handle.close()

    def __init__(self, file_name, file_format, resource_args=None,
                 essence_args=None, belief_args=None):

        fieldnames = ['agent_id'] + ['generation_count']

        if not resource_args is None:
            resource_fields = ['resource:' + arg_name for arg_name in resource_args]
            fieldnames += resource_fields
        self.resource_args = resource_args
                
        if not essence_args is None:
            essence_fields = ['essence:' + arg_name for arg_name in essence_args]
            fieldnames += essence_fields
        self.essence_args = essence_args
                
        if not belief_args is None:
            belief_fields = ['belief:' + arg_name for arg_name in belief_args]
            fieldnames += belief_fields
        self.belief_args = belief_args
                
        self.file_handle = open(file_name, 'w')
        if file_format == 'csv':
            self.writer = csv.DictWriter(self.file_handle,
                                         fieldnames=fieldnames,
                                         extrasaction='ignore')
            self.writer.writeheader()

        else:
            raise ValueError('Unknown agent system file format: %s' %(file_format))
