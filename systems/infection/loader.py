'''Load a system from saved data

'''
import sys
import pandas as pd

from systems.infection.unit import Unit
from systems.infection.world import World

load_dir = sys.argv[1]

agent_file = load_dir + '/save_agent_state0.csv'
df = pd.read_csv(agent_file)
gg = df.groupby('agent_index')
agents = []
for a_id, a_data in gg:
    belief_d = {}
    essence_d = {}
    resource_d = {}
    print (a_data)

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

    print (essence_d)
    print (agent.essence.keys())
    print (essence_val)
    agent.essence.set_values(essence_val)
    agent.resource.set_values(resource_val)
    agent.belief[b_key_1].set_values(belief_val)

    print (agent.essence._items)
    print (agent.resource._items)
    print (agent.belief)
    print (agent.belief['Surrounding'])

    agents.append(agent)
