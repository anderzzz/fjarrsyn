'''Instructor classes

'''
import copy
import numpy as np
import numpy.random
from collections import OrderedDict, Iterable

from core.scaffold_map import _Map, MapCollection
from core.message import Buzz, Direction, Feature, \
                         Belief, Resource, Essence, \
                         ImprintOperator
from core.array import _Array

INSTRUCTOR_POLARITY = ['producer', 'transformer', 'consumer']
INSTRUCTOR_INGREDIENT = ['tangible', 'abstract']

class _Instructor(object):
    '''Bla bla

    '''
    def __init__(self, name, engine, 
                 message_input=None, message_output=None,
                 scaffold_map=None, engine_kwargs={}):

        def _decorate_always_iterable_output(f):
            '''Decorator to ensure the engine always generates an iterable
            output, even if the function returns a single object.

            '''
            def wrapper(*args, **kwargs):
                ret = f(*args, **kwargs)
                if isinstance(ret, str):
                    return (ret,)
                elif (not isinstance(ret, Iterable)):
                    return (ret,)
                else:
                    return ret

            return wrapper

        self.name = name

        if not callable(engine):
            raise TypeError('Instructor engine must be callable')
        self.engine = _decorate_always_iterable_output(engine)
        self.kwargs = engine_kwargs

        self.message_input = message_input
        if not message_output is None:
            if not isinstance(message_output, _Array):
                raise TypeError('Message output must be a child to _Array')
        self.message_output = message_output

        if not scaffold_map is None:
            if not isinstance(scaffold_map, (_Map, MapCollection)):
                raise TypeError('Scaffold map must be a child to _Map')
        self.scaffold_map = scaffold_map

        if (self.message_output is None) and (self.scaffold_map is None):
            type1 = INSTRUCTOR_POLARITY[2]
            
        elif self.message_input is None:
            type1 = INSTRUCTOR_POLARITY[0]

        else:
            type1 = INSTRUCTOR_POLARITY[1]

        type2_container = []
        if not self.scaffold_map is None:
            type2_container.append(INSTRUCTOR_INGREDIENT[0])

        if (not self.message_input is None) or (not self.message_output is None):
            type2_container.append(INSTRUCTOR_INGREDIENT[1])

        if len(type2_container) == 0:
            raise ValueError('Instructor must engage with at least a ' + \
                             'message input, message output, or scaffold map')

        self.type_label = type1 + ':' + '-'.join(type2_container)

#class _Organ(object):
#    '''Organ parent class, which defines common structure and method for all
#    organs. 
#
#    Parameters
#    ----------
#    organ_name : str
#        Name of the organ
#    array_input : _Array or None
#        Instance of array the organ deals with as input. If None an OrderedDict
#        is used as template, which upon execution will return empty values and
#        keys
#    organ_function : callable
#        The function that upon execution performs the operations of the organ
#    array_output : _Array or None
#        Instance of message the organ deals with as output. If None and
#        OrderedDict is used as template, which upon execution will return empty
#        values and keys
#    function_kwargs : dict, optional
#        Any arguments needed for the organ_function
#
#    '''
#    def __init__(self, organ_name, array_input, 
#                 organ_function, array_output, 
#                 resource_map=None, organ_function_kwargs={}):
#
#        def _decorate_always_iterable_output(f):
#            '''Decorator to ensure that functions that organ functions that
#            return a single value fit within the general slicing logic,
#            accomplished by making single value returns a one-member tuple
#
#            '''
#            def wrapper(*args, **kwargs):
#                ret = f(*args, **kwargs)
#                if isinstance(ret, str):
#                    return (ret,)
#                elif (not isinstance(ret, Iterable)):
#                    return (ret,)
#                else:
#                    return ret
#
#            return wrapper
#
#        #
#        # Name of the organ
#        #
#        self.name = organ_name
#
#        #
#        # Verify and define the organ function that is called upon execution
#        #
#        if not callable(organ_function):
#            raise TypeError('Organ requires callable function for its operation')
#        self.organ_func = _decorate_always_iterable_output(organ_function)
#        self.kwargs = organ_function_kwargs
#
#        #
        # Set array input and output. This handles cases where the input is
        # either not defined or a string
