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
        
        return 'Node(name:%s)' %(self.name)

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

def node_maker(agents, envs=None, node_names=None, node_attributes=None):
    '''Convenience function to place a collection of agents and environments in nodes

    Parameters
    ----------
    TBD

    Returns
    -------
    TBD

    '''
    n_nodes = len(agents)

    if not envs is None:
        if len(envs) != n_nodes:
            raise ValueError('Environment container not of same size as agent container')
        envs_iter = envs

    else:
        envs_iter = [None] * n_nodes

    if not node_names is None:
        if len(node_names) != n_nodes:
            raise ValueError('Node names container no of same size as agent container')
        node_names_iter = node_names

    else:
        node_names_iter = ['ID {}'.format(k) for k in range(n_nodes)]

    if not node_attributes is None:
        if len(node_attributes) != n_nodes:
            raise ValueError('Node attributes container not of same size as agent container')
        node_attributes_iter = node_attributes

    else:
        node_attributes_iter = [{}] * n_nodes

    ret = []
    for agent, env, name, attributes in zip(agents, envs_iter, node_names_iter, node_attributes_iter):
        ret.append(Node(name, agent, env, attributes))

    return ret