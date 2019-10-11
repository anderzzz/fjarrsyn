'''Instructors are compound objects that connect messages and maps by an engine
in order to form organs and laws of the agents. Therefore instructors are
central to the agent-based modelling.

'''
from collections import OrderedDict, Iterable

import numpy as np
import numpy.random

from fjarrsyn.core.scaffold_map import ResourceMap, EssenceMap, \
                              MapCollection, _Map
from fjarrsyn.core.message import Buzz, Direction, Feature, \
                         Belief, Resource, Essence, \
                         MessageOperator

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
        and scaffold_map output, not performed by the engine. The order of
        engine input and output are constrained by the child classes, see their
        documentation
    message_input : optional
        Object encoding any agent input to the instructor. The input
        message is conventionally output from another instructor. This
        parameter can be a message operator.
    message_output : optional
        Object encoding any agent output from the instructor. The
        engine populates the values of the Message object given here.
    scaffold_map_output : _Map or MapCollection, optional
        Map object encoding any changes to the tangible Messages of the agent.
        The engine populates the values of the Map object given here.
    resource_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the resource 
        values of the agent calling the instructor
    essence_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the essence
        values of the agent calling the instructor
    engine_kwargs : dict, optional
        Named arguments for the engine function.

    '''
    _INSTRUCTOR_POLARITY = ['producer', 'transformer', 'consumer']
    _INSTRUCTOR_INGREDIENT = ['tangible', 'abstract']

    def _format_op(self, inp, valid_class, invalid_classes):
        '''Check if input of valid class and turn into message operator if so.
        This includes creating empty return if input is None

        Parameters
        ----------
        inp
            Input message, message operator or None
        valid class
            Class that the base message should be of
        invalid_classes
            Single or tuple of classes that the input message should not be an
            instance of

        Returns
        -------
        ret : MessageOperator
            Validated operator that retrieves the appropriate values upon
            execution, including empty tuple

        Raises
        ------
        TypeError
            If input is instance of an invalid class

        '''
        if isinstance(inp, valid_class):
            ret = MessageOperator(inp)

        elif isinstance(inp, invalid_classes):
            raise TypeError('Invalid class encountered: %s' %(str(type(inp))))

        elif inp is None:
            ret = lambda : ()

        else:
            ret = inp

        return ret

    def _scaffold_mapper(self, engine_output):
        '''Perform the scaffold mapping of the engine output, if any such
        should be performed

        Parameters
        ----------
        engine_output : container
            The entire output from the instructor engine to be divided into
            the various output messages

        '''
        if self.scaffold_map_output is None:
            pass

        else:
            if self.message_output is None:
                out_values_naturallaw = engine_output

            else:
                out_values_naturallaw = engine_output[self.message_output.n_elements:]

            self.scaffold_map_output.set_values(out_values_naturallaw)

    def __init__(self, name, engine, 
                 message_input=None, message_output=None,
                 scaffold_map_output=None, 
                 resource_op_input=None, essence_op_input=None,
                 engine_kwargs={}):

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

        if not scaffold_map_output is None:
            if not isinstance(scaffold_map_output, (_Map, MapCollection)):
                raise TypeError('Scaffold map must be a child to _Map')
        self.scaffold_map_output = scaffold_map_output

        if not resource_op_input is None:
            if not callable(resource_op_input):
                raise TypeError('Resource operator input must be callable')
        self.resource_op_input = resource_op_input

        if not essence_op_input is None:
            if not callable(essence_op_input):
                raise TypeError('Essence operator input must be callable')
        self.essence_op_input = essence_op_input

        #
        # Compute the instructor logical type
        #
        if (self.message_output is None) and (self.scaffold_map_output is None):
            type1 = self._INSTRUCTOR_POLARITY[2]
            
        elif self.message_input is None:
            type1 = self._INSTRUCTOR_POLARITY[0]

        else:
            type1 = self._INSTRUCTOR_POLARITY[1]

        type2_container = []
        if not self.scaffold_map_output is None:
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
        the Agent Managament System, but not required.
    buzz : Buzz
        Buzz object with defined semantics, which the sensor engine populates
        upon execution
    resource_map_output : ResourceMap or MapCollection, optional
        In case the execution of the sensor produces tangible output to alter
        agent resources, a map with defined semantics is given
    resource_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the resource 
        values of the agent calling the instructor
    essence_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the essence
        values of the agent calling the instructor
    agent_id_to_engine : bool, optional
        If True, the agent ID of the calling agent is passed as an argument to
        the sensor function
    sensor_func_kwargs : dict, optional
        Named arguments to the sensor function

    Raises
    ------
    TypeError
        If the `buzz` parameter provides a message of type other than Buzz

    Notes
    -----
    The engine input parameters are constrained in the following order: First, any resource
    values from the `resource_op_input`, second, any essence values from the
    `essence_op_input`, third, any agent ID, last any keyword arguments.

    The engine output parameters are constrained in the following order: First,
    any data to populate the buzz output, second, any data to populate the
    output resource map.

    '''
    def __call__(self, agent_id):
        '''Execute the sensor and populate the output

        Parameters
        ----------
        agent_id : str
            Agent system ID of the calling agent

        Returns
        -------
        success 
            If execution of engine successful, return value is True. If
            execution of engine created Exception, that Exception is returned 

        '''
        resource_values = tuple(self.resource_op_input())
        essence_values = tuple(self.essence_op_input())
        args = resource_values + essence_values

        if self.agent_id_to_engine:
            args += (agent_id,)
            
        try:
            out_values = self.engine(*args, **self.kwargs)
        except Exception as err:
            return err

        out_values_intentional = out_values[:self.message_output.n_elements]
        self.message_output.set_values(out_values_intentional)
        self._scaffold_mapper(out_values)

        return True

    def __init__(self, sensor_name, sensor_func, buzz, 
                 resource_map_output=None, 
                 resource_op_input=None, essence_op_input=None,
                 agent_id_to_engine=False,
                 sensor_func_kwargs={}):

        if not isinstance(buzz, Buzz):
            raise TypeError('Sensor output should be of class Buzz')

        resource_op_actual = self._format_op(resource_op_input, Resource, (Essence,))
        essence_op_actual = self._format_op(essence_op_input, Essence, (Resource,))

        super().__init__(sensor_name, sensor_func, 
                         message_output=buzz, 
                         scaffold_map_output=resource_map_output, 
                         resource_op_input=resource_op_actual,
                         essence_op_input=essence_op_actual,
                         engine_kwargs=sensor_func_kwargs)

        self.agent_id_to_engine = agent_id_to_engine

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
    inputer : Direction or callable to access objects of such type
        The input to the engine, or an executable that returns the input the
        engine consumes. Conventionally the Direction object has been produced by a
        moulder.
    resource_map_output : ResourceMap or MapCollection, optional
        In case the execution of the actuator produces tangible output to alter
        agent resources, a map with defined semantics is given
    resource_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the resource 
        values of the agent calling the instructor
    essence_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the essence
        values of the agent calling the instructor
    agent_id_to_engine : bool, optional
        If True, the agent ID of the calling agent is passed as an argument to
        the actuator function
    actuator_func_kwargs : dict, optional
        Named arguments to the actuator function

    Raises
    ------
    TypeError
        If the `direction` parameter provides a message of type other than
        Direction

    Notes
    -----
    The engine input parameters are constrained in the following order: First,
    any values from the input direction, second, any resource
    values from the `resource_op_input`, third, any essence values from the
    `essence_op_input`, fourth, any agent ID, last any keyword arguments.

    The engine output parameters are constrained in the following order: First
    and only,any data to populate the output resource map.

    '''
    def __call__(self, agent_id):
        '''Execute the actuator to consume input and populate the output (if
        any)

        Parameters
        ----------
        agent_id : str
            The agent ID for the agent whose actuator is executed

        Returns
        -------
        success 
            If execution of engine successful, return value is True. If
            execution of engine created Exception, that Exception is returned     

        '''
        direction_values = tuple(self.message_input())
        resource_values = tuple(self.resource_op_input())
        essence_values = tuple(self.essence_op_input())
        args = direction_values + resource_values + essence_values

        if self.agent_id_to_engine:
            args += (agent_id,)

        try:
            out_values = self.engine(*args, **self.kwargs)
        except Exception as err:
            return err

        self._scaffold_mapper(out_values)

        return True

    def __init__(self, actuator_name, actuator_func, inputer, 
                 resource_map_output=None, 
                 resource_op_input=None, essence_op_input=None,
                 agent_id_to_engine=False,
                 actuator_func_kwargs={}):

        resource_op_actual = self._format_op(resource_op_input, Resource, (Essence,))
        essence_op_actual = self._format_op(essence_op_input, Essence, (Resource,))
        inputer_actual = self._format_op(inputer, Direction, (Buzz, Belief, Feature))

        super().__init__(actuator_name, actuator_func, 
                         message_input=inputer_actual,
                         scaffold_map_output=resource_map_output,
                         resource_op_input=resource_op_actual,
                         essence_op_input=essence_op_actual,
                         engine_kwargs=actuator_func_kwargs)

        self.agent_id_to_engine = agent_id_to_engine

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
    resource_map_output : ResourceMap or MapCollection, optional
        In case the execution of the interpreter produces tangible output to alter
        agent resources, a map with defined semantics is given
    resource_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the resource 
        values of the agent calling the instructor
    essence_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the essence
        values of the agent calling the instructor
    agent_id_to_engine : bool, optional
        If True, the agent ID of the calling agent is passed as an argument to
        the interpreter function
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

    Notes
    -----
    The engine input parameters are constrained in the following order: First,
    any values from the input buzz (or belief), second, any resource
    values from the `resource_op_input`, third, any essence values from the
    `essence_op_input`, fourth, any belief to be updated if `belief_updater` is
    True, fifth, any agent ID, last any keyword arguments.

    The engine output parameters are constrained in the following order: First,
    any value output to populate the output belief, second, any data to populate 
    the output resource map.

    '''
    def __call__(self, agent_id):
        '''Execute the interpreter to consume input and produce the output

        Parameters
        ----------
        agent_id : str
            The agent ID for the agent whose actuator is executed

        Returns
        -------
        success 
            If execution of engine successful, return value is True. If
            execution of engine created Exception, that Exception is returned     

        '''
        inp_values = tuple(self.message_input())
        resource_values = tuple(self.resource_op_input())
        essence_values = tuple(self.essence_op_input())
        args = inp_values + resource_values + essence_values

        if self.belief_updater:
            args += tuple(self.message_output.values())

        if self.agent_id_to_engine:
            args += (agent_id,)

        try:
            out_values = self.engine(*args, **self.kwargs)
        except Exception as err:
            return err

        out_values_intentional = out_values[:self.message_output.n_elements]
        self.message_output.set_values(out_values_intentional)
        self._scaffold_mapper(out_values)

        return True 

    def __init__(self, interpreter_name, interpreter_func, inputer, belief,
                 resource_map_output=None, 
                 resource_op_input=None, essence_op_input=None,
                 agent_id_to_engine=False,
                 interpreter_func_kwargs={},
                 belief_updater=False):

        if not isinstance(belief, Belief):
            raise TypeError('Interpreter output should be of class Belief')

        resource_op_actual = self._format_op(resource_op_input, Resource, (Essence,))
        essence_op_actual = self._format_op(essence_op_input, Essence, (Resource,))
        inputer_actual = self._format_op(inputer, (Buzz, Belief), (Direction, Feature))

        super().__init__(interpreter_name, interpreter_func, 
                         message_input=inputer_actual,
                         message_output=belief,
                         scaffold_map_output=resource_map_output,
                         resource_op_input=resource_op_actual,
                         essence_op_input=essence_op_actual,
                         engine_kwargs=interpreter_func_kwargs)

        self.agent_id_to_engine = agent_id_to_engine
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
    resource_map_output : ResourceMap or MapCollection, optional
        In case the execution of the moulder produces tangible output to alter
        agent resources, a map with defined semantics is given
    resource_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the resource 
        values of the agent calling the instructor
    essence_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the essence
        values of the agent calling the instructor
    agent_id_to_engine : bool, optional
        If True, the agent ID of the calling agent is passed as an argument to
        the moulder function
    moulder_func_kwargs : dict, optional
        Named arguments to the moulder function

    Raises
    ------
    TypeError
        If the `direction` parameter provides a message of type other than
        Direction or if the `inputer` parameter provides a message of type other
        than Belief.

    Notes
    -----
    The engine input parameters are constrained in the following order: First,
    any values from the input belief, second, any resource
    values from the `resource_op_input`, third, any essence values from the
    `essence_op_input`, fourth, any agent ID, last any keyword arguments.

    The engine output parameters are constrained in the following order: First,
    any value output to populate the output direction, second, any data to populate 
    the output resource map.

    '''
    def __call__(self, agent_id):
        '''Execute the moulder to consume input and produce the output

        Parameters
        ----------
        agent_id : str
            The agent ID for the agent whose actuator is executed

        Returns
        -------
        success 
            If execution of engine successful, return value is True. If
            execution of engine created Exception, that Exception is returned     

        '''
        belief_values = tuple(self.message_input())
        resource_values = tuple(self.resource_op_input())
        essence_values = tuple(self.essence_op_input())
        args = belief_values + resource_values + essence_values

        if self.agent_id_to_engine:
            args += (agent_id,)

        try:
            out_values = self.engine(*args, **self.kwargs)
        except Exception as err:
            return err

        out_values_intentional = out_values[:self.message_output.n_elements]
        self.message_output.set_values(out_values_intentional)
        self._scaffold_mapper(out_values)

        return True

    def __init__(self, moulder_name, moulder_func, inputer, direction,
                 resource_map_output=None, 
                 resource_op_input=None, essence_op_input=None,
                 agent_id_to_engine=False,
                 moulder_func_kwargs={}):

        if not isinstance(direction, Direction):
            raise TypeError('Moulder output should be of class Direction')

        resource_op_actual = self._format_op(resource_op_input, Resource, (Essence,))
        essence_op_actual = self._format_op(essence_op_input, Essence, (Resource,))
        inputer_actual = self._format_op(inputer, Belief, (Buzz, Direction, Feature))

        super().__init__(moulder_name, moulder_func,
                         message_input=inputer_actual,
                         message_output=direction,
                         scaffold_map_output=resource_map_output,
                         resource_op_input=resource_op_actual,
                         essence_op_input=essence_op_actual,
                         engine_kwargs=moulder_func_kwargs)

        self.agent_id_to_engine = agent_id_to_engine

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
    resource_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the resource 
        values of the agent calling the instructor
    essence_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the essence
        values of the agent calling the instructor
    agent_id_to_engine : bool, optional
        If True, the agent ID of the calling agent is passed as an argument to
        the cortex function
    cortex_func_kwargs : dict, optional
        Named arguments to the cortex function

    Raises
    ------
    TypeError
        If the `inputer` parameter provides a message of type other than
        Essence, Resource or Belief, or if the `feature` parameter is a 
        message of type other than Feature.

    Notes
    -----
    The engine input parameters are constrained in the following order: First,
    any values from the input agent imprints, second, any resource
    values from the `resource_op_input`, third, any essence values from the
    `essence_op_input`, fourth, any agent ID, last any keyword arguments.

    The engine output parameters are constrained in the following order: First
    and only, any data to populate the output feature..

    '''
    def __call__(self, agent_id):
        '''Execute the cortex to consume input and produce the output

        Parameters
        ----------
        agent_id : str
            The agent ID for the agent whose actuator is executed

        Returns
        -------
        success 
            If execution of engine successful, return value is True. If
            execution of engine created Exception, that Exception is returned     

        '''
        agent_state_values = tuple(self.message_input())
        resource_values = tuple(self.resource_op_input())
        essence_values = tuple(self.essence_op_input())
        args = agent_state_values + resource_values + essence_values

        if self.agent_id_to_engine:
            args += (agent_id,)

        try:
            out_values = self.engine(*args, **self.kwargs)
        except Exception as err:
            return err

        self.message_output.set_values(out_values)

        return True 

    def __init__(self, cortex_name, cortex_func, inputer, feature,
                 resource_op_input=None, essence_op_input=None,
                 agent_id_to_engine=False,
                 cortex_func_kwargs={}):

        if not isinstance(feature, Feature):
            raise TypeError('Cortex output should be of class Feature')

        resource_op_actual = self._format_op(resource_op_input, Resource, (Essence,))
        essence_op_actual = self._format_op(essence_op_input, Essence, (Resource,))
        inputer_actual = self._format_op(inputer, (Essence, Resource, Belief), \
                                                  (Buzz, Direction, Feature))

        super().__init__(cortex_name, cortex_func, 
                         message_input=inputer_actual,
                         message_output=feature,
                         resource_op_input=resource_op_actual,
                         essence_op_input=essence_op_actual,
                         engine_kwargs=cortex_func_kwargs)

        self.agent_id_to_engine = agent_id_to_engine

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
    resource_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the resource 
        values of the agent calling the instructor
    essence_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the essence
        values of the agent calling the instructor
    agent_id_to_engine : bool, optional
        If True, the agent ID of the calling agent is passed as an argument to
        the compulsion function
    compel_func_kwargs : dict, optional
        Named arguments to the compel function

    Raises
    ------
    TypeError
        If the resource map is not an instance of ResourceMap or MapCollection

    Notes
    -----
    The engine input parameters are constrained in the following order: First,
    any resource
    values from the `resource_op_input`, second, any essence values from the
    `essence_op_input`, third, any agent ID, last any keyword arguments.

    The engine output parameters are constrained in the following order: First
    and only, any data to populate the output resource map

    '''
    def __call__(self, agent_id):
        '''Execute the compulsion and populate the output

        Parameters
        ----------
        agent_id : str
            The agent ID for the agent whose actuator is executed

        Returns
        -------
        success 
            If execution of engine successful, return value is True. If
            execution of engine created Exception, that Exception is returned     

        '''
        resource_values = tuple(self.resource_op_input())
        essence_values = tuple(self.essence_op_input())
        args = resource_values + essence_values

        if self.agent_id_to_engine:
            args += (agent_id,)

        try:
            out_values = self.engine(*args, **self.kwargs)
        except Exception as err:
            return err

        self.scaffold_map_output.set_values(out_values)

        return True 

    def __init__(self, compel_name, compel_func, resource_map,
                 resource_op_input=None, essence_op_input=None,
                 agent_id_to_engine=False,
                 compel_func_kwargs={}):

        if not isinstance(resource_map, (ResourceMap, MapCollection)):
            raise TypeError('Compulsion must have a resource map of type ' + \
                            'ResourceMap or MapCollection')

        resource_op_actual = self._format_op(resource_op_input, Resource, (Essence,))
        essence_op_actual = self._format_op(essence_op_input, Essence, (Resource,))

        super().__init__(compel_name, compel_func, 
                         scaffold_map_output=resource_map, 
                         resource_op_input=resource_op_actual,
                         essence_op_input=essence_op_actual,
                         engine_kwargs=compel_func_kwargs)

        self.agent_id_to_engine = agent_id_to_engine

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
    resource_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the resource 
        values of the agent calling the instructor
    essence_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the essence
        values of the agent calling the instructor
    agent_id_to_engine : bool, optional
        If True, the agent ID of the calling agent is passed as an argument to
        the mutation function
    mutation_prob : float, optional
        Probability the mutation engine is executed
    mutate_func_kwargs : dict, optional
        Named arguments to the mutate function

    Raises
    ------
    TypeError
        If the essence map is not an instance of EssenceMap or MapCollection
    ValueError
        If the probability is not between 0.0 and 1.0

    Notes
    -----
    The engine input parameters are constrained in the following order: First,
    any resource
    values from the `resource_op_input`, second, any essence values from the
    `essence_op_input`, third, any agent ID, last any keyword arguments.

    The engine output parameters are constrained in the following order: First
    and only, any data to populate the output essence map

    '''
    def __call__(self, agent_index):
        '''Execute the mutation attempt and populate the output if attempt
        successful

        Parameters
        ----------
        agent_id : str
            The agent ID for the agent whose actuator is executed

        Returns
        -------
        success 
            If execution of engine successful, return value is True. If
            execution of engine created Exception, that Exception is returned.    
            Note that even if mutation attempt did not lead to a mutation, the
            return value is True

        Notes
        -----
        The attempt to mutate is stochastic and of a probability set during
        initialization. If a mutation is made, the engine is applied to all
        arguments of the essence. If mutations should be attempted in sequence
        independently on the essence arguments, use the MultiMutation class

        '''
        if np.random.ranf() < self.mutation_prob:

            resource_values = tuple(self.resource_op_input())
            essence_values = tuple(self.essence_op_input())
            args = resource_values + essence_values

            if self.agent_id_to_engine:
                args += (agent_id,)

            try:
                out_values = self.engine(*args, **self.kwargs)
            except Exception as err:
                return err

            self.scaffold_map_output.set_values(out_values)

        else:
            pass

        return True

    def __init__(self, mutate_name, mutate_func, essence_map,
                 resource_op_input=None, essence_op_input=None,
                 agent_id_to_engine=False,
                 mutation_prob=1.0,
                 mutate_func_kwargs={}):

        if not isinstance(essence_map, (EssenceMap, MapCollection)): 
            raise TypeError('Mutation must have an essence map of type ' + \
                            'EssenceMap or MapCollection')

        resource_op_actual = self._format_op(resource_op_input, Resource, (Essence,))
        essence_op_actual = self._format_op(essence_op_input, Essence, (Resource,))

        super().__init__(mutate_name, mutate_func, 
                         scaffold_map_output=essence_map, 
                         resource_op_input=resource_op_actual,
                         essence_op_input=essence_op_actual,
                         engine_kwargs=mutate_func_kwargs)

        self.agent_id_to_engine = agent_id_to_engine 

        if mutation_prob > 1.0 or mutation_prob < 0.0:
            raise ValueError('Mutation probability must be in range 0.0 to 1.0')
        self.mutation_prob = mutation_prob

