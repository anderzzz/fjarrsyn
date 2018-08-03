'''Bla bla

'''
import numpy as np
import numpy.random

class BeakerPropagator(object):
    '''Bla bla

    '''
    def __call__(self, system):
        '''Bla bla

        '''
        for agent, aux_object in system:

            print (agent)
            if not agent is None:

                agent_survived = agent()
                if agent_survived:
                    self.agent_mutator(agent)

            self.aux_objectforce(aux_object)

    def __init__(self, agent_mutator, aux_objectforce):

        self.agent_mutator = agent_mutator
        self.aux_objectforce = aux_objectforce



