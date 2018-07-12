'''Agent 

'''
import random

NULL_RETURN = (None, False) 

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

    def _set(self, object_type, key, value):
        '''Bla bla

        '''
        try:
            container = getattr(self, object_type)
        except AttributeError:
            raise RuntimeError('Agent lacks %s' %(object_type))

        container[key] = value
        setattr(self, object_type, container)

    def _setter(self, object_type, key, value):
        '''Bla bla

        '''
        def ret():
            self._set(object_type, key, value)

        return ret

    def set_data(self, data, entry_name, entry):
        '''Bla bla

        '''
        if callable(entry):
            raise RuntimeError('Attempt to set data to callable object')
        else:
            self._set(data, entry_name, entry)

    def set_organ(self, organ, func_name, func):
        '''Bla bla

        '''
        if not callable(func):
            raise RuntimeError('Attempt to set organ to non-callable object')
        else:
            self._set(organ, func_name, func)

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
        if not service_name in self._request_service_labels():
            return NULL_RETURN

        else:
            func = self.service[service_name]

        try:
            outcome = func(**kwargs)
        except Exception:
            return NULL_RETURN

        return (outcome, True)

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

    def interpret(self, what, kwargs={}):
        '''Bla bla

        '''
        if not what in self.interpreter:
            raise RuntimeError('Agent lacks interpreter for %s' %(what))

        else:
            the_interpreter = self.interpreter[what]

        updated_beliefs = the_interpreter(**kwargs)

        return updated_beliefs

    def handle(self, target, kwargs={}):
        '''Bla bla

        '''
        if not target in self.handler:
            raise RuntimeError('Agent lacks handler for %s' %(target))

        else:
            the_handler = self.handler[target]

        actuators = the_handler(**kwargs)

        return actuators

    def __str__(self):

        return self.name + '(ID:%s)'%(str(self.agent_id_system))

    def __init__(self, name):

        self.name = name
        self.agent_id_system = None

        self.scaffold = {}
        self.belief = {}
        self.data = {'scaffold' : self.scaffold, 'belief' : self.belief}

        self.service = {}
        self.sensor = {}
        self.actuator = {}
        self.interpreter = {}
        self.handler = {}
        self.organs = {'service' : self.service, 
                       'sensor' : self.sensor,
                       'actuator' : self.actuator, 
                       'interpreter' : self.interpreter,
                       'handler' : self.handler}

        self.set_organ('service', 'list_my_services', self._request_service_labels)

