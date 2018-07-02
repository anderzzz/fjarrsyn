'''Agent 

'''
import numpy as np
import numpy.random

from collections import namedtuple

class State(object):
    '''Bla bla

    '''
    def __setitem__(self, key, value):
        '''Bla bla

        '''
        self.state_vector[key] = value

    def __getitem__(self, key):
        '''Bla bla

        '''
        return self.state_vector[key]

    def __iter__(self):
        '''Bla bla

        '''
        return self.state_vector.keys()

    def __contains__(self, item):
        '''Bla bla

        '''
        ret_bool = item in self.state_vector.keys()
        return ret_bool

    def __init__(self):

        self.state_vector = {} 

NULL_RETURN = (None, False) 

class Capriciousness(object):
    '''Bla bla

    '''
    def always_comply(self):
        '''Bla bla

        '''
        return True 

    def never_comply(self):
        '''Bla bla

        '''
        return False 

    def fault_bernoulli(self):
        '''Bla bla

        '''
        s = np.random.binomial(1, self.p_fault)
        if not s > 0:
            return True
        else:
            return False

    def __call__(self, f):
        '''Decorator caller

        '''
        def wrapped_f(*args):
            if self.style_func():
                return f(*args)
            else:
                return NULL_RETURN
        return wrapped_f

    def __init__(self, style_type='always_comply', p_fault=0.0):

        self.style_type = style_type
        self.p_fault = p_fault
        self.style_func = getattr(self, self.style_type)

class Agent(object):
    '''Bla bla

    '''
    def _request_service_labels(self):
        '''Bla bla

        '''
        return self.services.keys() 

    def _request_general(self, request_type, kwargs={}):
        '''Bla bla

        '''
        if not request_type in self._request_service_labels():
            return NULL_RETURN

        func = self.services[request_type]
        outcome = func(**kwargs)

        return (outcome, True)

    def request_service(self, request_type, kwargs={}):
        '''Bla bla

        '''
        request_runner = self.capricious_decorator(self._request_general)
        return request_runner(request_type, kwargs)

    def set_service(self, service_label, service_method, overwrite=False):
        '''Bla bla

        '''
        if service_label in self._request_service_labels():
            if overwrite:
                self.services[service_label] = service_method
            else:
                raise RuntimeError('Agent request method overwrite of %s ' + \
                                   'not authorized' %(service_label))
        else:
            self.services[service_label] = service_method

    # FIX: SENSOR CALL INTEGRATE WITH SERVICE CALL
    def _request_sensor(self, sensor_type, kwargs={}):
        '''Bla bla

        '''
        func = self.sensors[sensor_type]
        outcome = func(**kwargs)

        return (outcome, True)

    def request_sensor(self, sensor_type, kwargs={}):
        '''Bla bla

        '''
        request_runner = self.capricious_decorator(self._request_sensor)
        return request_runner(sensor_type, kwargs)

    def _update_dict(self, dict_name, entry, new_v=None, v_diff=None):
        '''Bla bla

        '''
        ddd = getattr(self, dict_name)

        if not (v_diff is None):
            if not entry in ddd.keys():
                raise KeyError('Unable to find %s for agent %s' %(entry, self.name))

            else:
                x_old = ddd[entry] 
                x_new = x_old + value_diff
                ddd[entry] = x_new

        elif not (new_v is None):
            ddd[entry] = new_v

        else:
            raise RuntimeError('Update of agent %s attempted without value')

    def update_database(self, entry, new_value=None, value_diff=None):
        '''Bla bla

        '''
        self._update_dict('database', entry, new_value, value_diff)

    def update_belief(self, about_what, new_belief=None, belief_diff=None):
        '''Bla bla

        '''
        self._update_dict('belief', about_what, new_belief, belief_diff)

    def update_sensor(self, precept, sensor_function, sensor_function_kwargs={}):
        '''Bla bla

        '''
        self._update_dict('sensors', precept, 
                          (sensor_function, sensor_function_kwargs))

    def __init__(self, name):

        self.name = name
        self.agent_id_system = None

        self.capricious_decorator = Capriciousness(style_type='always_comply')

        self.internal_state = State()
        self.signaled_state = State()

        self.belief = {} 
        self.goal = None
        self.plan = None
        self.sensors = {} 
        self.actuators = {}
        self.services = {'list_my_services': self._request_service_labels}
        self.database = {} 

