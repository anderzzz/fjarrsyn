'''Plan related classes

'''
class Chain(object):
    '''Bla bla

    '''
    def autocondition(self, func):
        '''Bla bla

        '''
        def wrapper(*args, **kwargs):
            truth_value = None
            func(*args, **kwargs)
            if not self.condition is None:
                truth_value = self.condition()

            return truth_value

        return wrapper

    def _apply_verb_sequence_to(self, agent):
        '''Bla bla

        '''
        ret = agent.engage(self.verb_sequence)

    def _apply_engager_to(self, agent):
        '''Bla bla

        '''
        raise NotImplementedError('Have not done this one')
        ret = self.engager()

    def set_engager(self, engager_func):
        '''Bla bla

        '''
        self.engager_func = engager_func

    def __init__(self, name, verbs=None, condition=None, engager_func=None):
        self.name = name
        self.verb_sequence = verbs
        self.condition = condition
        self.engager_func = engager_func

        if not self.verb_sequence is None:
            self.apply_to = self.autocondition(self._apply_verb_sequence_to)
        else:
            self.apply_to = self.autocondition(self._apply_engager_to)

class _AutoCondition(object):
    '''Bla bla

    '''
    def __call__(self):
        '''Bla bla

        '''
        args = tuple(self.imprint.values())
        return self.func(*args, **self.kwargs)

    def __init__(self, name, imprint, func, kwargs={}):
        
        self.name = name
        self.imprint = imprint
        self.func = func
        self.kwargs = kwargs

class AutoBeliefCondition(_AutoCondition):
    '''Bla bla

    '''
    def __init__(self, belief_cond_name, belief, cond_func, cond_func_kwargs={}):

        super().__init__(belief_cond_name, belief, cond_func, cond_func_kwargs)