#        #
#        if array_input is None:
#            self.array_input = OrderedDict()
#        elif isinstance(array_input, str):
#            self.array_input = _Array(array_input, []) 
#        else:
#            self.array_input = array_input
#
#        if array_output is None:
#            self.array_output = OrderedDict()
#        elif isinstance(array_output, str):
#            self.array_output = _Array(array_output, []) 
#        else:
#            self.array_output = array_output
#
#        #
#        # Verify the resource map if present
#        #
#        if not resource_map is None:
#            if not isinstance(resource_map, (ResourceMap, ResourceMapCollection)):
#                raise TypeError('Organ resource maps should be of class ' + \
#                                'ResourceMap or ResourceMapCollection')
#        self.resource_map = resource_map

class Sensor(_Instructor):
    '''Sensor class, which defines how a precept of the external World is
    turned into buzz within the agent.

    Parameters
    ----------
    name : str
        Name of sensor
    precept_name : str
        Name of the precept of the World to interact with
    sensor_func : callable
        Callable function that upon execution reads precept and returns the
        buzz dictionary
    buzzkeys : list
        List of strings for the buzz names that the sensor generates, must be
        identical to the keys for the dictionary returned by the `sensor_func`
    kwargs : dict, optional
        Named arguments for the `sensor_func`

    '''
    def __call__(self, agent_index):
        '''Execute the sensor function with check that buzz output conforms to
        expected shape.

        Returns
        -------
        buzz : dict
            The buzz generated by the Sensor as it interacts with environment

        Raises
        ------
        ValueError
            If the sensor function returns a buzz dictionary with keys that do
            not match the buzz keys defined during sensor initialization.

        '''
        if self.func_get_agent_id:
            kwargs = copy.copy(self.kwargs)
            kwargs['agent_index'] = agent_index
        
        else:
            kwargs = self.kwargs

        out_values = self.engine(**kwargs)

        out_values_intentional = out_values[:self.message_output.n_elements]
        self.message_output.set_values(out_values_intentional)

        if not self.scaffold_map is None:
            out_values_naturallaw = out_values[self.message_output.n_elements:]
            self.scaffold_map.set_values(out_values_naturallaw)

        return True

    def __init__(self, sensor_name, sensor_func, buzz, 
                 resource_map=None, func_get_agent_id=True,
                 sensor_func_kwargs={}):

        if not isinstance(buzz, Buzz):
            raise TypeError('Sensor output should be of class Buzz')

        super().__init__(sensor_name, sensor_func, 
                         message_output=buzz, 
                         scaffold_map=resource_map, 
                         engine_kwargs=sensor_func_kwargs)
        self.func_get_agent_id = func_get_agent_id

class Actuator(_Instructor):
    '''Actuator class, which defines how an action by the agent alters the
    external world.

    Parameters
    ----------
    name : str
        Name of the actuator
    action_name : str
        Name of the action to act on the World
    actuator_func : callable
        Callable function that upon execution alters the World. The function
        does not have to return anything
    keys2populate : list
        Container of names of the arguments to the callable function that
        define the specific action. This list should exclude any agent
        identifier, which declares where in the World the action is applied.
    agent_index : str
        Agent index in the World onto which the action should be applied

    '''
    def __call__(self, agent_index):
        '''Execute the actuator function and alter the World

        Notes
        -----
        The actuator can only be executed after the actuator has been
        populated, which is done with the `populate` method

        Raises
        ------
        RuntimeError
            In case the actuator is executed prior to population

        '''
        direction_values = self.message_input.values()

        if self.func_get_agent_id:
            kwargs = copy.copy(self.kwargs)
            kwargs['agent_index'] = agent_index

        else:
            kwargs = self.kwargs

        out_values = self.engine(*direction_values, **kwargs)

        if not self.scaffold_map is None:
            out_values_naturallaw = out_values
            self.scaffold_map.set_values(out_values_naturallaw)

        return True

    def __init__(self, actuator_name, actuator_func, direction,
                 resource_map=None, func_get_agent_id=True,
                 actuator_func_kwargs={}):

        if not isinstance(direction, Direction):
            raise TypeError('Actuator cannot handle input other than Direction')

        super().__init__(actuator_name, actuator_func, 
                         message_input=direction,
                         scaffold_map=resource_map, 
                         engine_kwargs=actuator_func_kwargs)
        self.func_get_agent_id = func_get_agent_id

