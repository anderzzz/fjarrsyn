'''Main runner routine for cooperative and trust growers

'''
from core.simulator import FiniteSystemRunner
from core.sampler import AgentSampler, EnvSampler, SystemIO

from unit import Unit, AgentAuxEnv
from world import World

u1 = Unit('test0', 0.5, 0.8, 0.0, 1.0, 0.0, 0.0)
u2 = Unit('test1', 0.5, 0.8, 0.0, 0.0, 0.0, 0.0)

env_agent = [AgentAuxEnv(0.0, 0.0, 0.0, 0.0), AgentAuxEnv(0.5, 0.5, 0.5, 0.0)]

ww = World('test_world', [u1, u2], env_agent)

u1.sense('Feel Neighbour Surface')
u1.interpret('Friendly Environment')
u1.mould('Share Resources')
u1.act('Share Resources to Neighbours')

for nn in ww:
    print (nn)
    print (nn.agent_content, nn.aux_content.container)
