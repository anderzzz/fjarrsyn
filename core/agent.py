'''The Agent parent class.

'''
from core.instructor import Sensor, Actuator, Interpreter, Moulder, Cortex
from core.policy import Clause, Heartbeat
from core.message import Resource, Essence, Feature, Buzz, Belief, Direction

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
    strict_engine : bool, optional
        If False, any exceptions from engine execution of instructors are
        non-fatal to the execution. If True, engine exceptions terminates
        execution

    '''
    def _tickle_cortex_labels(self):
        '''Mandatory cortex function of agent to reveal all cortex labels.

        Returns
        -------
        keys : list
            List of unadulterated string keys for the cortex functions of the agent.

        '''
        return (list(self.cortex.keys()),)

    def apply_map(self, _map):
        '''Convenience function to apply a resource map, if present, to the
        agent resources

        Parameters
        ----------
        _map : _Map
            A resource or essence map, which was created by an Instructor, like
            an organ or an external law

        '''
        if not _map is None:
            if not _map.is_empty():
                _map.apply_to(self)

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

    def set_scaffold(self, scaffold, allow_overwrite=True):
        '''Add a scaffold to the agent 

        Parameters
        ----------
        scaffold : Resource or Essence
            An agent scaffold that defines a property of the agent constitution
        allow_overwrite : bool, optional
            If True the scaffold can be altered, if False the scaffold can only
            be assigned once

        Raises
        ------
        RuntimeError
            If scaffold reassignment is attempted after first assignment
        TypeError
            If scaffold is neither an instance of Resource or Essence

        '''
        if not isinstance(allow_overwrite, bool):
            raise TypeError('`allow_overwrite` should be Boolean')

        if isinstance(scaffold, Resource):
            if (not allow_overwrite) and (not self.resource is None):
                raise RuntimeError('Agent resource not allowed to be ' + \
                                   'changed after first assignement')
            else:
                self.resource = scaffold

        elif isinstance(scaffold, Essence):
            if (not allow_overwrite) and (not self.essence is None):
                raise RuntimeError('Agent essence not allowed to be ' + \
                                   'changed after first assignement')
            else:
                self.essence = scaffold

        else:
            raise TypeError('Agent scaffold should be instance of ' + \
                            'class Resource or Essence')

    def set_scaffolds(self, *scaffolds, allow_overwrite=True):
        '''Add several scaffolds to the agent at once

        Parameters
        ----------
        scaffolds : Resource or Essence
            An agent scaffold that defines a property of the agent constitution
        allow_overwrite : bool, optional
            If True the scaffold can be altered, if False the scaffold can only
            be assigned once

        '''
        for scaffold in scaffolds: 
            self.set_scaffold(scaffold, allow_overwrite)

    def set_message(self, message, allow_overwrite=True):
        '''Add a message available to the organs of the agent.

        Parameters
        ----------
        message : Buzz, Belief, Direction, Feature
            The message instance to add to the agent's repetoire. The message
            must be one of the known message classes, not a scaffold

        Raises
        ------
        TypeError
            If the `message` that is given as input is not an instance of a
            known message class

        '''
        if not isinstance(allow_overwrite, bool):
            raise TypeError('`allow_overwrite` should be Boolean')

        if isinstance(message, Buzz):
            self._set('buzz', message.name, message)

        elif isinstance(message, Belief):
            self._set('belief', message.name, message)

        elif isinstance(message, Direction):
            self._set('direction', message.name, message)

        elif isinstance(message, Feature):
            self._set('feature', message.name, message)

        else:
            raise TypeError('Unknown message type: %s' %(str(type(message))))

    def set_messages(self, *messages, allow_overwrite=True):
        '''Add several messages to the agent at once

        Parameters
        ----------
        messages : Buzz, Belief, Direction, Feature
            An agent message
        allow_overwrite : bool, optional
            If True the message can be altered, if False the message can only
            be assigned once

        '''
        for message in messages:
            self.set_message(message, allow_overwrite)

    def set_organ(self, organ):
        '''Add an organ to the agent.

        Parameters
        ----------
        organ
            The instructor class instance to add to the agent. The organ must be one
            of the known organ classes

        Raises
        ------
        TypeError
            If the `organ` that is given as input is not an instance of a known
            organ class

        '''
        if isinstance(organ, Sensor):
            self._set('sensor', organ.name, organ)
            self.set_message(organ.message_output)
            self._inverse_map[organ.name] = 'sensor'

        elif isinstance(organ, Actuator):
            self._set('actuator', organ.name, organ)
            self._inverse_map[organ.name] = 'actuator'

        elif isinstance(organ, Interpreter):
            self._set('interpreter', organ.name, organ)
            self.set_message(organ.message_output)
            self._inverse_map[organ.name] = 'interpreter'

        elif isinstance(organ, Moulder):
            self._set('moulder', organ.name, organ) 
            self.set_message(organ.message_output)
            self._inverse_map[organ.name] = 'moulder'

        elif isinstance(organ, Cortex):
            self._set('cortex', organ.name, organ)
            self.set_message(organ.message_output)
            self._inverse_map[organ.name] = 'cortex'

        else:
            raise TypeError('Unknown organ type: %s' %(str(type(organ))))

    def set_organs(self, *organs):
        '''Add organs to the agent

        Parameters
        ----------
        organs
            Argument tuple of organs to add to the agent. Must be instances
            of known organ classes

        '''
        for organ in organs:
            self.set_organ(organ)

    def set_policy(self, policy):
        '''Set a policy item the agent has access to for execution

        Parameters
        ----------
        policy
            The policy object

        Raises
        ------
        TypeError
            If the policy input is of unknown type

        '''
        if isinstance(policy, Clause):
            self._set('clause', policy.name, policy)

        elif isinstance(policy, Heartbeat):
            self.heartbeat = policy

        else:
            raise TypeError('Unknown policy type: %s' %(str(type(policy))))

    def set_policies(self, *policies):
        '''Add policies to the agent

        Parameters
        ----------
        policies
            Container of elements of the policy class instance to add to the
            agent in bulk.

        '''
        for policy in policies:
            self.set_policy(policy)

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

        did_it_reveal = the_cortex(self.agent_id_system)
        if self.strict_engine and (not did_it_reveal is True):
            raise did_it_reveal

        return the_cortex.message_output

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
        if self.strict_engine and (not did_it_sense is True):
            raise did_it_sense

        self.apply_map(the_sensor.scaffold_map_output)

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

        did_it_interpret = the_interpreter(self.agent_id_system)
        if self.strict_engine and (not did_it_interpret is True):
            raise did_it_interpret

        self.apply_map(the_interpreter.scaffold_map_output)

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

        did_it_mould = the_moulder(self.agent_id_system)
        if self.strict_engine and (not did_it_mould is True):
            raise did_it_mould

        self.apply_map(the_moulder.scaffold_map_output)

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
        if self.strict_engine and (not did_it_act is True):
            raise did_it_act

        self.apply_map(the_actuator.scaffold_map_output)

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

    def pump(self):
        '''Agent heart beat counter, which can be used in execution of policies
        of the agent keeping track of how many iterations have been performed
        and if a terminal exit condition is met

        Parameters
        ----------
        n_max : int, optional
            Maximum number of heart beats before end of execution. If None, the
            execution goes on forever or until other terminal condition is met

        Returns
        -------
        continue_life : bool
            True if agent can iterate further in the execution, False if not

        '''
        if self.heartbeat is None:
            return True

        else:
            return self.heartbeat(self) 

    def __str__(self):

        return self.name + '(ID:%s)'%(str(self.agent_id_system))

    def __call__(self):
        '''Method to call agent invokes the executive function. This should be
        defined in specific classes that uses the present class as parent.

        '''
        raise RuntimeError('Basic Agent class has no executive function. ' + \
                           'That should be implemented in specific agent classes.')

    def __init__(self, name, strict_engine=False):

        self.name = name
        self.strict_engine = strict_engine

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
                                             self._tickle_cortex_labels, 
                                             None,
                                             feature)
        self.set_organ(cortex_reveal_cortex_labels)

        #
        # Variables for the dynamics of the agent
        #
        self.n_heart_beats = 0
        self.inert = False
        self.clause = {}
        self.heartbeat = None
        self.policies = {'clause' : self.clause,
                         'heartbeat' : self.heartbeat}
