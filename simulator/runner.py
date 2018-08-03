'''Classes to run a simulation of an agent system along with a propagator of
the system. The classes contain standard sampling methods.

'''
import csv
import pandas as pd

from core.agent_ms import AgentManagementSystem

class FiniteSystemRunner(object):
    '''Class to create an object that runs a simulation of an agent system
    using a system specific propagator. The class handles sampling of data at
    a set interval, including agent state and agent graph relations.

    Parameters
    ----------
    n_iter : int
        Total number of iterations to simulate. Each iteration implies one
        propagation, which means if the propagator includes multiple agent
        operations, more than `n_iter` agent operations are executed
    n_sample_steps : int, optional
        How many iterations between sampling the state of the system. If set to
        a negative number, no sampling is done
    sample_file_name : str, optional
        File name to write agent state data to during sampling
    imprints_sample : list, optional
        List of strings that specify a subset of imprints of agent to sample.
        The format is `<imprint_type>_<label>`, for example, `scaffold_money`
        or `belief_friendly`.
    graph_file_name : str, optional
        File name to write agent graph connection data to during sampling. If
        not specified, no graph data is sampled.
    system_propagator : callable
        A callable object, such as a function or class instance, that specifies
        how the agent system is propagated
    system_propagator_kwargs : dict, optional
        Named argument dictionary to the `system_propagator`

    '''
    def flatten_imprint(self, imprint):
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
        for imprint_type, imprint_data in imprint.items():
            for unit_name, unit_value in imprint_data.items():
                key_union = imprint_type + '_' + unit_name
                flat_imprint[key_union] = unit_value

        return flat_imprint

    def write_state_of_(self, system):
        '''Write the agent states of the system

        Parameters
        ----------
        system
            The agent management system

        '''
        for agent_id, agent in system.agents_in_scope.items(): 
            data_dict = self.flatten_imprint(agent.imprint)
            data_dict['agent_id'] = agent_id
            data_dict['write_count'] = str(self.write_count)
            
            self.writer.writerow(data_dict)

    def write_graph_state_of_(self, system):
        '''Write agent adjacencies of the system graph

        Parameters
        ----------
        system 
            The agent management system

        '''
        adjacency_data = system.agents_graph.get_adjacency_list()

        agents1 = []
        agents2 = []
        for index, row in adjacency_data.iteritems():
            agent_ind = (not row[0].agent_content is None, 
                         not row[1].agent_content is None)

            if all(agent_ind):
                agents1.append(row[0].agent_content.agent_id_system)
                agents2.append(row[1].agent_content.agent_id_system)

            elif agent_ind[0]:
                agents1.append(row[0].agent_content.agent_id_system)
                agents2.append(None)

            elif agent_ind[1]:
                agents1.append(None)
                agents2.append(row[1].agent_content.agent_id_system)

        df = pd.DataFrame({'agent_1':agents1, 'agent_2':agents2,
                           'write_count': str(self.write_count)})
        df.to_csv(self.graph_handle, header=False, index=False, mode='a')

    def time_to_sample(self, k_iter):
        '''Test if this iteration should be sampled

        Parameters
        ----------
        k_iter : int
            The iteration counter

        Returns
        -------
        sample : bool
            If True the iteration should be sampled as set by the sample
            parameters in the initialization

        '''
        if self.n_sample_steps < 0:
            return False
        else:
            return (k_iter % self.n_sample_steps) == 0

    def __call__(self, system):
        '''The outer loop for a finite step simulation of a system, each step a
        system propagator is applied

        Parameters
        ----------
        system : AgentManagementSystem
            The system to simulate

        Raises
        ------
        TypeError
            If the input object is not an agent management system

        '''
        if not isinstance(system, AgentManagementSystem):
            raise TypeError('The system runner can only handle a an object ' + \
                            'that inherets AgentManagementSystem')

        for k_iter in range(self.n_iter):

            self.propagate_(system, **self.propagate_kwargs)

            if self.time_to_sample(k_iter):
                self.write_state_of_(system)
                self.file_handle.flush()

                if not self.graph_file_name is None:
                    self.write_graph_state_of_(system)
                    self.graph_handle.flush()

                self.write_count += 1

    def __init__(self, n_iter, 
                 n_sample_steps=-1, sample_file_name='sample.csv',
                 imprints_sample=[], 
                 graph_file_name=None, 
                 system_propagator=None, system_propagator_kwargs={}):

        self.n_iter = n_iter
        self.n_sample_steps = n_sample_steps

        self.sample_file_name = sample_file_name
        self.graph_file_name = graph_file_name
        self.write_count = 0
        if not self.n_sample_steps < 0:
            self.file_handle = open(self.sample_file_name, 'w')
            fieldnames = ['agent_id'] + ['write_count'] + imprints_sample
            self.writer = csv.DictWriter(self.file_handle, 
                                         fieldnames=fieldnames,
                                         extrasaction='ignore')
            self.writer.writeheader()

            if not self.graph_file_name is None:
                self.graph_handle = open(self.graph_file_name, 'w')
                self.graph_handle.write('agent_1,agent_2,write_count\n')

        if system_propagator is None:
            raise TypeError("The system_propagator is not defined")

        self.propagate_ = system_propagator
        self.propagate_kwargs = system_propagator_kwargs
