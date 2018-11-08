'''Plan related classes

'''
class _Policy(object):
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

    def __init__(self, name, apply_func, condition=None):

        self.name = name
        self.apply_to = apply_func
        self.condition = condition

class Compulsion(_Policy):
    '''Bla bla

    '''
    def _apply_sequence(self, apply_func_sequence):
        '''Bla bla

        '''
        def wrapper(*args, **kwargs):
            for func in apply_func_sequence:
                func.apply_to(*args)

        return wrapper

    def __init__(self, name, natural_law, condition=None):
        
        super().__init__(name, self._apply_sequence(natural_law), condition)

class Clause(_Policy):
    '''Bla bla

    '''
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

        self.verb_sequence = verbs
        self.engager_func = engager_func
        if not self.verb_sequence is None:
            applier = self.autocondition(self._apply_verb_sequence_to)
        else:
            applier = self.autocondition(self._apply_engager_to)

        super().__init__(name, applier, condition)

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
