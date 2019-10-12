'''The Mover Parent Class'''

from fjarrsyn.core.agent_ms import AgentManagementSystem

class Mover(object):
    '''Base class for all Movers to move an agent system forward

    Parameters
    ----------

    '''
    def moved_by(self, agent_ms):
        '''Move the mover of given AMS

        Parameters
        ----------
        agent_ms : AgentSystemManager
            The agent system manager to which the mover is to be applied

        '''
        if isinstance(agent_ms, AgentManagementSystem):
            raise TypeError('Invalid class encountered: %s' %(str(type(agent_ms))))

        self.engine(agent_ms, **self.kwargs)

    def __init__(self, name, engine, kwargs={}):

        self.name = name

        if not callable(engine):
            raise TypeError('Function to Mover is not an executable')
        self.engine = engine
        self.kwargs = kwargs


class StandardMoverFunc(object):
    '''Convenience class to create standard Mover functions

    '''
    def __call__(self, kwargs):
        '''Caller'''

        self.func(**kwargs)

    def __init__(self, agent_iterator='shuffle', cleanse_at_start=True):

        raise NotImplementedError('Not yet implemented')