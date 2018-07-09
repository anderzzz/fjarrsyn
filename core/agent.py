'''Agent 

'''
NULL_RETURN = (None, False) 

class _Agent(object):
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

    def __str__(self):

        return self.name + '(ID:%s)'%(str(self.agent_id_system))

    def __init__(self, name):

        self.name = name
        self.agent_id_system = None

        self.scaffold = {}

        self.service = {}
        self.plan = {}
        self.reformer = {}

        self.organs = {'service' : self.service, 'plan' : self.plan, 
                       'reformer' : self.reformer}
        self.data = {'scaffold' : self.scaffold}

        self.set_organ('service', 'list_my_services', self._request_service_labels)

class EngagedAgent(_Agent):
    '''Bla bla

    '''
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

    def __init__(self, name):

        super().__init__(name)

        self.belief = {}

        self.sensor = {}
        self.actuator = {}

        self.data['belief'] = self.belief
        self.organs['sensor'] = self.sensor
        self.organs['actuator'] = self.actuator

class PassiveAgent(_Agent):
    '''Bla bla

    '''
    def __init__(self, name):

        super().__init__(name)

