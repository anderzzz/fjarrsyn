'''Classes to run a simulation of an agent system along with a propagator of
the system. 

'''
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.mover import Mover

class _Simulator(object):
    '''Parent class to simulators

    Parameters
    ----------
    system_mover : Mover
        The callable Mover of the AMS that implements the system dynamics
    system_io : SystemIO, optional
        An instance of the SystemIO class that defines what system data to
        sample and how to write it to disk

    '''
    def step(self, system):
        '''Take on step forward of the system as defined by the system
        mover, and if appropriate, sample system data and write to disk

        Parameters
        ----------
        system : AgentManagementSystem
            The system to simulate

        '''
        self.move_(system)
        if not self.io is None:
            self.io.try_stamp(system, self.step_count)

        self.step_count += 1

    def __init__(self, system_mover, system_io=None, step_offset=0):

        if not isinstance(system_mover, Mover):
            raise TypeError("The system mover is of wrong type:%s" %(str(type(system_mover))))

        self.move_ = system_mover
        self.io = system_io

        self.step_count = step_offset

class FiniteSystemRunner(_Simulator):
    '''Class to create an object that runs a simulation of an agent system
    using a system specific mover. The class handles sampling of data at
    a set interval, including agent state and agent graph relations. The
    simulation involves a finite number of steps

    Parameters
    ----------
    n_iter : int
        Total number of iterations to simulate. Each iteration implies one
        propagation, which means if the mover includes multiple agent
        operations, more than `n_iter` agent operations are executed
    system_propagator : callable
        A callable object, such as a function or class instance, that specifies
        how the agent system is propagated
    system_io : SystemIO, optional
        An instance of the SystemIO class that defines what system data to
        sample and how to write it to disk
    progress_report_steps : int, optional
        If provided, every simulation step that is a multiplier of given
        integer, a progress statement is printed to stdout. This can provide
        useful information of progress of lengthy simulations
    system_propagator_kwargs : dict, optional
        Named argument dictionary to the `system_propagator`

    '''
    def __call__(self, system):
        '''The outer loop for a finite step simulation of a system, each step a
        system mover is applied

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
            self.step(system)

            if not self.progress_report_step is None:
                if k_iter % self.progress_report_step == 0:
                    print (self.print_progress(k_iter))

    def __init__(self, n_iter, system_mover,
                 n_iter_init_offset=0,
                 system_io=None, progress_report_step=None):

        self.n_iter = n_iter

        self.progress_report_step = progress_report_step
        self.print_progress = lambda x: '---> ' + str(x) + 'steps of total ' + \
                              str(self.n_iter) + ' have been executed'

        super().__init__(system_mover, system_io, n_iter_init_offset)

class ConditionalSystemRunner(_Simulator):
    '''A simulator of an Agent Management System where the termination criteria
    is some condition rather than a set number of step

    '''
    pass
