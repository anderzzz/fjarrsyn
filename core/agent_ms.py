'''Bla bla

'''
from uuid import uuid4

class AgentManagementSystem(object):
    '''Bla bla

    '''
    def agents_iter(self):
        '''Bla bla

        '''
        return iter(self.agents_in_scope.values())

    def __init__(self, name, agents):

        self.name = name

        self.agents_in_scope = {}
        for agent in agents:
            agent.agent_id_system = str(uuid4())
            self.agents_in_scope[agent.agent_id_system] = agent