class Interpreter(_Instructor):
    '''Interpreter class, which defines how buzz from a sensor is made into
    persistent beliefs of the agent.

    Parameters
    ----------
    name : str
        Name of the interpreter
    buzz_names : list
        Container of names of the buzz to be interpreted. Must correspond with
        the output from the relevant sensor
    interpreter_func : callable
        Callable function that upon execution computes and assigns belief given
        the buzz input
    kwargs : dict, optional
        Any arguments other than the buzz needed in order to execute the
        interpreter function

    '''
    def __call__(self):
        '''Execute the interpreter function

        Parameters
        ----------
        buzz : dict
            The buzz values from the relevant sensor

        Returns
        -------
        belief_updated : list
            List of keys to the beliefs that were updated following the
            interpretation

        '''
        inp_values = self.message_input().values()

        if self.belief_updater:
            current_beliefs = self.message_output.values()
            args = tuple(current_beliefs + inp_values)

        else:
            args = tuple(inp_values)

        out_values = self.engine(*args, **self.kwargs)

        out_values_intentional = out_values[:self.message_output.n_elements]
        self.message_output.set_values(out_values_intentional)

        if not self.scaffold_map is None:
            out_values_naturallaw = out_values[self.message_output.n_elements:]
            self.scaffold_map.set_values(out_values_naturallaw) 

        return True 

    def __init__(self, interpreter_name, interpreter_func, inputer, belief,
                 resource_map=None, interpreter_func_kwargs={},
                 belief_updater=False):

        if isinstance(inputer, (Buzz, Belief)):
            inputer_actual = ImprintOperator(inputer).identity

        elif isinstance(inputer, (Buzz, Direction, Feature)):
            raise TypeError('Interpreter cannot handle Direction, Buzz or Feature as input')

        else:
            inputer_actual = inputer

        if not isinstance(belief, Belief):
            raise TypeError('Interpreter output should be of class Belief')

        super().__init__(interpreter_name, interpreter_func, 
                         message_input=inputer_actual,
                         message_output=belief,
                         scaffold_map=resource_map,
                         engine_kwargs=interpreter_func_kwargs)

        self.belief_updater = belief_updater

class Moulder(_Instructor):
    '''Moulder class, which defines how beliefs are turned into an executable
    instance of an actuator.

    Parameters
    ----------
    name : str
        Name of moulder
    belief_names : list
        Container of belief labels that the moulder engages with
    moulder_func : callable
        Callable function that upon execution processes agent belief and
        scaffold into a complete set of parameters to be used to populate an
        actuator
    kwargs : dict, optional
        Named arguments for the `moulder_func`

    '''
    def __call__(self):
        '''Execute the moulder to populate an actuator

        Notes
        -----
        After excecution of the moulder the actuator can be executed. Prior to
        moulding the actuator is form without content.

        Parameters
        ----------
        belief : dict
            Dictionary of belief values, at least a subset of which overlaps
            with the belief names defined during initialization
        actuator
            The actuator instance to populate. If not defined the moulder is
            executed expecting only to create an object force output

        '''
        belief_values = self.message_input().values()

        out_values = self.engine(*belief_values, **self.kwargs)

        out_values_intentional = out_values[:self.message_output.n_elements]
        self.message_output.set_values(out_values_intentional)

        if not self.scaffold_map is None:
            out_values_naturallaw = out_values[self.message_output.n_elements:]
            self.scaffold_map.set_values(out_values_naturallaw) 

        return True

    def __init__(self, moulder_name, moulder_func, inputer, direction,
                 resource_map=None, moulder_func_kwargs={}):

        if isinstance(inputer, Belief):
            inputer_actual = ImprintOperator(inputer).identity

        elif isinstance(inputer, (Buzz, Direction, Feature)):
            raise TypeError('Moulder cannot handle Direction, Buzz or Feature as input')

        else:
            inputer_actual = inputer

        if not isinstance(direction, Direction):
            raise TypeError('Moulder output should be of class Direction')

        super().__init__(moulder_name, moulder_func,
                         message_input=inputer_actual,
                         message_output=direction,
                         scaffold_map=resource_map,
                         engine_kwargs=moulder_func_kwargs)

