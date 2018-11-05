'''Plan related classes

'''
class Chain(object):
    '''Bla bla

    '''
    def execute(self):
        '''Bla bla

        '''
        truth_value = None

        ret = self.engager_func()

        if not self.condition is None:
            truth_value = self.condition()

        return truth_value

    def set_engager(self, engager_func):
        '''Bla bla

        '''
        self.engager_func = engager_func

    def __init__(self, name, verbs=None, condition=None, engager_func=None):
        self.name = name
        self.verb_sequence = verbs
        self.condition = condition
        self.engager_func = engager_func

class _AutoCondition(object):
    '''Bla bla

    '''
    def __call__(self):
        '''Bla bla

        '''
        pass

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
