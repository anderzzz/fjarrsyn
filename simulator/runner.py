'''Bla bla

'''
class Runner(object):
    '''Bla bla

    '''
    def __call__(self, agent_ms):
        '''Bla bla

        '''
        for k_iter in range(self.n_iter):
            for agent in agent_ms.iteritems():
                agent()

    def __init__(self, n_iter, random=False):

        self.n_iter = n_iter

