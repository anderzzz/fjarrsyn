'''Basic object to store the agents and auxiliary content in the agent system
graph. The object should be considered to be replaced with namedtuple at some
point, once the default field has matured

'''
class Node(object):
    '''Basic object to store agent and auxiliary content in the agent system.

    Parameters
    ----------
    name : str
        Name of node
    agent_content : Agent
        An Agent object
    aux_content : optional
        Auxiliary content, such as an immediate environment, to the Agent of
        the Node
    other_attributes : dict, optional
        Dictionary of additional attributes assigned to the Node. These can
        be part of operations on the graph during a simulation or they can be
        part of graph sampling, for example. Each key is the name of the
        attribute, the value is the value of the attribute.
    
    '''
    def __str__(self):
        
        return self.name

    def __contains__(self, item):

        if self.agent_content is None:
            return False

        else:
            return item == self.agent_content.agent_id_system

    def __init__(self, name, agent_content, aux_content=None,
                 other_attributes={}):

        self.name = name 
        self.agent_content = agent_content
        self.aux_content = aux_content

        for key, item in other_attributes:
            setattr(self, key, item)

