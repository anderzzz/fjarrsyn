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
        return self.belief['my_opinion']

    def _request_form_new_opinion(self):
        '''Bla bla

        '''
        opinions_around_me = self._sense['neighbours_opinions']
        n_neighbours = len(opinions_around_me)

        if self.belief['forming_opinion'] == 'immitate_one':
            one_opinion = opinions_around_me[random.randrange(n_neighbours)]
            if random.random() > self.belief['rebel']:
                self.update_belief('my_opinion', one_opinion)


    def __init__(self, name, rebel_index, opinion_init, opinion_forming):

        super().__init__(name)

        self.update_belief('rebel', rebel_index)
        self.update_belief('my_opinion', opinion_init)
        self.update_belief('forming_opinion', opinion_forming)

        self.add_service('what_is_opinion', self._request_what_is_opinion)
        self.add_service('form_new_opinion', self._request_form_new_opinion)

