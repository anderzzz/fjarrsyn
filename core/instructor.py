'''Instructors are compound objects that connect messages and maps by an engine
in order to form organs and laws of the agents. Therefore instructors are
central to the agent-based modelling.

'''
import copy
import numpy as np
import numpy.random
from collections import OrderedDict, Iterable

from core.scaffold_map import ResourceMap, EssenceMap, \
                              MapCollection, _Map
from core.message import Buzz, Direction, Feature, \
                         Belief, Resource, Essence, \
                         ImprintOperator

class _Instructor(object):
    '''Base class for all instructors. Common attributes are defined and type
    checks are done on inputs.

    Parameters
    ----------
    name : str
        Name of the instructor
    engine : callable
        Function that processes input from the agent (if any) in order to 
        produce output to the agent (if any). The function can perform
        additional operations outside the agent. Conventionally, the only
        operations within the agent should be encoded as part of the message
        and scaffold_map output, not performed by the engine
    message_input : optional
        Object encoding any agent input to the instructor. The input
        message is conventionally output from another instructor.
    message_output : optional
        Object encoding any agent output from the instructor. The
        engine populates the values of the Message object given here.
    scaffold_map : _Map or MapCollection, optional
        Map object encoding any changes to the tangible Messages of the agent.
        The engine populates the values of the Map object given here.
    engine_kwargs : dict, optional
        Named arguments for the engine function.

    '''
    _INSTRUCTOR_POLARITY = ['producer', 'transformer', 'consumer']
    _INSTRUCTOR_INGREDIENT = ['tangible', 'abstract']

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

        #
        # Set engine attributes
        #
        if not callable(engine):
            raise TypeError('Instructor engine must be callable')
        self.engine = _decorate_always_iterable_output(engine)
        self.kwargs = engine_kwargs

        #
        # Message input and output can be of flexible type. These are checked
        # in child classes
        #
        self.message_input = message_input
        self.message_output = message_output

        if not scaffold_map is None:
            if not isinstance(scaffold_map, (_Map, MapCollection)):
                raise TypeError('Scaffold map must be a child to _Map')
        self.scaffold_map = scaffold_map

        #
        # Compute the instructor logical type
        #
        if (self.message_output is None) and (self.scaffold_map is None):
            type1 = self._INSTRUCTOR_POLARITY[2]
            
        elif self.message_input is None:
            type1 = self._INSTRUCTOR_POLARITY[0]

        else:
            type1 = self._INSTRUCTOR_POLARITY[1]

        type2_container = []
        if not self.scaffold_map is None:
            type2_container.append(self._INSTRUCTOR_INGREDIENT[0])

        if (not self.message_input is None) or (not self.message_output is None):
            type2_container.append(self._INSTRUCTOR_INGREDIENT[1])

        if len(type2_container) == 0:
            raise ValueError('Instructor must engage with at least a ' + \
                             'message input, message output, or scaffold map')

        self.type_label = type1 + ':' + '-'.join(type2_container)

