'''Bla bla

'''
class Node(object):
    '''Bla bla
    
    '''
    def __str__(self):
        
        return self.name

    def __contains__(self, item):

        if self.agent_content is None:
            return False

        else:
            return item == self.agent_content.agent_id_system

    def __init__(self, name, agent_content, aux_content=None):

        self.name = name 
        self.agent_content = agent_content
        self.aux_content = aux_content

