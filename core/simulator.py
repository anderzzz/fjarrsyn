'''Classes to run a simulation of an agent system along with a propagator of
the system. The classes contain standard sampling methods.

'''
from core.agent_ms import AgentManagementSystem

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
            raise TypeError('Simulation is done only of instance of ' + \
                            'Agent Management System')

        for k_iter in range(self.n_iter):

            self.propagate_(system, **self.propagate_kwargs)
            self.io.try_stamp(system, k_iter)

            if not self.progress_report_step is None:
                if k_iter % self.progress_report_step == 0:
                    print (self.print_progress(k_iter))

    def __init__(self, n_iter, system_propagator, 
                 system_io=None, progress_report_step=None,
                 system_propagator_kwargs={}):

        #
        # The step data of simulation and sampling
        #
        self.n_iter = n_iter

        if not progress_report_step is None:
            self.print_progress = lambda x: '---> ' + str(x) + 'steps of total ' + \
                str(self.n_iter) + ' have been executed'
        self.progress_report_step = progress_report_step

        #
        # Check the system propagator 
        #
        if system_propagator is None:
            raise TypeError("The system_propagator is not defined")

        self.propagate_ = system_propagator
        self.propagate_kwargs = system_propagator_kwargs

        if not system_io is None:
            self.io = system_io

        else:
            self.io.try_stamp = lambda x, y: None 
