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

    def _apply_resource_map(self, resource_map):
        '''Convenience function to apply a resource map, if present, to the
        agent resources

        Parameters
        ----------
        resource_map : ResourceMap
            A resource map, presumably attached to a recently executed organ

        '''
        if not resource_map is None:
            if not resource_map.is_empty():
                resource_map.apply_to(self)

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
            self._inverse_map[organ.name] = 'sensor'

        elif isinstance(organ, Actuator):
            self._set('actuator', organ.name, organ)
            self._inverse_map[organ.name] = 'actuator'

        elif isinstance(organ, Interpreter):
            self._set('interpreter', organ.name, organ)
            self._set('belief', organ.array_output.array_name, organ.array_output)
            self._inverse_map[organ.name] = 'interpreter'

        elif isinstance(organ, Moulder):
            self._set('moulder', organ.name, organ) 
            self._set('direction', organ.array_output.array_name,
                                   organ.array_output)
            self._inverse_map[organ.name] = 'moulder'

        elif isinstance(organ, Cortex):
            self._set('cortex', organ.name, organ)
            self._set('feature', organ.array_output.array_name,
                                 organ.array_output)
            self._inverse_map[organ.name] = 'cortex'

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

    def tickle(self, phrase):
        '''Verb for the agent to execute a Cortex organ

        Notes
        -----
        The method collects the Cortex associated with input phrase and
        executes it as well as applies any resource map created by the organ.

        Unlike other verbs, this is activated by an external agent, therefore
        any illegal phrase does not raise an exception, instead returns None.

        Parameters
        ----------
        phrase : str
            Name of the Cortex to execute

        '''
        if not phrase in self.cortex:
            return None

        else:
            the_cortex = self.cortex[phrase]

        reaction = the_cortex()

        return reaction 

    def sense(self, phrase):
        '''Verb for the agent to execute a Sensor organ

        Notes
        -----
        The method collects the Sensor associated with input phrase and
        executes it as well as applies any resource map created by the organ

        Parameters
        ----------
        phrase : str
            Name of the Sensor to execute

        Raises
        ------
        KeyError
            If agent has no Sensor associated with the phrase

        '''
        if not phrase in self.sensor:
            raise KeyError('Agent lacks sensor for %s' %(phrase))

        else:
            the_sensor = self.sensor[phrase]

        did_it_sense = the_sensor(self.agent_id_system)
        self._apply_resource_map(the_sensor.resource_map)

    def interpret(self, phrase):
        '''Verb for the agent to execute an Interpreter organ

        Notes
        -----
        The method collects the Interpreter associated with input phrase and
        executes it as well as applies any resource map created by the organ

        Parameters
        ----------
        phrase : str
            Name of the Interpreter to execute

        Raises
        ------
        KeyError
            If agent has no Interpreter associated with the phrase

        '''
        if not phrase in self.interpreter:
            raise KeyError('Agent lacks interpreter for %s' %(phrase))

        else:
            the_interpreter = self.interpreter[phrase]

        did_it_interpret = the_interpreter()
        self._apply_resource_map(the_interpreter.resource_map)

    def mould(self, phrase):
        '''Verb for the agent to execute a Moulder organ

        Notes
        -----
        The method collects the Moulder associated with input phrase and
        executes it as well as applies any resource map created by the organ

        Parameters
        ----------
        phrase : str
            Name of the Moulder to execute

        Raises
        ------
        KeyError
            If agent has no Moulder associated with the phrase

        '''
        if not phrase in self.moulder:
            raise KeyError('Agent lacks moulder for %s' %(phrase))

        else:
            the_moulder = self.moulder[phrase]

        did_it_mould = the_moulder()
        self._apply_resource_map(the_moulder.resource_map)

    def act(self, phrase):
        '''Verb for the agent to execute an Actuator organ

        Notes
        -----
        The method collects the Actuator associated with input phrase and
        executes it as well as applies any resource map created by the organ

        Parameters
        ----------
        phrase : str
            Name of the Actuator to execute

        Raises
        ------
        KeyError
            If agent has no Actuator associated with the phrase

        '''
        if not phrase in self.actuator:
            raise KeyError('Agent lacks Actuator for %s' %(phrase))

        else:
            the_actuator = self.actuator[phrase]

        did_it_act = the_actuator(self.agent_id_system)
        self._apply_resource_map(the_actuator.resource_map)

    def engage(self, organ_sequence):
        '''Compound verb for agent to execute a sequence of multiple organs

        Parameters
        ----------
        organ_sequence : Iterable
            An iterable of strings, each string pointing to a unique organ of
            any type, other than cortex. The appropriate verb for agent are
            executed in the same order as in the sequence

        Notes
        -----
        The method assumes that all organs, all types considered, have unique
        names. If that is not true this compound verb is not well-defined.
        However, no check is explicitly made to ensure unique names are used.

        '''
        for organ_name in organ_sequence:
            if not organ_name in self._inverse_map:
                raise KeyError('The organ name %s not among agent organs' %(organ_name))

            if self._inverse_map[organ_name] == 'sensor':
                self.sense(organ_name)
            elif self._inverse_map[organ_name] == 'interpreter':
                self.interpret(organ_name)
            elif self._inverse_map[organ_name] == 'moulder':
                self.mould(organ_name)
            elif self._inverse_map[organ_name] == 'actuator':
                self.act(organ_name)
            elif self._inverse_map[organ_name] == 'cortex':
                raise ValueError('The agent can only engage in intentional ' + \
                                 'actions, not cortical ones')
            else:
                KeyError('Unknown organ type %s' %(self._inverse_map[organ_name]))

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
        self._inverse_map = {}

        # 
        # Mandatory cortex organ to reveal what cortices are available
        #
        feature = Feature('cortices_available', ('cortices_names',))
        cortex_reveal_cortex_labels = Cortex('reveal_available_cortex', 
                                             None,
                                             self._tickle_cortex_labels, 
                                             feature)
        self.set_organ(cortex_reveal_cortex_labels)

