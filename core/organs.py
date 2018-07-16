'''All organ classes of the basic Agent are contained in this file.

'''
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
    '''Bla bla

    '''
    def populate(self, keyvalue):
        '''Bla bla

        '''
        self.kwargs = {'agent_index' : self.agent_index}

        keys = set(keyvalue.keys())
        key_reference = set(self.keys2populate)
        if keys != key_reference:
            raise RuntimeError('Keys to actuator not identical to ' + \
                               'reference list set on initialization')

        for key, value in keyvalue.items():
            self.kwargs[key] = value

    def __call__(self):
        '''Bla bla

        '''
        if self.kwargs is None:
            raise RuntimeError('Actuator called prior to population')

        self.actuator_func(**self.kwargs)

    def __init__(self, name, action_name, actuator_func, keys2populate,
                 agent_index):

        self.name = name
        self.action_name = action_name
        self.actuator_func = actuator_func
        self.keys2populate = keys2populate
        self.agent_index = agent_index

        self.kwargs = None

class Interpreter(object):
    '''Bla bla

    '''
    def __call__(self, buzz):
        '''Bla bla

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
    '''Bla bla

    '''
    def __call__(self, beliefs, actuator):
        '''Bla bla

        '''
        func_kwargs = {}
        for belief_input in self.belief_names:
            func_kwargs[belief_input] = beliefs[belief_input]

        for kwarg, value in self.kwargs.items():
            func_kwargs[kwarg] = value

        actuator_params = self.moulder_func(**func_kwargs)

        ret = actuator.populate(actuator_params)

        return ret

    def __init__(self, name, belief_names, moulder_func, kwargs={}):

        self.name = name
        self.belief_names = belief_names
        self.moulder_func = moulder_func
        self.kwargs = kwargs

class Cortex(object):
    '''Bla bla

    '''
    def __call__(self):
        '''Bla bla

        '''
        return self.cortex_func(**self.kwargs)

    def __init__(self, name, tickle_name, cortex_func, kwargs={}):

        self.name = name
        self.tickle_name = tickle_name
        self.cortex_func = cortex_func
        self.kwargs = kwargs