class Sensor(_Instructor):
    '''Sensor class, which defines how a precept of the external world is
    turned into buzz within the agent. Conventionally the external world is in
    the scope of the Agent Management System.

    Parameters
    ----------
    sensor_name : str
        Name of sensor
    sensor_func : callable
        The function that defines the engine of the sensor that produces the
        output buzz. Conventionally the function is defined within the scope of
        the Agent Managament System
    buzz : Buzz
        Buzz object with defined semantics, which the sensor engine populates
        upon execution
    resource_map : ResourceMap or MapCollection, optional
        In case the execution of the sensor produces tangible output to alter
        agent resources, a map with defined semantics is given
    func_get_agent_id : bool, optional
        If True, the sensor function is provided the agent index as one of the
        input arguments, if False, not so.
    sensor_func_kwargs : dict, optional
        Named arguments to the sensor function

    Raises
    ------
    TypeError
        If the `buzz` parameter provides a message of type other than Buzz

    '''
    def __call__(self, agent_index):
        '''Execute the sensor and populate the output

        Parameters
        ----------
        agent_index : str
            The agent index for the agent whose sensor is executed

        Returns
        -------
        success : bool
            If execution of engine successful, return value is True. If
            execution created Exception, return value is False     

        '''
        if self.func_get_agent_id:
            kwargs = copy.copy(self.kwargs)
            kwargs['agent_index'] = agent_index
        
        else:
            kwargs = self.kwargs

        try:
            out_values = self.engine(**kwargs)
        except Exception:
            return False

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
    '''Actuator class, which defines how the Agent takes actions onto the
    external world. Conventionally the external world is in the scope of the
    Agent Management System.

    Parameters
    ----------
    actuator_name : str
        Name of actuator
    actuator_func : callable
        The function that defines the engine of the actuator that consumes the
        input direction. Conventionally the function is defined within the scope of
        the Agent Managament System
    direction : Direction
        Direction object with defined semantics, whose values the actuator engine
        consumes upon execution. Conventionally the Direction object has been
        produced by a moulder
    resource_map : ResourceMap or MapCollection, optional
        In case the execution of the actuator produces tangible output to alter
        agent resources, a map with defined semantics is given
    func_get_agent_id : bool, optional
        If True, the actuator function is provided the agent index as one of the
        input arguments, if False, not so.
    actuator_func_kwargs : dict, optional
        Named arguments to the actuator function

    Raises
    ------
    TypeError
        If the `direction` parameter provides a message of type other than
        Direction

    '''
    def __call__(self, agent_index):
        '''Execute the actuator to consume input and populate the output (if
        any)

        Parameters
        ----------
        agent_index : str
            The agent index for the agent whose actuator is executed

        Returns
        -------
        success : bool
            If execution of engine successful, return value is True. If
            execution created Exception, return value is False     

        '''
        direction_values = self.message_input.values()

        if self.func_get_agent_id:
            kwargs = copy.copy(self.kwargs)
            kwargs['agent_index'] = agent_index

        else:
            kwargs = self.kwargs

        try:
            out_values = self.engine(*direction_values, **kwargs)
        except Exception:
            return False

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
    '''Interpreter class, which defines how the Agent interprets buzz or
    beliefs in order to produce or update beliefs the agent holds. 

    Parameters
    ----------
    interpreter_name : str
        Name of interpreter
    interpreter_func : callable
        The function that defines the engine of the interpreter that consumes the
        input buzz or belief and which generates the belief output. Conventionally 
        the function is defined within the scope of the Agent
    inputer : Buzz, Belief or callable to access objects of such type
        The input to the engine, or an executable that returns the input the
        engine consumes. Conventionally the Buzz object has been produced by a
        sensor; conventionally the Belief object has been produced by another
        interpreter
    belief : Belief
        Belief object with defined semantics, which the interpreter engine populates
        upon execution
    resource_map : ResourceMap or MapCollection, optional
        In case the execution of the interpreter produces tangible output to alter
        agent resources, a map with defined semantics is given
    interpreter_func_kwargs : dict, optional
        Named arguments to the interpreter function
    belief_updater : bool, optional
        If True, the engine is provided as arguments the values of the belief
        of the output. This enables the engine to evaluate a change in belief
        and return updated beliefs. Note that the current values of the output
        are provided before the values of the input in the arguments passed to
        the engine. If False, the engine receives only values from the input. 

    Raises
    ------
    TypeError
        If the `belief` parameter provides a message of type other than
        Belief or if the `inputer` parameter provides a message of type other
        than Buzz or Belief.

    '''
    def __call__(self):
        '''Execute the interpreter to consume input and produce the output

        Returns
        -------
        success : bool
            If execution of engine successful, return value is True. If
            execution created Exception, return value is False     

        '''
        inp_values = self.message_input().values()

        if self.belief_updater:
            current_beliefs = self.message_output.values()
            args = tuple(current_beliefs + inp_values)

        else:
            args = tuple(inp_values)

        try:
            out_values = self.engine(*args, **self.kwargs)
        except Exception:
            return False

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
    '''Moulder class, which defines how the Agent moulds direction from
    beliefs in order to produce instruction for actuator. 

    Parameters
    ----------
    moulder_name : str
        Name of moulder
    moulder_func : callable
        The function that defines the engine of the moulder that consumes the
        input belief and which generates the direction output. Conventionally 
        the function is defined within the scope of the Agent
    inputer : Belief or callable to access object of that type
        The input to the engine, or an executable that returns the input the
        engine consumes. Conventionally the Belief object has been produced by
        an interpreter at some point in time.
    direction : Direction
        Direction object with defined semantics, which the moulder engine populates
        upon execution
    resource_map : ResourceMap or MapCollection, optional
        In case the execution of the moulder produces tangible output to alter
        agent resources, a map with defined semantics is given
    moulder_func_kwargs : dict, optional
        Named arguments to the moulder function

    Raises
    ------
    TypeError
        If the `direction` parameter provides a message of type other than
        Direction or if the `inputer` parameter provides a message of type other
        than Belief.

    '''
    def __call__(self):
        '''Execute the moulder to consume input and produce the output

        Returns
        -------
        success : bool
            If execution of engine successful, return value is True. If
            execution created Exception, return value is False     

        '''
        belief_values = self.message_input().values()

        try:
            out_values = self.engine(*belief_values, **self.kwargs)
        except Exception:
            return False

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
    '''Cortex class, which defines how the Agent responds to being tickled
    and produces a feature. 

    Parameters
    ----------
    cortex_name : str
        Name of cortex
    cortex_func : callable
        The function that defines the engine of the cortex that consumes the
        input imprint and which generates the feature output. Conventionally 
        the function is defined within the scope of the Agent
    inputer : Essence, Resource, Belief or callable
        The input to the engine, or an executable that returns the input the
        engine consumes. These objects encodes something persistent of the
        agent. 
    feature : Feature
        Feature object with defined semantics, which the cortex engine populates
        upon execution
    cortex_func_kwargs : dict, optional
        Named arguments to the cortex function

    Raises
    ------
    TypeError
        If the `inputer` parameter provides a message of type other than
        Essence, Resource or Belief, or if the `feature` parameter is a 
        message of type other than Feature.

    '''
    def __call__(self):
        '''Execute the cortex to consume input and produce the output

        Returns
        -------
        success : bool
            If execution of engine successful, return value is True. If
            execution created Exception, return value is False     

        '''
        agent_state_values = self.message_input().values()

        try:
            out_values = self.engine(*agent_state_values, **self.kwargs)
        except Exception:
            return False

        self.message_output.set_values(out_values)

        return True 

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
    '''Compulsion class, which defines how the Agent responds to being
    compelled to produce a tangible mapping

    Parameters
    ----------
    compel_name : str
        Name of compulsion
    compel_func : callable
        The function that defines the engine of the compulsion that produces
        the tangible resource mapping for the agent
    resource_map : ResourceMap or MapCollection
        Map with defined semantics to act on agent resources
    func_get_agent_id : bool, optional
        If True, the compel function is provided the agent index as one of the
        input arguments, if False, not so.
    compel_func_kwargs : dict, optional
        Named arguments to the compel function

    Raises
    ------
    TypeError
        If the resource map is not an instance of ResourceMap or MapCollection

    '''
    def __call__(self, agent_index):
        '''Execute the compulsion and populate the output

        Parameters
        ----------
        agent_index : str
            The agent index for the agent that is compelled

        Returns
        -------
        success : bool
            If execution of engine successful, return value is True. If
            execution created Exception, return value is False     

        '''
        if self.func_get_agent_id:
            kwargs = copy.copy(self.kwargs)
            kwargs['agent_index'] = agent_index

        else:
            kwargs = self.kwargs

        try:
            out_values = self.engine(**kwargs)
        except Exception:
            return False

        self.scaffold_map.set_values(out_values)

        return True 

    def __init__(self, compel_name, compel_func, resource_map,
                 func_get_agent_id=True, compel_func_kwargs={}):

        if not isinstance(resource_map, (ResourceMap, MapCollection)):
            raise TypeError('Compulsion must have a resource map of type ' + \
                            'ResourceMap or MapCollection')

        super().__init__(compel_name, compel_func, 
                         scaffold_map=resource_map, 
                         engine_kwargs=compel_func_kwargs)
        self.func_get_agent_id = func_get_agent_id