class Cortex(_Instructor):
    '''Cortex class, which defines reaction to a certain tickle from the World.
    The Cortex is separate from beliefs and depend only on scaffold

    Parameters
    ----------
    name : str
        Name of cortex
    tickle_name : str
        Name of the kind of external tickling that the cortex responds to
    cortex_func : callable
        Callable function that upon execution returns a value of some sort that
        at most can depend on the agent scaffold.
    kwargs : dict, optional
        Named arguments for the `cortex_func`

    '''
    def __call__(self):
        '''Execute the cortex

        Returns
        -------
        value
            Return value as the cortex is tickled.

        '''
        agent_state_values = self.message_input().values()

        out_values = self.engine(*agent_state_values, **self.kwargs)

        self.message_output.set_values(out_values)

        return self.message_output

    def __init__(self, cortex_name, cortex_func, inputer, feature,
                 cortex_func_kwargs={}):

        if isinstance(inputer, (Essence, Resource, Belief)):
            inputer_actual = ImprintOperator(inputer).identity

        elif isinstance(inputer, (Direction, Feature, Buzz)):
            raise TypeError('Cortex cannot handle Direction, Buzz or Feature as input')

        else:
            inputer_actual = inputer

        if not isinstance(feature, Feature):
            raise TypeError('Cortex output should be of class Feature')

        super().__init__(cortex_name, cortex_func, 
                         message_input=inputer_actual,
                         message_output=feature,
                         engine_kwargs=cortex_func_kwargs)

class Compulsion(_Instructor):
    '''Bla bla

    '''
    def __call__(self, agent_index):
        '''Bla bla

        '''
        if self.func_get_agent_id:
            kwargs = copy.copy(self.kwargs)
            kwargs['agent_index'] = agent_index

        else:
            kwargs = self.kwargs

        out_values = self.engine(**kwargs)

        self.scaffold_map.set_values(out_values)

        return True 

    def __init__(self, name, compel_func, resource_map,
                 func_get_agent_id=True, compel_func_kwargs={}):

        if not isinstance(resource_map, _Map):
            raise TypeError('Compulsion must have a resource map, child of _Map')

        super().__init__(name, compel_func, 
                         scaffold_map=resource_map, 
                         engine_kwargs=compel_func_kwargs)
        self.func_get_agent_id = func_get_agent_id

class Mutation(_Instructor):
    '''Bla bla

    '''
    def __call__(self, agent_index):
        '''Bla bla

        '''
        if np.random.ranf() < self.mutation_prob:
            if self.func_get_agent_id:
                kwargs = copy.copy(self.kwargs)
                kwargs['agent_index'] = agent_index

            else:
                kwargs = self.kwargs

            out_values = self.engine(**kwargs)

            self.scaffold_map.set_values(out_values)

        else:
            pass

        return True

    def __init__(self, name, mutate_func, essence_map,
                 mutation_prob=1.0, func_get_agent_id=True,
                 mutate_func_kwargs={}):

        if not isinstance(essence_map, _Map): 
            raise TypeError('Mutation must have a essence map, child of _Map')

        super().__init__(name, mutate_func, 
                         scaffold_map=essence_map, 
                         engine_kwargs=mutate_func_kwargs)
        self.func_get_agent_id = func_get_agent_id

        if mutation_prob > 1.0 or mutation_prob < 0.0:
            raise ValueError('Mutation probability must be in range 0.0 to 1.0')
        self.mutation_prob = mutation_prob

class MultiMutation(Mutation):

    def __call__(self, agent):
        '''Bla bla

        '''
        out_values = []
        for key in self.scaffold_map.keys():
            if np.random.ranf() < self.mutation_prob:
                essence_values = agent.essence[key]
                out_values.append(self.engine(*essence_values, **self.kwargs))

            else:
                out_values.append(None)

        self.scaffold_map.set_values(out_values)

