'''Agent 

'''
class State(object):
    '''Bla bla

    '''
    def append(self, key, value):
        '''Bla bla

        '''

    def set_vector(self, vector):
        '''Bla bla

        '''
        self.state_vector = vector

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
        return self.state_vector.items()

    def __init__(self):

        self.state_vector = {} 

ALWAYS_COMPLY = True

class Agent(object):
    '''Bla bla

    '''
    def set_internal_state(self, state_vector)
        '''Bla bla

        '''
        self.internal_state.set_vector(state_vector)

    def set_signaled_state(self, state_vector)
        '''Bla bla

        '''
        self.signaled_state.set_vector(state_vector)

    def set_request_services(self, service_label, service_method,
                             service_method_kwargs=None, overwrite=False):
        '''Bla bla

        '''
        if service_label in self.request_services:
            if overwrite:
                self.request_services[service_label] = 
                    (service_method, service_method_kwargs)
            else:
                raise RuntimeError('Agent request method overwrite of %s ' + \
                                   'not authorized' %(service_label))
        else:
            self.request_services[service_label] = 
                (service_method, service_method_kwargs)

    def request_comply(self):
        '''Bla bla

        '''
        return ALWAYS_COMPLY
            
    # REQUEST HANDLING SHOULD BE A DECORATOR
    def request(self, request_type):
        '''Bla bla

        '''
        if not request_type in self.request_services:
            return (None, False)

        if not self.request_comply():
            return (None, False)

        (func, kwargs) = self.request_services[request_type]
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

