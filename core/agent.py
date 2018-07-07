'''Agent 

'''
import numpy as np
import numpy.random

import random
from collections import namedtuple

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
        return self.service.keys() 

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
            func = self.service[request_type]

        try:
            outcome = func(**kwargs)
        except Exception:
            return NULL_RETURN

        return (outcome, True)

    def request_service(self, service_name, kwargs={}):
        '''Public method for external agents to request present agent to supply
        some service as specified by the `service_label`.

        Notes
        -----
            Formally the method returns a function that has been decorated with
            a model of capricious behaviour on part of the agent.

        Parameters
        ----------
        service_name : str
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
        return request_runner(service_name, kwargs)

    def _sense(self, precept, kwargs={}):
        '''Method for agent to sense a precept of the environment. The method
        should only be called by the agent itself

        Parameters
        ----------
        precept : str
            Label for the precept to be sensed
        kwargs : dict
            Arguments to the sensor function passed at runtime

        Returns
        -------
        outcome
            Variable with data returned from the sensor

        Raises
        ------
        RuntimeError
            If no sensor is associated with the provided precept

        '''
        if not precept in self.sensor:
            raise RuntimeError('Agent lacks sensor for precept %s' %(precept))

        else:
            the_sensor = self.sensor[precept]

        outcome = the_sensor(**kwargs)

        return outcome

    # ABSTRACT AGENT PROPERTIES SUCH THAT SCALAR VALUES ARE LIKE CALLABLE
    def set_nature(self, entry, new_value):
        '''Bla bla

        '''
        self.nature[entry] = new_value

    def set_belief(self, about_what, new_belief):
        '''Bla bla

        '''
        self.belief[about_what] = new_belief

    def set_natural_constraint(self, about_what, enumeration=None,
                              lower_bound=None, upper_bound=None):
        '''Bla bla

        '''
        if not (enumeration is None):
            self.natural_constraint[about_what] = enumeration

        elif (not (lower_bound is None)) or (not (upper_bound is None)):
            self.natural_constraint[about_what] = (lower_bound, upper_bound) 

        #elif unbiased generator function

        else:
            raise RuntimeError('Natural constraint invalidly defined')

    def set_service(self, service_name, service_function):
        '''Bla bla

        '''
        self._set_exec('service', service_name, service_function)

    def set_sensor(self, precept, sensor_function):
        '''Bla bla

        '''
        self._set_exec('sensor', precept, sensor_function)

    def set_plan(self, plan_name, plan_function):
        '''Bla bla

        '''
        self._set_exec('plan', plan_name, plan_function)

    def set_actuator(self, action, actuator_function):
        '''Bla bla

        '''
        self._set_exec('actuator', action, actuator_function)

    def _set_exec(self, agent_property, name, func):
        '''Bla bla

        '''
        if not callable(func):
            raise RuntimeError('Attempt to set non-callable object')

        container = getattr(self, agent_property)
        container[name] = func
        setattr(self, agent_property, container)

    def __call__(self, kwargs={}):
        '''Bla bla

        '''
        the_plan = random.choice(list(self.plan.values()))
        the_plan(**kwargs)

    def __init__(self, name):

        self.name = name
        self.agent_id_system = None

        self.capricious_decorator = Capriciousness(style_type='always_comply')

        self.belief = {} 
        self.goal = None
        self.plan = {}
        self.sensor = {} 
        self.actuator = {}
        self.service = {}
        self.nature = {} 
        self.natural_constraint = {}

        self.set_service('list_my_services', self._request_service_labels)
