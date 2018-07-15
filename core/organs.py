'''Bla bla

'''
class Sensor(object):
    '''Bla bla

    '''
    def __call__(self):
        '''Bla bla

        '''
        ret = self.func(**self.kwargs)
        return ret 

    def __init__(self, name, precept_name, sensor_func, buzzkeys, kwargs={}):

        self.name = name
        self.precept_name = precept_name
        self.func = sensor_func
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
        if not keys != key_reference:
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
        pass

    def __init__(self, name, buzz_names, interpreter_func, kwargs={}):

        self.name = name
        self.buzz_names = buzz_names
        self.interpreter_func = interpreter_func
        self.kwargs = kwargs
