'''Agent 

'''
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

    def __call__(self, f):
        '''Decorator caller

        '''
        def wrapped_f(*args):
            if self.style_func():
                return f(*args)
            else:
                return NULL_RETURN
        return wrapped_f

    def __init__(self, style_type='always_comply'):

        self.style_type = style_type
        self.style_func = getattr(self, self.style_type)

class Agent(object):
    '''Bla bla

    '''
    def set_request_services(self, service_label, service_method, overwrite=False):
        '''Bla bla

        '''
        if service_label in self.request_services:
            if overwrite:
                self.request_services[service_label] = service_method
            else:
                raise RuntimeError('Agent request method overwrite of %s ' + \
                                   'not authorized' %(service_label))
        else:
            self.request_services[service_label] = service_method

    @Capriciousness()
    def request(self, request_type, kwargs={}):
        '''Bla bla

        '''
        if not request_type in self.request_services:
            return NULL_RETURN

        func = self.request_services[request_type]
        outcome = func(**kwargs)

        return (outcome, True)


    def __init__(self, name):

        self.name = name

        self.internal_state = State()
        self.signaled_state = State()

        self.external_view = None

        self.utility_engine = None
        self.action_selector = None
        
        self.request_services = {}

