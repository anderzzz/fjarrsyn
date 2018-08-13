'''Bla bla

'''
import logging

#def pretty_print(dd):
#    l = ['(%s : %s)' %(key, str(dd[key])) for key in sorted(dd.keys())]
#    j = ';'.join(l)
#    return j

class BeakerPropagator(object):
    '''Bla bla

    '''
    def __call__(self, system):
        '''Bla bla

        '''
        for agent, aux_object in system:

#            logging.debug('---> NEW NODE')

            if not agent is None:

#                logging.debug('Environment scaffold before agent interaction')
#                logging.debug(pretty_print(aux_object.scaffold))

                agent_survived = agent()
                if agent_survived:
#                    logging.debug('Agent scaffold after intentional action')
#                    logging.debug(pretty_print(agent.scaffold))

                    self.agent_mutator(agent)

#                    logging.debug('Agent scaffold after random mutation')
#                    logging.debug(pretty_print(agent.scaffold))

#            logging.debug('Environment scaffold before force')
#            logging.debug(pretty_print(aux_object.scaffold))

            self.aux_objectforce(aux_object)

#            logging.debug('Environment scaffold after force')
#            logging.debug(pretty_print(aux_object.scaffold))

    def __init__(self, agent_mutator, aux_objectforce):

        self.agent_mutator = agent_mutator
        self.aux_objectforce = aux_objectforce


