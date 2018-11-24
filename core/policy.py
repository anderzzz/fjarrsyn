'''Plan related classes

'''
from collections import Iterable

class Clause(object):
    '''Collection of multiple atomic verbs that can be executed in defined
    sequence under a meaningful semantic label. To the clause a binary test of
    a condition can be attached.

    Parameters
    ----------
    name : str
        The name of the clause
    verb_phrase : list, optional
        A list of two-membered tuples. Each tuple defines the atomic verb and
        the associated phrase, see details in Notes. The order of the tuples
        defines the order the atomic verbs are executed
    condition : child of _AutoCondition, optional
        A child class of the _AutoCondition parent class, which defines a
        condition to evaluate with respect to an agent belief or resource after
        the execution of the atomic verbs. 

    Notes
    -----
    The clause is defined by a sequence of atomic verb-phrase pairs as well as
    a condition. A clause can be comprised of one of the two components as
    well. The verb-phrase pairs are semantically defined, such as

    [('sense', 'noise in surrounding'),('interpret', 'possible ongoing activity')]

    where the first member of each tuple must correspond to an atomic verb of
    the agent, and the second member of each tuple must correspond to a
    particular Sensor or Interpreter (in the above example) of the agent. Other
    verbs and organs can be employed, and longer sequences can be used.

    If only a condition should be checked, the verb-phrase sequence should be
    left unspecified.

    '''
    def __call__(self, agent):
        '''The execution (that is 'prouncement') of the clause for a given
        agent

        Parameters
        ----------
        agent : Agent
            The agent for whom the clause is executed

        Returns
        -------
        truth_value : bool
            The truth value of the clause. If the clause contains an
            autocondition, the truth value is the return value of the
            autocondition. If the clause contains no autocondition, the truth
            value is the logical conjunction of the return values of the atomic
            verbs, which should be `True`, unless at least one instructor
            engine failed to execute witout exception.

        '''
        ret = True
        for verb, phrase in self.verb_phrase:
            ret_tmp = getattr(agent, verb)(phrase)
            ret = ret and ret_tmp

        truth_value = ret

        if not self.condition is None:
            truth_value = self.condition(agent, **self.condition_kwargs)

        return truth_value

    def __init__(self, name, verb_phrase=[], condition=None, condition_kwargs={}):

        self.name = name

        if not condition is None:
            if not isinstance(condition, _AutoCondition): 
                raise TypeError('The condition of a clause must be an auto condition')
        self.condition = condition
        self.condition_kwargs = condition_kwargs

        if not isinstance(verb_phrase, Iterable):
            raise TypeError('The verb phrase pairs must be part of an iterable')
        if len(verb_phrase) > 0:
            for vp in verb_phrase:
                if len(vp) != 2:
                    raise ValueError('Each verb phrase entry should be a pair ' + \
                                     'of strings, the verb, then the phrase')
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
