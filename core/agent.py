'''The Agent parent class.

'''
import copy
import numpy
import numpy.random
from collections import namedtuple

from core.instructor import Sensor, Actuator, Interpreter, Moulder, Cortex
from core.policy import Plan, Clause, Heartbeat
from core.message import Resource, Essence, Feature, Buzz, Belief, Direction
from core.sampler import AgentSampler
from core.constants import AGENT_IMPRINTS

class SocketConnectionError(Exception):
    pass

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
    class _IsInert(object):
        '''Decorator method for the verbs of the current Agent. If the agent
        has been declared inert, all verbs are rendered inactive.

        '''
        @classmethod
        def check(self, verb):

            def verb_decorated(*args, **kwargs):
                inert_agent = args[0].inert
                if inert_agent is True:
                    return False
                else:
                    return verb(*args, **kwargs)

            return verb_decorated

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

        elif isinstance(organ, Actuator):
            self._set('actuator', organ.name, organ)

        elif isinstance(organ, Interpreter):
            self._set('interpreter', organ.name, organ)
            self.set_message(organ.message_output)

        elif isinstance(organ, Moulder):
            self._set('moulder', organ.name, organ) 
            self.set_message(organ.message_output)

        elif isinstance(organ, Cortex):
            self._set('cortex', organ.name, organ)
            self.set_message(organ.message_output)

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

        elif isinstance(policy, Plan):
            self._set('plan', policy.name, policy)

        elif isinstance(policy, Heartbeat):
            self._set('heartbeat', policy.name, policy)

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

    @_IsInert.check
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

    @_IsInert.check
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
        
        return did_it_sense

    @_IsInert.check
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

        return did_it_interpret

    @_IsInert.check
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

        return did_it_mould

    @_IsInert.check
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

        return did_it_act

    @_IsInert.check
    def pronounce(self, phrase):
        '''Compound verb for agent to execute a sequence of multiple organs
        with optionally added condition check at the end

        Parameters
        ----------
        phrase : str
            Name of the clause to execute

        Raises
        ------
        KeyError
            If agent has no Clause associated with the phrase

        '''
        if not phrase in self.clause:
            raise KeyError('Agent lacks Clause for %s' %(phrase))

        else:
            the_clause = self.clause[phrase]

        return the_clause(self) 

    @_IsInert.check
    def enact(self, code_name):
        '''Execute a plan of certain code name

        Parameters
        ----------
        code_name : str
            Code name of the plan available to the agent

        Raises
        ------
        KeyError
            If the agent has no plan of given code name

        '''
        if not code_name in self.plan:
            raise KeyError('Agent lacks plan with code name %s' %(code_name))

        else:
            the_plan = self.plan[code_name]

        the_plan.enacted_by(self)

    @_IsInert.check
    def pump(self, phrase):
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
        if not phrase in self.heartbeat:
            raise KeyError('Agent lacks Heartbeat for %s' %(phrase))

        else:
            the_heartbeat = self.heartbeat[phrase]

        still_alive = the_heartbeat(self)

        if still_alive is False:
            self.inert = True

        return still_alive

    @_IsInert.check
    def sample(self, generation=0):
        '''Sample the agent imprints according to a sampler

        Parameters
        ----------
        generation : int, optional
            Meta data about when the agent is sampled. If not specified set to
            zero.

        Returns
        -------
        ret_data : dict
            Dictionary with sampled data, key being the type of data, value the
            data. The content of dictionary is mostly specified in the
            initilization of the sampler. Exception is three entries
            that specifies the agent identity (name and agent system ID) and
            sample time (generation)

        '''
        if self.sampler is None:
            raise TypeError('An AgentSampler instance has not been set')

        if not isinstance(self.sampler, AgentSampler):
            raise TypeError('The sampler for agent must be instance of AgentSampler')

        return self.sampler.sample(self, generation)

    def connect_to(self, other_agent, socket_id, token=None):
        '''Method to use for given agent in order to connect to a socket
        of the other agent

        Parameters
        ----------
        other_agent : Agent
            The Agent object of the external agent to which a socket connection
            is attempted
        socket_id : str
            The socket id or short-hand to which connection is made
        token : int, optional
            The token required to be granted connection to the socket.

        Returns
        -------
        conn
            The socket connection object. Two methods are available as
            attributes, `execute` and `close`, which executes the associated
            functionality to the connected socket, and closes the connection

        '''
        try:
            socket_other = other_agent.socket_offered[socket_id]
        except KeyError:
            raise KeyError('Unknown socket %s for agent %s' \
                           %(socket_id, other_agent.__repr__()))

        return socket_other.connect(self.agent_id_system, token)

    def create_socket(self, name, verb, phrase, create_token=True):
        '''Agent creates intentionally a socket to a particular verb and phrase
        that enables delegation of execution to an external agent

        Parameters
        ----------
        name : str
            Name of socket, the short-hand the external agent will use
        verb : str
            The verb method to expose.
        phrase : str
            The phrase associated with the given verb to expose.
        create_token : bool, optional
            If True, a random token is created that is associated with the
            socket, such that only if the right token is provided during
            connection will it enable execution

        Notes
        -----
        The method adds the created socket to the agent dictionary of
        `socket_offered`.

        Currently the token is not securely created.

        '''
        func = getattr(self, verb)

        if not create_token:
            token = None

        else:
            token = numpy.random.randint(10**12) 

        socket = Socket(name, func, verb, phrase, token)
        self.socket_offered[name] = socket

    def get_imprint_repr(self, imprint_subset=None):
        '''Return for agent the string representations for all or a subset of
        agent imprints

        Parameters
        ----------
        imprint_subset : list, optional
            Subset of agent imprint names for which to create the string
            representation. If None, all imprints are handled.

        Returns
        -------
        imprint_reprs : dict
            Dictionary of lists of string representations of designated agent
            imprints, keyed on the type of imprint

        '''
        def _get_minor_keys(a):
            return [(a.name, key_) for key_ in a.keys()]
                
        if not imprint_subset is None:
            if not set(imprint_subset).issubset(AGENT_IMPRINTS):
                raise ValueError('Imprint subset not a subset to AGENT_IMPRINTS constant')

        else:
            imprint_subset = AGENT_IMPRINTS

        ret = {} 
        for impr in imprint_subset:

            a_imprint = getattr(self, impr)

            if a_imprint is None:
                continue
            if len(a_imprint) == 0:
                continue

            if impr == 'belief':
                _minor = []
                for major_key in a_imprint.keys():
                    _minor += _get_minor_keys(a_imprint[major_key])

            else:
                _minor = _get_minor_keys(a_imprint)

            ret[impr] = [(x1, x2) for x1, x2 in _minor]

        return ret

    def hooked_up(self):
        '''Determines if agent is part of an agent management system

        Returns
        -------
        hooked_up : bool
            True if the agent has an ID in an agent management system, False
            otherwise

        '''
        return (not self.agent_id_system is None)

    def revive(self):
        '''Revive an agent that has been inert for some reason

        '''
        self.ticks = 0
        self.inert = False

    def deepcopy(self):
        '''Create a deep copy of the current agent, functional and parametric

        Returns
        -------
        agent : Agent
            A copy of current agent.

        Notes
        -----
        The method creates a replica of the current agent, which means organs,
        policies, resources, messages and essence are copied. The name as well
        as the agent_id are however unassigned, since these relate to the agent
        as a specific particle in the system and should be assigned as part of
        assigning the agent a place within the system. The heart ticks are set
        to zero as well, such that the new agent is at its youngest state.

        If an agent has a more complex method of reproduction, like adjusting
        certain of its parametric features (essence, resources, beliefs), these
        additional adjustments should be added after calling the current
        method.

        '''
        copy_agent = copy.deepcopy(self)

        copy_agent.name = ''
        copy_agent.agent_id_system = None
        copy_agent.inert = False
        copy_agent.ticks = 0

        return copy_agent

    def __repr__(self):

        return 'Agent ' + self.name + '(ID:%s)'%(str(self.agent_id_system))

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
        # Optional sampler for agent
        #
        self.sampler = None

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
                                             self._tickle_cortex_labels, 
                                             None,
                                             feature)
        self.set_organ(cortex_reveal_cortex_labels)

        #
        # External
        #
        self.socket_offered = {}

        #
        # Variables for the dynamics of the agent
        #
        self.inert = False
        self.ticks = 0
        self.clause = {}
        self.plan = {}
        self.heartbeat = {} 
        self.policies = {'clause' : self.clause,
                         'plan' : self.plan,
                         'heartbeat' : self.heartbeat}

