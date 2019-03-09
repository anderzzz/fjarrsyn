'''Main runner routine for cooperative and trust growers

'''
from core.simulator import FiniteSystemRunner
from core.sampler import AgentSampler, EnvSampler, SystemIO

from unit import Unit

u1 = Unit('test', 0.5, 0.8, 0.0, 1.0, 0.0, 0.0)
xx = u1.tickle('Reveal Cooperation')
print (xx)
