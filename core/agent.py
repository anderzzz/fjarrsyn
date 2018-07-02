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
        '''Method for the mandatory service for an agent to announce labels for
        its requestable services.

        Notes
        -----
            This method should not be accessed directly, only through the
            `request_service` method should this method be executed.

        Returns
        -------
        service_labels : set
            Service labels for requestable services by the agent

        '''
        return self.services.keys() 

    def _request_root(self, request_type, kwargs={}):
        '''The method that executes the request of service. The method should
        not be called directly but accessed via `request_service`.

        Notes
        -----
            The method has multiple return points, including a very general
            exception handling, such that an external agent providing a bad
            request does not force the agent to break. In these circumstances a
            `NULL_RETURN` is returned of identical format as the other return.

        Parameters
        ----------
        request_type : str
            The label for the service that is requested
        kwargs : dict, optional
            Optional dictionary of arguments to be passed onto the service
            method

        Returns
        -------
        outcome 
            Return variable containing the outcome of the requested service
        performed_service : bool
            Variable that indicates if the service was executed or denied for
            some reason by the agent

        '''
        if not request_type in self._request_service_labels():
            return NULL_RETURN

        else:
            func = self.services[request_type]

        try:
            outcome = func(**kwargs)
        except Exception:
            return NULL_RETURN

        return (outcome, True)

    def request_service(self, service_label, kwargs={}):
        '''Public method for external agents to request present agent to supply
        some service as specified by the `service_label`.

        Notes
        -----
            Formally the method returns a function that has been decorated with
            a model of capricious behaviour on part of the agent.

        Parameters
        ----------
        service_label : str
            String label for the service that is requested
        kwargs : dict, optional
            Optional dictionary of arguments to be passed onto the service
            method

        Returns
        -------
        outcome 
            Return variable containing the outcome of the requested service
        performed_service : bool
            Variable that indicates if the service was executed or denied for
            some reason by the agent

        '''
        request_runner = self.capricious_decorator(self._request_root)
        return request_runner(service_label, kwargs)

    def add_service(self, service_label, service_method, overwrite=False):
        '''Add service method and associate it to a service label that can be
        requested by an external agent

        Parameters
        ----------
        service_label : str
            The label of the service that the agent is imbued with
        service_method : function
            An executable function that executes the agent service
        overwrite : bool, optional
            If a service method already exists with the given label the
            overwriting only takes place if this Boolean is True

        '''
        if service_label in self._request_service_labels():
            if overwrite:
                self.services[service_label] = service_method
            else:
                raise RuntimeError('Agent request method overwrite of %s ' + \
                                   'not authorized' %(service_label))
        else:
            self.services[service_label] = service_method

    def _sense(self, precept):
        '''Method for agent to sense a precept of the environment. The method
        should only be called by the agent itself

        Parameters
        ----------
        precept : str
            Label for the precept to be sensed

        Returns
        -------
        outcome
            Variable with data returned from the sensor

        Raises
        ------
        RuntimeError
            If no sensor is associated with the provided precept

        '''
        if not precept in self.sensors:
            raise RuntimeError('Agent lacks sensor for precept %s' %(precept))

        else:
            (sensor_func, sensor_func_kwargs) = self.sensors[precept]

        outcome = sensor_func(**sensor_func_kwargs)

        return outcome

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