class Socket(object):
    '''Socket object exposes part of an Agent verb-phrase functionality to an
    external interface to which another Agent can connect

    Parameters
    ----------

    '''
    def connect(self, agent_id_calling, token_input=None):
        '''Method to connect to a socket from an external agent

        Parameters
        ----------
        agent_id_calling : str
            The agent system ID of the agent utilizing the socket
        token_input : int, optional
            If socket requires a token to use, the token must be provided
            otherwise a connection is not formed.

        Returns
        -------
        connection 
            The connection object that grants a defined control over the agent
            functionality attached to the socket. There are two attributes of
            the connection, `execute` and `close`, which are methods that
            when called execute the functionality associated with the socket
            and closes the connection with the socket, respectively.

        '''
        if (agent_id_calling in self.whitelist) and \
           (token_input == self.token):
            self._open_socket = True
            return self.Connection(self._execute, self._close) 

        else:
            self._open_socket = False
            raise SocketConnectionError('Agent (ID:%s) failed to connect ' %(agent_id_calling) + \
                                        'to socket <%s>' %(self.__repr__()))

    def _execute(self, args=()):
        '''The method that executes the verb and phrase

        Parameters
        ----------
        args : tuple, optional
            Any arguments to the verb method.

        Returns
        -------
        ret
            The return value of the verb phrase execution, typically a Boolean

        Raises
        ------
        RuntimeError
            If a connection that is not open is attemtpted to be executed

        '''
        if not self._open_socket:
            raise RuntimeError('Cannot execute an unopened connection')

        return self.func(self.phrase, *args)

    def _close(self):
        '''Close the connection to the socket

        '''
        self._open_socket = False

    def __repr__(self):
        if self.token is None:
            s_end = ' without token'
        else:
            s_end = ' with token'

        return 'Socket (name: %s) for verb "%s" and phrase "%s"' %(self.name, self.verb, self.phrase) + s_end 

    def __init__(self, name, func, verb, phrase, token):

        self.name = name
        self.func = func
        self.verb = verb
        self.phrase = phrase
        self.token = token

        self.whitelist = set([])
        self._open_socket = False

        self.Connection = namedtuple('Connection', ['execute', 'close'])
