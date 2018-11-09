'''Plan related classes

'''
class Clause(object):
    '''Bla bla

    '''
    def autocondition(self, func):
        '''Bla bla

        '''
        def wrapper(*args):
            truth_value = None
            func(*args)
            if not self.condition is None:
                truth_value = self.condition(*args)

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
        self.condition = condition
        self.verb_sequence = verbs
        self.engager_func = engager_func
        if not self.verb_sequence is None:
            self.apply_to = self.autocondition(self._apply_verb_sequence_to)
        else:
            self.apply_to = self.autocondition(self._apply_engager_to)

class Heartbeat(object):
    '''Bla bla

    '''
    def __call__(self, agent):
        '''Bla bla

        '''
        ret = True

        if self.inert:
            ret = False

        if not self.conditions is None:
            for condition in self.conditions:
                if not condition(agent):
                    ret = False

        self.ticks += self.ticker_arithmetic()
        if not self.max_ticker is None:
            if self.ticks > self.max_ticker:
                ret = False

        return ret

    def __init__(self, name, imprint_conditions=None, 
                 ticker_arithmetic=None, max_ticker=None):

        self.name = name

        self.conditions = imprint_conditions

        if ticker_arithmetic is None:
            self.ticker_arithmetic = lambda: 1
        else:
            self.ticker_arithmetic = ticker_arithmetic

        self.max_ticker = max_ticker
        self.ticks = 0
        self.inert = False

class _AutoCondition(object):
    '''Bla bla

    '''
    def __call__(self, agent):
        '''Bla bla

        '''
        imprint = getattr(agent, self.scaffold_name)
        if self.element_labels is None:
            args = tuple(imprint.values())
        else:
            args = tuple([imprint[key] for key in self.element_labels])

        return self.func(*args, **self.kwargs)

    def __init__(self, name, scaffold_name, element_labels, func, kwargs={}):
        
        self.name = name
        self.scaffold_name = scaffold_name
        self.element_labels = element_labels
        self.func = func
        self.kwargs = kwargs

class AutoBeliefCondition(_AutoCondition):
    '''Bla bla

    '''
    def __init__(self, belief_cond_name, belief_labels, cond_func, cond_func_kwargs={}):

        super().__init__(belief_cond_name, 'belief', belief_labels, 
                         cond_func, cond_func_kwargs)

class AutoResourceCondition(_AutoCondition):
    '''Bla bla

    '''
    def __init__(self, resource_cond_name, resource, resource_labels, 
                 cond_func, cond_func_kwargs={}):

        super().__init__(resource_cond_name, 'resource', resource_labels, 
                         cond_func, cond_func_kwargs)
