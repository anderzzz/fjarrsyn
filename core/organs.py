'''All organ classes of the basic Agent are contained in this file.

'''
import copy
from collections import OrderedDict, Iterable

from core.naturallaw import ResourceMapCollection, ResourceMap
from core.array import Buzz, Direction, Feature, \
                       Belief, Resource, Essence, \
                       ImprintOperator, _Array

class _Organ(object):
    '''Organ parent class, which defines common structure and method for all
    organs. 

    Parameters
    ----------
    organ_name : str
        Name of the organ
    array_input : _Array or None
        Instance of array the organ deals with as input. If None an OrderedDict
        is used as template, which upon execution will return empty values and
        keys
    organ_function : callable
        The function that upon execution performs the operations of the organ
    array_output : _Array or None
        Instance of message the organ deals with as output. If None and
        OrderedDict is used as template, which upon execution will return empty
        values and keys
    function_kwargs : dict, optional
        Any arguments needed for the organ_function

    '''
    def __init__(self, organ_name, array_input, 
                 organ_function, array_output, 
                 resource_map=None, organ_function_kwargs={}):

        def _decorate_always_iterable_output(f):
            '''Bla bla

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

        self.name = organ_name

        if not callable(organ_function):
            raise TypeError('Organ requires callable function for its operation')
        self.organ_func = _decorate_always_iterable_output(organ_function)

        if array_input is None:
            self.array_input = OrderedDict()
        elif isinstance(array_input, str):
            self.array_input = _Array(array_input, []) 
        else:
            self.array_input = array_input

        if array_output is None:
            self.array_output = OrderedDict()
        elif isinstance(array_output, str):
            self.array_output = _Array(array_input, []) 
        else:
            self.array_output = array_output

        if not resource_map is None:
            if not isinstance(resource_map, (ResourceMap, ResourceMapCollection)):
                raise TypeError('Organ resource maps should be of class ' + \
                                'ResourceMap or ResourceMapCollection')
        self.resource_map = resource_map

        self.kwargs = organ_function_kwargs

class Sensor(_Organ):
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
        kwargs = copy.copy(self.kwargs)
        kwargs['agent_index'] = agent_index

        out_values = self.organ_func(**kwargs)

        if self.resource_map is None:
            self.array_output.set_values(out_values)

        else:
            self.array_output.set_values(out_values[0])
            self.resource_map.set_values(out_values[1]) 

        return True

    def __init__(self, name, precept_label, sensor_func, buzz, 
                 resource_map=None, sensor_func_kwargs={}):

        if not isinstance(precept_label, str):
            raise TypeError('Sensor input should be string')

        if not isinstance(buzz, Buzz):
            raise TypeError('Sensor output should be of class Buzz')

        super().__init__(name, precept_label, sensor_func, 
                         buzz, resource_map, sensor_func_kwargs)

class Actuator(_Organ):
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
        direction_values = self.array_input.values()

        kwargs = copy.copy(self.kwargs)
        kwargs['agent_index'] = agent_index
        out_values = self.organ_func(*direction_values, **kwargs)

        if self.resource_map is None:
            pass

        else:
            out_values_naturallaw = out_values[self.array_output.n_elements:]
            self.resource_map.set_values(out_values_naturallaw)

        return True

    def __init__(self, actuator_name, direction, actuator_func, action_label,
                 resource_map=None, actuator_func_kwargs={}):

        if not isinstance(direction, Direction):
            raise TypeError('Actuator cannot handle input other than Direction')

        if not isinstance(action_label, str):
            raise TypeError('Actuator can only be given a string as its ' + \
                            'action_label output')

        super().__init__(actuator_name, direction, actuator_func, 
                         action_label, resource_map, actuator_func_kwargs)

class Interpreter(_Organ):
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
        inp_values = self.array_receiver().values()

        if self.belief_updater:
            current_beliefs = self.array_output.values()
            args = tuple(current_beliefs + inp_values)

        else:
            args = tuple(inp_values)

        out_values = self.organ_func(*args, **self.kwargs)

        if self.resource_map is None:
            self.array_output.set_values(out_values)

        else:
            self.array_output.set_values(out_values[0])
            self.resource_map.set_values(out_values[1]) 

        return True 

    def __init__(self, interpreter_name, inputer, interpreter_func, belief,
                 belief_updater=False, 
                 resource_map=None, interpreter_func_kwargs={}):

        if isinstance(inputer, (Buzz, Belief)):
            inputer_actual = ImprintOperator(inputer).identity

        elif isinstance(inputer, (Direction, Feature)):
            raise TypeError('Interpreter cannot handle Direction or Feature as input')

        else:
            inputer_actual = inputer

        if not isinstance(belief, Belief):
            raise TypeError('Interpreter output should be of class Belief')

        super().__init__(interpreter_name, None, interpreter_func, 
                         belief, resource_map, interpreter_func_kwargs)

        self.array_receiver = inputer_actual
        self.belief_updater = belief_updater

class Moulder(_Organ):
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
        belief_values = self.array_receiver().values()

        out_values = self.organ_func(*belief_values, **self.kwargs)

        out_values_intentional = out_values[:self.array_output.n_elements]
        self.array_output.set_values(out_values_intentional)

        if not self.resource_map is None:
            out_values_naturallaw = out_values[self.array_output.n_elements:]
            self.resource_map.set_values(out_values_naturallaw) 

        return True

    def __init__(self, moulder_name, inputer, moulder_func, direction,
                 resource_map=None, moulder_func_kwargs={}):

        if isinstance(inputer, Belief):
            inputer_actual = ImprintOperator(inputer).identity

        elif isinstance(inputer, (Buzz, Direction, Feature)):
            raise TypeError('Moulder cannot handle Direction, Buzz or Feature as input')

        else:
            inputer_actual = inputer

        super().__init__(moulder_name, None, 
                         moulder_func,  direction, 
                         resource_map, moulder_func_kwargs)

        self.array_receiver = inputer_actual

class Cortex(_Organ):
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
        agent_state_values = self.array_receiver().values()

        out_values = self.organ_func(*agent_state_values, **self.kwargs)
        self.array_output.set_values(out_values)

        return self.array_output

    def __init__(self, cortex_name, inputer, cortex_func, feature,
                 cortex_func_kwargs={}):

        if isinstance(inputer, (Essence, Resource, Belief)):
            inputer_actual = ImprintOperator(inputer).identity

        elif isinstance(inputer, (Direction, Feature, Buzz)):
            raise TypeError('Cortex cannot handle Direction, Buzz or Feature as input')

        else:
            inputer_actual = inputer

        if not isinstance(feature, Feature):
            raise TypeError('Cortex output should be of class Feature')

        super().__init__(cortex_name, None, cortex_func, feature, None,
                         cortex_func_kwargs)

        self.array_receiver = inputer_actual
