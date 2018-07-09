'''Bla bla

'''
import random

from core.agent import EngagedAgent

class Ant(EngagedAgent):
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
        return self.scaffold['my_opinion']

    def _execute_form_new_opinion_imitation(self):
        '''Bla bla

        '''
        opinions_around_me = self._sense('neighbours_opinions', 
                                        {'agent_index': self.agent_id_system})
        n_neighbours = len(opinions_around_me)

        if random.random() > self.scaffold['rebel']:
            opinion = opinions_around_me[random.randrange(n_neighbours)]
        else:
            opinion = random.choice(self.scaffold['my_opinion_enumeration'])

        self.set_data('scaffold', 'my_opinion', opinion)

        return True

    def __call__(self):

        self._execute_form_new_opinion_imitation()

        return True

    def __init__(self, name, rebel_index, opinion_init, opinion_universe):

        super().__init__(name)

        self.set_data('scaffold', 'rebel', rebel_index)
        self.set_data('scaffold', 'my_opinion', opinion_init)
        self.set_data('scaffold', 'my_opinion_enumeration', opinion_universe)

        self.set_organ('service', 'what_is_opinion', self._request_what_is_opinion)

        self.set_organ('plan', 'form_new_opinion_imitation', 
                      self._execute_form_new_opinion_imitation)

