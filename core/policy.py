'''Plan related classes

'''
from collections import Iterable

#class Plan(object):
#    '''Bla bla
#
#    '''
#    @permissions_check
#    def apply_to(self, agent):
#        '''Bla bla
#
#        '''
#        return self.func(agent)
#
#    def __init__(self, name, func):
#
#        self.name = name
#        self.func = func

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

    def __call__(self):
        '''Bla bla

        '''
        pass 

    def __init__(self, name, verb_phrase, condition=None):

        self.name = name
        self.condition = condition

        self.verb_phrase = verb_phrase 

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
    def _apply_cond_func(self, message):
        '''Bla bla

        '''
        if self.keys is None:
            args_values = tuple(message.values())

        else:
            args_values = tuple([message[key] for key in self.keys])

        return self.func(*args_values, **self.kwargs)

    def __init__(self, name, func, keys, kwargs={}):
        
        self.name = name
        self.func = func
        self.kwargs = kwargs

        if isinstance(keys, str):
            self.keys = (keys,)
        elif isinstance(keys, Iterable):
            self.keys = keys
        elif keys is None:
            self.keys = keys
        else:
            raise TypeError('Element labels to AutoCondition should be ' + \
                            'a string or an iterable')

class AutoBeliefCondition(_AutoCondition):
    '''Bla bla

    '''
    def __call__(self, agent):
        '''Bla bla

        '''
        message = agent.belief[self.message_input]
        return self._apply_cond_func(message)

    def __init__(self, belief_cond_name, cond_func, message_input_name, 
                 belief_keys=None, cond_func_kwargs={}):

        super().__init__(belief_cond_name, cond_func, belief_keys, 
                         cond_func_kwargs)
        self.message_input = message_input_name

class AutoResourceCondition(_AutoCondition):
    '''Bla bla

    '''
    def __call__(self, agent):
        '''Bla bla

        '''
        resource = agent.resource
        return self._apply_cond_func(resource)

    def __init__(self, resource_cond_name, cond_func, resource_keys=None, 
                 cond_func_kwargs={}):

        super().__init__(resource_cond_name, cond_func, resource_keys, 
                         cond_func_kwargs)
