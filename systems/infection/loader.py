'''Load a system from saved data

'''
import sys
import pandas as pd
import networkx as nx

from systems.infection.unit import Unit, AgentAuxEnv
from systems.infection.world import World
from core.graph import Node

load_dir = sys.argv[1]

agent_file = load_dir + '/save_agent_state0.csv'
env_file = load_dir + '/save_env_state0.csv'
graph_file = load_dir + '/save_graph_state0.edgelist'
df_a = pd.read_csv(agent_file)
gg_a = df_a.groupby('agent_index')
agents = {} 
for a_id, a_data in gg_a:
    belief_d = {}
    essence_d = {}
    resource_d = {}

    agent = Unit('Agent', agent_id=a_id)
    for _, row in a_data.iterrows():
        dd = row.to_dict()
        xx = dd['variable'].split(':')

        if xx[0] == 'belief':
            belief_d[(xx[1], xx[2])] = dd['value']
        if xx[0] == 'essence':
            essence_d[xx[2]] = dd['value']
        if xx[0] == 'resource':
            resource_d[xx[2]] = dd['value']

    essence_val = []
    for e_key in agent.essence.keys():
        essence_val.append(essence_d[e_key])

    resource_val = []
    for r_key in agent.resource.keys():
        resource_val.append(resource_d[r_key])

    belief_val = []
    for b_key_1 in agent.belief:
        for b_key_2 in agent.belief[b_key_1].keys():
            belief_val.append(belief_d[(b_key_1, b_key_2)])

    agent.essence.set_values(essence_val)
    agent.resource.set_values(resource_val)
    agent.belief[b_key_1].set_values(belief_val)

    agents[a_id] = agent

df_e = pd.read_csv(env_file)
gg_e = df_e.groupby('agent_index')
envs = {}
for a_id, e_data in gg_e:
    r_container = {}
    for _, row in e_data.iterrows():
        dd = row.to_dict()
        r_container[dd['variable']] = dd['value']
    env = AgentAuxEnv(**r_container)

    envs[a_id] = env

nodes = {}
for a_id in agents:
    nn = Node('', agents[a_id], envs[a_id])
    nodes[a_id] = nn

graph = nx.Graph()
graph.add_nodes_from(nodes.values())
fin = open(graph_file)
lines = fin.read().split('\n')
for line in lines[:-1]:
    xx = line.split(' ')
    n1 = nodes[xx[0]]
    n2 = nodes[xx[1]]
    graph.add_edge(n1, n2)

ww = World('dummy', agents.values(), graph, 0.0, 0.0, 0.0, 0.0, 0.0, [])
print (ww)
