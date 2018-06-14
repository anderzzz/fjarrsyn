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
    def _request_feature_labels(self):
        '''Bla bla

        '''
        return self.features.keys() 

    def _request_general(self, request_type, kwargs={}):
        '''Bla bla

        '''
        if not request_type in self._request_feature_labels():
            return NULL_RETURN

        func = self.request_services[request_type]
        outcome = func(**kwargs)

        return (outcome, True)

    def request_feature(self, request_type, kwargs={}):
        '''Bla bla

        '''
        request_runner = self.capricious_decorator(self._request_general)
        return request_runner(request_type, kwargs)

    def set_feature(self, feature_label, feature_method, overwrite=False):
        '''Bla bla

        '''
        if feature_label in self._request_feature_labels():
            if overwrite:
                self.features[feature_label] = feature_method
            else:
                raise RuntimeError('Agent request method overwrite of %s ' + \
                                   'not authorized' %(service_label))
        else:
            self.features[feature_label] = feature_method

    def __init__(self, name):

        self.name = name
        self.capricious_decorator = Capriciousness(style_type='always_comply')

        self.internal_state = State()
        self.signaled_state = State()

        self.belief = None
        self.plan = None
        self.sensors = None
        self.actuators = None
        self.features = {'list_my_features': self._request_feature_labels}

