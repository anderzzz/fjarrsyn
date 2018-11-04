'''The fundamental Agent parent class

'''
from core.organs import Sensor, Actuator, Interpreter, Moulder, Cortex
from core.array import Resource, Essence, Feature

class Agent(object):
    '''The parent Agent class. In applications a custom agent class is created,
    which inherits the current class.

    Notes
    -----
    The parent agent can be initialized as an almost empty template, where only
    the name is required. All content of the Agent, such as organs, messages,
    scaffolds, are added after initialization with the appropriate set-methods.

    Parameters
    ----------
    name : str
        Name of the agent

    '''
    def _tickle_cortex_labels(self):
        '''Mandatory cortex function of agent to reveal all cortex labels.

        Returns
        -------
        keys : list
            List of unadulterated string keys for the cortex functions of the agent.

        '''
        return (list(self.cortex.keys()),)

    def _set(self, object_type, key, value, key_check=False):
        '''Common function to add agent organ or imprint to the appropriate
        attribute container.

        Notes
        -----
        Only intended to be used within the Agent class.

        Parameters
        ----------
        object_type : str
            Type of organ or imprint 
        key : str
            Key for the particular organ or imprint 
        value 
            The object of the particular organ or imprint, such as float or
            callable functions
        key_check : bool
            If True enforces that `key` already exists in container, if False
            `key` does not have to exist.

        Raises
        ------
        AttributeError
            If the `object_type` does not map onto a container
        KeyError
            If the `key` is missing from the container

        '''
        try:
            container = getattr(self, object_type)
        except AttributeError:
            raise AttributeError('Agent lacks container for %s' %(object_type))

        if key_check and (not key in container):
            raise KeyError('Agent container lacks key %s' %(key))

        container[key] = value
        setattr(self, object_type, container)

    def set_scaffold(self, scaffold):
        '''Add an imprint to the agent 

        '''
        if isinstance(scaffold, Resource):
            self.resource = scaffold

        elif isinstance(scaffold, Essence):
            self.essence = scaffold

        else:
            raise TypeError('Agent scaffold should be instance of ' + \
                            'class Resource or Essence')

    def set_scaffold_bulk(self, scaffold, entryvalue, edit_only=False):
        '''Add several imprints to the agent at once

        Parameters
        ----------
        imprint : str
            Type of imprint to set
        entryvalue : dict
            The dictionary of entry name keys and corresponding value.
            The value should be a number, string or similar atomic variable, 
            not a callable function
        edit_only : bool, optional
            If False, `entry_name` can be non-existent in the particular
            imprint, if True, `entry_name` must exist already. Hence, this flag
            validates if imprints can be only edited or not.
        
        '''
        for key, value in entryvalue.items():
            self.set_scaffold(scaffold, key, value, edit_only)

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
            self._set('sensor', organ.name, organ)
            self._set('buzz', organ.array_output.array_name, organ.array_output)

        elif isinstance(organ, Actuator):
            self._set('actuator', organ.name, organ)

        elif isinstance(organ, Interpreter):
            self._set('interpreter', organ.name, organ)
            self._set('belief', organ.array_output.array_name, organ.array_output)

        elif isinstance(organ, Moulder):
            self._set('moulder', organ.name, organ) 
            self._set('direction', organ.array_output.array_name,
                                   organ.array_output)

        elif isinstance(organ, Cortex):
            self._set('cortex', organ.name, organ)
            self._set('feature', organ.array_output.array_name,
                                 organ.array_output)

        else:
            raise TypeError('Unknown organ type: %s' %str(type(organ)))

    def set_organ_bulk(self, organs):
        '''Add organs to the agent

        Parameters
        ----------
        organs
            Container of elements of the organ class instance to add to 
            the agent in bulk. The organ must be one of the known organ classes

        '''
        for organ in organs:
            self.set_organ(organ)

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

        Parameters
        ----------
        precept : str
            Name of the precept of the World to sense

        Raises
        ------
        KeyError
            If a precept is sensed that is not defined for the sensor

        '''
        if not precept in self.sensor:
            raise KeyError('Agent lacks sensor for precept %s' %(precept))

        else:
            the_sensor = self.sensor[precept]

        did_it_sense = the_sensor(self.agent_id_system)

        if not the_sensor.resource_map is None:
            if not the_sensor.resource_map.is_empty():
                the_sensor.resource_map.apply_to(self)

    def interpret(self, state):
        '''Method for agent to interpret state of the world

        Notes
        -----

        Parameters
        ----------
        state : str
            The name of the interpreter to be used

        Raises
        ------
        KeyError
            If a brain tissue is used that is not defined for the interpreter

        '''
        if not state in self.interpreter:
            raise KeyError('Agent lacks interpreter for state %s' %(state))

        else:
            the_interpreter = self.interpreter[state]

        did_it_interpret = the_interpreter()

        if not the_interpreter.resource_map is None:
            if not the_interpreter.resource_map.is_empty():
                the_interpreter.resource_map.apply_to(self)

    def perceive(self, precept, brain_tissue):
        '''Method for agent to sense and interpret a percept

        Notes
        -----
        This is a convenience method that combines `sense` and `interpret` methods
        since these two methods are mostly executed directly after each other.

        Parameters
        ----------
        precept : str
            The name of the external precept to sense
        brain_tissue : str
            The name of the interpreter to be used

        Returns
        -------
        updated_belief_labels
            Iterable with labels of updated beliefs following interpretation. 

        '''
        return self.interpret(brain_tissue, self.sense(precept))

    def mould(self, potential):
        '''Method for agent to mould beliefs into a populated actuator that
        subsequently can be acted upon

        Notes
        -----

        Parameters
        ----------
        potential: str
            Name of the potential to mould

        Raises
        ------
        KeyError
            If a potential is requested for which agent has no moulder

        '''
        if not potential in self.moulder:
            raise KeyError('Agent lacks moulder for %s' %(potential))

        else:
            the_moulder = self.moulder[potential]

        did_it_mould = the_moulder()

        if not the_moulder.resource_map is None:
            if not the_moulder.resource_map.is_empty():
                the_moulder.resource_map.apply_to(self)

    def act(self, action):
        '''Method for agent to act a populated actuator.

        Notes
        -----

        Parameters
        ----------
        actions : str
            Name of the action onto the World to act on

        Raises
        ------
        KeyError
            If an action is requested for which the agent has no actuator

        '''
        if not action in self.actuator:
            raise KeyError('Agent lacks actuator for %s' %(action))

        else:
            the_actuator = self.actuator[action]

        did_it_act = the_actuator(self.agent_id_system)

        if not the_actuator.resource_map is None:
            if not the_actuator.resource_map.is_empty():
                the_actuator.resource_map.apply_to(self)

    def engage(self, action):
        '''Method for agent to mould and act an action

        Notes
        -----
        This is a convenience method that combines `mould` and `act` methods
        since these two methods are mostly executed directly after each other.

        Parameters
        ----------
        action : str
            Name of the action onto the World to mould and act on

        '''
        self.mould(action)
        self.act(action)

    def hooked_up(self):
        '''Determines if agent is part of an agent management system

        Returns
        -------
        hooked_up : bool
            True if the agent has an ID in an agent management system, False
            otherwise

        '''
        return (not self.agent_id_system is None)

    def __str__(self):

        return self.name + '(ID:%s)'%(str(self.agent_id_system))

    def __call__(self):
        '''Method to call agent invokes the executive function. This should be
        defined in specific classes that uses the present class as parent.

        '''
        raise RuntimeError('Basic Agent class has no executive function. ' + \
                           'That should be implemented in specific agent classes.')

    def __init__(self, name):

        self.name = name

        #
        # Agent ID is a property of the agent assigned by the agent system 
        # manager as agents are included in the bookkeeping
        #
        self.agent_id_system = None

        #
        # Scaffolds of the agent. There can be only one resource and one
        # essence
        self.resource = None
        self.essence = None
        self.scaffold = {'resource' : self.resource,
                         'essence' : self.essence}

        #
        # Messages of the agent. These are typically assigned along with the
        # setting of organs
        #
        self.belief = {}
        self.buzz = {}
        self.direction = {}
        self.feature = {}
        self.message = {'belief' : self.belief,
                        'buzz' : self.buzz,
                        'direction' : self.direction,
                        'feature' : self.feature}

        #
        # Organs of the agent. These are assigned with the appropriate setter
        # function
        #
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

        # 
        # Mandatory cortex organ to reveal what cortices are available
        #
        feature = Feature('cortices_available', ('cortices_names',))
        cortex_reveal_cortex_labels = Cortex('reveal_available_cortex', 
                                             None,
                                             self._tickle_cortex_labels, 
                                             feature)
        self.set_organ(cortex_reveal_cortex_labels)