class MultiMutation(Mutation):
    '''Multi Mutation class, which defines how the Agent responds to being
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
    resource_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the resource 
        values of the agent calling the instructor
    essence_op_input : MessageOperator, optional
        Operator that when called accesses all or a subset of the essence
        values of the agent calling the instructor
    agent_id_to_engine : bool, optional
        If True, the agent ID of the calling agent is passed as an argument to
        the mutation function
    mutation_prob : float, optional
        Probability the mutation engine is executed
    mutate_func_kwargs : dict, optional
        Named arguments to the mutate function

    Raises
    ------
    TypeError
        If the essence map is not an instance of EssenceMap or MapCollection
    ValueError
        If the probability is not between 0.0 and 1.0

    Notes
    -----
    This is a child class of the Mutation class and only differs in how the
    mutation attemtps are distributed on the essence arguments, see `__call__`

    '''
    def __call__(self, agent_index):
        '''Execute the mutation attempt and populate the output if attempt
        successful

        Parameters
        ----------
        agent_id : str
            The agent ID for the agent whose actuator is executed

        Returns
        -------
        success 
            If execution of engine successful, return value is True. If
            execution of engine created Exception, that Exception is returned.    
            Note that even if mutation attempt did not lead to a mutation, the
            return value is True

        Notes
        -----
        The attempt to mutate is stochastic and of a probability set during
        initialization. If the essence contains multiple arguments a sequence
        of independent attempts to mutate is done, which means some arguments
        may mutate, others may not. If mutation should apply, or not apply, to
        all arguments use the Mutation class.

        '''
        resource_values = tuple(self.resource_op_input())
        essence_values = tuple(self.essence_op_input())
        args = resource_values + essence_values

        if self.agent_id_to_engine:
            args += (agent_id,)

        out_values = []
        for key in self.scaffold_map_output:
            if np.random.ranf() < self.mutation_prob:
                try:
                    out_values.extend(list(self.engine(*args, **self.kwargs)))
                except Exception as err:
                    return err

            else:
                out_values.extend([None] * key.n_elements)

        self.scaffold_map_output.set_values(out_values)

        return True
