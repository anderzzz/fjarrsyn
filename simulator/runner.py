'''Classes to run a simulation of an agent system along with a propagator of
the system. The classes contain standard sampling methods.

'''
from core.agent_ms import AgentManagementSystem
from writeread.graph_io import GraphIO
from writeread.agent_io import AgentSystemIO

class FiniteSystemRunner(object):
    '''Class to create an object that runs a simulation of an agent system
    using a system specific propagator. The class handles sampling of data at
    a set interval, including agent state and agent graph relations. The
    simulation involves a finite number of steps

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
    sample_file_format : str, optional
        File format of file that samples the agent system state
    imprints_sample : list, optional
        List of strings that specify a subset of imprints of agent to sample.
        The format is `<imprint_type>_<label>`, for example, `scaffold_money`
        or `belief_friendly`.
    graph_file_name_body : str, optional
        Body of the file name to which agent graph connection data is written
        during sampling. If not specified, no graph data is sampled. Note that
        suffixes denoting file format and sampling iteration are added to the 
        files written to disk
    graph_file_format : str, optional
        File format to use for the file with sampled graph data
    system_propagator : callable
        A callable object, such as a function or class instance, that specifies
        how the agent system is propagated
    system_propagator_kwargs : dict, optional
        Named argument dictionary to the `system_propagator`

    '''
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
        def _sample():
            '''Print sampling data to disk

            '''
            print ('SAMPLE')
            #
            # Sample state of agent system
            #
            self.sampler.write_state_of_(system, self.write_count)
            self.sampler.flush()

            #
            # If requested, sample agent graph
            #
            if not self.grapher is None:
                self.grapher.write_graph_state(system.agents_graph, 
                                               self.write_count)

        if not isinstance(system, AgentManagementSystem):
            raise TypeError('The system runner can only handle a an object ' + \
                            'that inherets AgentManagementSystem')

        #
        # Outermost loop for simulation
        #
        for k_iter in range(self.n_iter):

            self.propagate_(system, **self.propagate_kwargs)

            if self.time_to_sample(k_iter):
                _sample()
                self.write_count += 1

        #
        # After simulation, take one last sample
        #
        if self.time_to_sample(0):
            _sample()

    def __init__(self, n_iter, 
                 n_sample_steps=-1, 
                 sample_file_name='sample.csv', sample_file_format='csv',
                 imprints_sample=[], 
                 graph_file_name_body=None, graph_file_format='json',
                 system_propagator=None, system_propagator_kwargs={}):

        #
        # The step data of simulation and sampling
        #
        self.n_iter = n_iter
        self.n_sample_steps = n_sample_steps

        #
        # If sampling has been requested, initialize relevant IO classes
        #
        if not self.n_sample_steps < 0:
            self.write_count = 0
            self.sampler = AgentSystemIO(sample_file_name, 
                                         sample_file_format,
                                         imprints_sample)

            if not graph_file_name_body is None:
                self.grapher = GraphIO(graph_file_name_body,
                                       graph_file_format)
            else:
                self.grapher = None

        #
        # Check the system propagator 
        #
        if system_propagator is None:
            raise TypeError("The system_propagator is not defined")

        self.propagate_ = system_propagator
        self.propagate_kwargs = system_propagator_kwargs
