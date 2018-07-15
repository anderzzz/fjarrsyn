'''Agent 

'''
import random

from core.organs import Sensor, Actuator, Interpreter, Moulder, Cortex

NULL_RETURN = (None, False) 

class Agent(object):
    '''Bla bla

    '''
    def _tickle_cortex_labels(self):
        '''Bla bla

        '''
        return self.cortex.keys() 

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

    def set_organ(self, organ):
        '''Bla bla

        '''
        #HOW TO KEY INTERPRETER? ON SENSOR? ON BUZZ PROFILE
        if isinstance(organ, Sensor):
            self._set('sensor', organ.precept_name, organ)

        elif isinstance(organ, Actuator):
            self._set('actuator', organ.action_name, organ)

        elif isinstance(organ, Interpreter):
            self._set('interpreter', organ.name, organ)

        elif isinstance(organ, Moulder):
            pass

        elif isinstance(organ, Cortex):
            self._set('cortex', organ.tickle_name, organ)

        else:
            raise TypeError('Unknown organ type: %s' %str(type(organ)))

    def tickle(self, itch):
        '''Bla bla

        '''
        if not itch in self.cortex:
            raise RuntimeError('Agent lacks cortex for itch %s' %(itch))

        else:
            func = self.cortex[itch]

        reaction = func()

        return reaction 

    def sense(self, precept):
        '''Method for agent to sense a precept of the environment. The method
        should only be called by the agent itself

        '''
        if not precept in self.sensor:
            raise RuntimeError('Agent lacks sensor for precept %s' %(precept))

        else:
            the_sensor = self.sensor[precept]

        buzz = the_sensor()

        return buzz 

    def interpret(self, brain_tissue, buzz):
        '''Bla bla

        '''
        if not brain_tissue in self.interpreter:
            raise RuntimeError('Agent lacks interpreter %s' %(brain_tissue))

        else:
            the_interpreter = self.interpreter[brain_tissue]

        updated_belief_labels = the_interpreter(buzz)

        return updated_belief_labels

    def mould(self, target, kwargs={}):
        '''Bla bla

        '''
        if not target in self.moulder:
            raise RuntimeError('Agent lacks moulder for %s' %(target))

        else:
            the_moulder = self.moulder[target]

        actuators = the_moulder(**kwargs)

        return actuators

    def __str__(self):

        return self.name + '(ID:%s)'%(str(self.agent_id_system))

    def __init__(self, name):

        self.name = name
        self.agent_id_system = None

        self.scaffold = {}
        self.belief = {}
        self.data = {'scaffold' : self.scaffold, 'belief' : self.belief}

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

