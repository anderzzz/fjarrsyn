'''Bla bla

'''
import random

from core.agent import Agent

class Ant(Agent):
    '''Bla bla

    '''
    def _request_what_is_opinion(self):
        '''Unadulterated service request method to supply agent opinion

        Notes
        -----
            Should not be directly accessed from an external source, rather the
            `request_service` method is what is publically available.

        Returns
        -------
        my_opinion 
            The opinion of the agent

        '''
        return self.nature['my_opinion']

    def _execute_form_new_opinion_imitation(self):
        '''Bla bla

        '''
        opinions_around_me = self._sense('neighbours_opinions', 
                                        {'agent_index': self.agent_id_system})
        n_neighbours = len(opinions_around_me)

        if random.random() > self.nature['rebel']:
            one_opinion = opinions_around_me[random.randrange(n_neighbours)]
            self.set_nature('my_opinion', one_opinion)
        else:
            random_opinion = random.choice(self.natural_constraint['my_opinion'])
            self.set_nature('my_opinion', random_opinion) 

    def __init__(self, name, rebel_index, opinion_init, opinion_universe):

        super().__init__(name)

        self.set_nature('rebel', rebel_index)
        self.set_nature('my_opinion', opinion_init)
        self.set_natural_constraint('my_opinion', enumeration=opinion_universe)

        self.set_service('what_is_opinion', self._request_what_is_opinion)

        self.set_plan('form_new_opinion_imitation', 
                      self._execute_form_new_opinion_imitation)

