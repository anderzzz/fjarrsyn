'''The Percolator Parent Class'''

class Percolator(object):
    '''Base class for all Percolators to move an agent system forward

    Parameters
    ----------

    '''
    def enacted_by(self, agent_ms):
        '''Enact percolator to given AMS

        Parameters
        ----------
        agent_ms : AgentSystemManager
            The agent system manager to which the percolator is to be applied

        '''
        self.func(agent_ms, **self.func_kwargs)

    def __init__(self, name, func, func_kwargs):

        self.name = name

        if not callable(func):
            raise TypeError('Function to Percolator is not an executable')
        self.func = func
        self.func_kwargs = func_kwargs


class StandardPercolatorFunc(object):
    '''Convenience class to create standard percolator functions

    '''
    def __call__(self, kwargs):
        '''Caller'''

        self.func(**kwargs)

    def __init__(self, agent_iterator='shuffle', cleanse_at_start=True):

        raise NotImplementedError('Not yet implemented')