class Mutation(_Instructor):
    '''Mutation class, which defines how the Agent responds to being
    mutated to produce a tangible mapping

    Parameters
    ----------
    mutate_name : str
        Name of mutation
    mutate_func : callable
        The function that defines the engine of the mutation that produces
        the tangible resource mapping for the agent
    essence_map : EssenceMap or MapCollection
        Map with defined semantics to act on agent essence
    mutation_prob : float, optional
        Probability the mutation engine is executed
    func_get_agent_id : bool, optional
        If True, the mutate function is provided the agent index as one of the
        input arguments, if False, not so.
    mutate_func_kwargs : dict, optional
        Named arguments to the mutate function

    Raises
    ------
    TypeError
        If the essence map is not an instance of EssenceMap or MapCollection
    ValueError
        If the probability is not between 0.0 and 1.0

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

    def __init__(self, mutate_name, mutate_func, essence_map,
                 mutation_prob=1.0, func_get_agent_id=True,
                 mutate_func_kwargs={}):

        if not isinstance(essence_map, (EssenceMap, MapCollection)): 
            raise TypeError('Mutation must have an essence map of type ' + \
                            'EssenceMap or MapCollection')

        super().__init__(mutate_name, mutate_func, 
                         scaffold_map=essence_map, 
                         engine_kwargs=mutate_func_kwargs)
        self.func_get_agent_id = func_get_agent_id

        if mutation_prob > 1.0 or mutation_prob < 0.0:
            raise ValueError('Mutation probability must be in range 0.0 to 1.0')
        self.mutation_prob = mutation_prob

class MultiMutation(Mutation):

    def __call__(self, agent_index):
        '''Bla bla

        '''
        if self.func_get_agent_id:
            kwargs = copy.copy(self.kwargs)
            kwargs['agent_index'] = agent_index

        else:
            kwargs = self.kwargs

        out_values = []
        for key in self.scaffold_map:
            if np.random.ranf() < self.mutation_prob:
                out_values.append(self.engine(**kwargs))

            else:
                out_values.append(None)

        self.scaffold_map.set_values(out_values)

