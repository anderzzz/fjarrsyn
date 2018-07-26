'''All organ classes of the basic Agent are contained in this file.

'''
from core.objectforce import ObjectForce

class Organ(object):

    def __init__(self):
        # MAKE THIS PARENT TO ALL ORGANS
        pass

class Sensor(object):
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
    def __str__(self):
        '''Print string for sensor object

        '''
        ret = 'Sensor %s for precept %s.' %(self.name, self.precept_name)
        return ret

    def __call__(self):
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
        ret = self.sensor_func(**self.kwargs)

        if set(ret.keys()) != set(self.buzzkeys):
            raise ValueError('Sensor function generated unexpected buzz keys')

        return ret 

    def __init__(self, name, precept_name, sensor_func, buzzkeys, kwargs={}):

        self.name = name
        self.precept_name = precept_name
        self.sensor_func = sensor_func
        self.buzzkeys = buzzkeys
        self.kwargs = kwargs

class Actuator(object):
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
    def populate(self, keyvalue):
        '''Populate the actuator (form) with action parameter values (content).

        Parameters
        ----------
        keyvalue : dict
            Dictionary with values to populate named parameters. The input is
            typically obtained from a Moulder organ.

        Raises
        ------
        ValueError
            If the keys in the input `keyvalue` differs from the list of
            parameter names defined during initialization.

        '''
        self.kwargs = {'agent_index' : self.agent_index}

        keys = set(keyvalue.keys())
        key_reference = set(self.keys2populate)
        if keys != key_reference:
            raise ValueError('Keys to actuator not identical to ' + \
                             'reference list set on initialization')

        for key, value in keyvalue.items():
            self.kwargs[key] = value

    def depopulate(self):
        '''Depopulate a specific actuator to be pure form, no content.

        Notes
        -----
        This is typically used after a specific actuator has been excecuted in
        order to ensure proper accounting by requiring the mould method to
        precede any single action.

        '''
        self.kwargs = None

    def __call__(self):
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
        if self.kwargs is None:
            raise RuntimeError('Actuator called prior to population')

        reaction = self.actuator_func(**self.kwargs)

        if not reaction is None:
            if not isinstance(reaction, ObjectForce):
                raise TypeError('Actuator organ is only allowed to return ' + \
                                'instance of ObjectForce')

        return reaction

    def __init__(self, name, action_name, actuator_func, keys2populate,
                 agent_index):

        self.name = name
        self.action_name = action_name
        self.actuator_func = actuator_func
        self.keys2populate = keys2populate
        self.agent_index = agent_index

        self.kwargs = None

class Interpreter(object):
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
    def __call__(self, buzz):
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
        func_kwargs = {}
        for buzz_input in self.buzz_names:
            func_kwargs[buzz_input] = buzz[buzz_input]

        for kwarg, value in self.kwargs.items():
            func_kwargs[kwarg] = value

        return self.interpreter_func(**func_kwargs) 

    def __init__(self, name, buzz_names, interpreter_func, kwargs={}):

        self.name = name
        self.buzz_names = buzz_names
        self.interpreter_func = interpreter_func
        self.kwargs = kwargs

class Moulder(object):
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
    def __call__(self, actuator, belief):
        '''Execute the moulder to populate an actuator

        Notes
        -----
        After excecution of the moulder the actuator can be executed. Prior to
        moulding the actuator is form without content.

        Parameters
        ----------
        actuator
            The actuator instance to populate
        belief : dict
            Dictionary of belief values, at least a subset of which overlaps
            with the belief names defined during initialization

        '''
        func_kwargs = {}
        for belief_input in self.belief_names:
            func_kwargs[belief_input] = belief[belief_input]

        for kwarg, value in self.kwargs.items():
            func_kwargs[kwarg] = value

        actuator_params = self.moulder_func(**func_kwargs)
        actuator.populate(actuator_params)

    def __init__(self, name, belief_names, moulder_func, kwargs={}):

        self.name = name
        self.belief_names = belief_names
        self.moulder_func = moulder_func
        self.kwargs = kwargs

class Cortex(object):
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
        return self.cortex_func(**self.kwargs)

    def __init__(self, name, tickle_name, cortex_func, kwargs={}):

        self.name = name
        self.tickle_name = tickle_name
        self.cortex_func = cortex_func
        self.kwargs = kwargs
