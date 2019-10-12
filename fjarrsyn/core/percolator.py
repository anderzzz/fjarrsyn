'''The Mover Parent Class'''

class Mover(object):
    '''Base class for all Movers to move an agent system forward

    Parameters
    ----------

    '''
    def enacted_by(self, agent_ms):
        '''Enact mover to given AMS

        Parameters
        ----------
        agent_ms : AgentSystemManager
            The agent system manager to which the mover is to be applied

        '''
        self.func(agent_ms, **self.func_kwargs)

    def __init__(self, name, engine, engine_kwargs={}):

        self.name = name

        if not callable(engine):
            raise TypeError('Function to Mover is not an executable')
        self.engine = engine
        self.engine_kwargs = engine_kwargs


class StandardMoverFunc(object):
    '''Convenience class to create standard Mover functions

    '''
    def __call__(self, kwargs):
        '''Caller'''

        self.func(**kwargs)

    def __init__(self, agent_iterator='shuffle', cleanse_at_start=True):

        raise NotImplementedError('Not yet implemented')