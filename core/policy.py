'''Policy classes that are used to define the dynamic aspects of an agent, such
that its potential intentions can be turned into a specific sequence of
intentional actions

'''
import networkx as nx
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

class Plan(object):
    '''Plan that agents can enact as part of their intentional execution

    '''
    def from_json(self, filepath):
        '''Bla bla

        '''
        pass

    def to_json(self, filepath):
        '''Bla bla

        '''
        pass

    def _get_root_index(self, t):
        '''Bla bla

        '''
        return [n for n, d in t.in_degree() if d == 0].pop(0)

    def enacted_by(self, agent, current_root_id=None):
        '''The recursive enaction function of the plan by the given agent

        Parameters
        ----------
        agent : Agent
            The agent that is enacting the plan
        current_root_id : int, optional
            The id of the current node in the binary execution tree. Should be
            None for the caller, and only within the recursion is this
            parameter adjusted to trace where in the tree the execution is

        Returns
        -------
        drill_down : bool
            If further drilling down the execution tree is to be done. Set to
            False when leaf reached

        Notes
        -----
        This method is only to be called after the method `stamp_and_approve`
        is called wherein the execution tree is subjected to basic validation
        and the parent identified.

        '''
        #
        # Check that plan is stamped and approved
        #
        if current_root_id is None:
            try:
                current_root_id = self.tree_root_id
            except AttributeError:
                raise AttributeError('Likely error: plan was not stamped and approved')

        #
        # Extract the verb and phrase and execute it for the agent
        #
        current_node = self.tree.nodes[current_root_id]
        verb = current_node['verb']
        phrase = current_node['phrase']
        ret_val = getattr(agent, verb)(phrase)

        #
        # Determine if there are successors in the execution tree
        #
        successors = list(self.tree.successors(current_root_id))
        
        #
        # If there are successors select which path to go
        #
        drill_down = True
        for n in successors:
            if self.tree.edges[current_root_id, n]['polarity'] is True and \
                   ret_val is True:

                drill_down = self.enacted_by(agent, n)

            elif self.tree.edges[current_root_id, n]['polarity'] is False and \
                    ret_val is False:

                drill_down = self.enacted_by(agent, n)

            else:
                continue

            #
            # In correct executions this conditional breaks out of the
            # recursion once a leaf has been encountered
            #
            if drill_down is False:
                break

            else:
                raise RuntimeError('Unmatched verb return and plan edge ' + \
                                   'attribute. Could be caused by missing ' + \
                                   'cargo')

        return False 

    def add_cargo(self, verb_inp, phrase_inp):
        '''Adds a step in the execution tree, comprised on verb and phrase

        Parameters
        ----------
        verb : str
            The name of the verb of an agent to include in the execution
        phrase_inp : str
            The phrase to couple with the verb

        Returns
        -------
        cargo_id : int
            The integer ID this particular execution unit is assigned. This is
            the ID that is referenced as dependencies between units are set
            with `add_dependency`

        '''
        self.tree.add_node(self.cargo_counter, verb=verb_inp, phrase=phrase_inp)
        self.cargo_counter += 1

        return self.cargo_counter

    def add_dependency(self, cc_parent, cc_child_true, cc_child_false=None):
        '''Adds a dependency or parent-child relation between two execution
        units

        Parameters
        ----------
        cc_parent : int
            The integer ID of the parent execution unit in the dependency
        cc_child_true : int
            The integer ID of the child execution unit in the dependency, given
            that the parent evaluates to True upon its execution
        cc_child_false : int, optional
            The integer ID of the child execution unit in the dependency, given
            that the parent evaluates to False upon its execution. Optional
            since by default agent verbs returns True

        '''
        self.tree.add_edge(cc_parent, cc_child_true, polarity=True)
        if not cc_child_false is None:
            self.tree.add_edge(cc_parent, cc_child_false, polarity=False)

    def stamp_and_approve(self):
        '''Mandatory method to validate and seal the execution tree such that
        it can be enacted by an agent

        Raises
        ------
        ValueError
            If the execution units do not form a tree

        '''
        if not nx.is_tree(self.tree):
            raise ValueError('The plan graph is not structured like a tree')
        self.tree_root_id = self._get_root_index(self.tree)

    def __init__(self, name, tree=None):

        self.name = name
        self.tree = nx.DiGraph() 
        self.cargo_counter = 0
