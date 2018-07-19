'''Agent 

'''
import random

from core.organs import Sensor, Actuator, Interpreter, Moulder, Cortex

class Agent(object):
    '''Bla bla

    '''
    def _tickle_cortex_labels(self):
        '''Mandatory cortex function of agent to reveal all cortex labels.

        Returns
        -------
        keys : list
            List of unadulterated string keys for the cortex functions of the agent.

        '''
        return self.cortex.keys() 

    def _set(self, object_type, key, value):
        '''Common function to add agent organ or data to the appropriate
        attribute container.

        Notes
        -----
        Only intended to be used within the Agent class.

        Parameters
        ----------
        object_type : str
            Type of organ or data
        key : str
            Key for the particular organ or data
        value 
            The object of the particular organ or data, such as float or
            callable functions

        Raises
        ------
        AttributeError
            If the `object_type` does not map onto a container

        '''
        try:
            container = getattr(self, object_type)
        except AttributeError:
            raise AttributeError('Agent lacks container for %s' %(object_type))

        container[key] = value
        setattr(self, object_type, container)

    def set_data(self, data, entry_name, entry):
        '''Set data... more details TBD

        '''
        if callable(entry):
            raise RuntimeError('Attempt to set data to callable object')
        else:
            self._set(data, entry_name, entry)

    def set_organ(self, organ):
        '''Add an organ to the agent.

        Parameters
        ----------
        organ
            The organ class instance to add to the agent. The organ must be one
            of the known organ classes

        Raises
        ------
        TypeError
            If the `organ` that is given as input is not an instance of a known
            organ class

        '''
        if isinstance(organ, Sensor):
            self._set('sensor', organ.precept_name, organ)

        elif isinstance(organ, Actuator):
            self._set('actuator', organ.action_name, organ)

        elif isinstance(organ, Interpreter):
            self._set('interpreter', organ.name, organ)

        elif isinstance(organ, Moulder):
            self._set('moulder', organ.name, organ) 

        elif isinstance(organ, Cortex):
            self._set('cortex', organ.tickle_name, organ)

        else:
            raise TypeError('Unknown organ type: %s' %str(type(organ)))

    def tickle(self, itch):
        '''Method to tickle the cortex of the agent

        Notes
        -----
        The cortex is intended to be tickled by an external agent to the
        current agent. Therefore, `tickle` is intended as a public method.

        Parameters
        ----------
        itch : str
            Name for the itch that is tickled of the agent cortex

        Returns
        -------
        reaction
            The return value from the cortex.

        Raises
        ------
        KeyError
            If an itch is tickled that is not defined for the cortex

        '''
        if not itch in self.cortex:
            raise KeyError('Agent lacks cortex for itch %s' %(itch))

        else:
            the_cortex = self.cortex[itch]

        reaction = the_cortex()

        return reaction 

    def sense(self, precept):
        '''Method for agent to sense a precept of the environment. 

        Notes
        -----
        The sensor is intended to sense a precept of the World wherein the
        method is intended as a private method to the current agent.

        Parameters
        ----------
        precept : str
            Name of the precept of the World to sense

        Returns
        -------
        buzz : dict
            Buzz that the sensor triggers once it senses the precept

        Raises
        ------
        KeyError
            If a precept is sensed that is not defined for the sensor

        '''
        if not precept in self.sensor:
            raise KeyError('Agent lacks sensor for precept %s' %(precept))

        else:
            the_sensor = self.sensor[precept]

        buzz = the_sensor()

        return buzz 

    def interpret(self, brain_tissue, buzz):
        '''Method for agent to interpret a buzz with certain brain tissue

        Notes
        -----
        The particular interpreter brain tissue interprets a buzz
        triggered by sensor wherein the method is intended as a private method
        to the current agent.

        Parameters
        ----------
        brain_tissue : str
            The name of the interpreter to be used
        buzz : dict
            The buzz to interpret with the `brain_tissue` interpreter

        Returns
        -------
        updated_belief_labels
            Iterable with labels of updated beliefs following interpretation

        Raises
        ------
        KeyError
            If a brain tissue is used that is not defined for the interpreter

        '''
        if not brain_tissue in self.interpreter:
            raise KeyError('Agent lacks interpreter %s' %(brain_tissue))

        else:
            the_interpreter = self.interpreter[brain_tissue]

        updated_belief_labels = the_interpreter(buzz)

        return updated_belief_labels

    def mould(self, action):
        '''Method for agent to mould beliefs into an action

        Notes
        -----
        The desired action is moulded from a number of given beliefs wherein
        the method is intended as a private method to the current agent.
        The beliefs to be used are defined as part of initilization of the
        organ.

        Parameters
        ----------
        actions : str
            Name of the action onto the World to mould

        Returns
        -------
        actuators
            Iterable of actuator instances that once executed in the World
            generates the specified action

        Raises
        ------
        KeyError
            If an action is requested for which agent has no moulder

        '''
        if not action in self.moulder:
            raise KeyError('Agent lacks moulder for action %s' %(action))

        else:
            the_moulder = self.moulder[action]

        the_moulder(self.actuator[action], self.belief)

    def act(self, action):
        '''Bla bla

        '''
        if not action in self.actuator:
            raise KeyError('Agent lacks actuator for action %s' %(action))

        else:
            the_actuator = self.actuator[action]

        the_actuator()

    def __str__(self):

        return self.name + '(ID:%s)'%(str(self.agent_id_system))

    def __call__(self):
        '''Method to call agent invokes the executive function. This should be
        defined in specific classes that uses the present class as parent.

        '''
        raise RuntimeError('Basic Agent class has not executive function. ' + \
                           'That should be implemented in specific agent classes.')

    def __init__(self, name):

        self.name = name
        self.agent_id_system = None

        self.scaffold = {}
        self.belief = {}
        self.data = {'scaffold' : self.scaffold, 
                     'belief' : self.belief}

        self.cortex = {}
        self.sensor = {}
        self.actuator = {}
        self.interpreter = {}
        self.moulder = {}
        self.organs = {'cortex' : self.cortex, 
                       'sensor' : self.sensor,
                       'actuator' : self.actuator, 
                       'interpreter' : self.interpreter,
                       'moulder' : self.moulder}

        cortex = Cortex('revealation_set', 'cortex_labels', self._tickle_cortex_labels)
        self.set_organ(cortex)

