import numpy as np
import numpy.random
np.random.seed(79)

from core.agent_ms import AgentManagementSystem

from core.agent import Agent
from core.organs import Sensor, Cortex
from core.array import Buzz, Feature, Essence

class TestAgentMS(AgentManagementSystem):

    def type_query(self, agent_index):

        neighbours = self.neighbours_to(agent_index)

        the_other_agent = neighbours.pop()
        feature_return = the_other_agent.tickle('my_type')
        
        revealed_type = feature_return['revealed_type']

        if self[agent_index].essence['my_mood'] < 0.25:
            honest_assessment = 0.2
        elif self[agent_index].essence['my_mood'] < 0.55:
            honest_assessment = 0.5
        else:
            honest_assessment = 1.0

        return revealed_type, honest_assessment 

    def __init__(self, name, agents_init):

        super().__init__(name, agents_init)

        for agent, aux_content in self:
            buzz = Buzz('type_discovery', ('type_sense', 'honesty_sense'))
            sensor = Sensor('discover_neighbour_type', 'neighbour_type_query', self.type_query, buzz)
            feature = Feature('revealed_type', ('revealed_type',))
            essence = Essence('who_am_i', ('my_type', 'my_mood'))
            cortex = Cortex('my_type', essence, agent.reveal_type, feature)
            agent.set_organ_bulk([sensor, cortex])

            essence.set_values([np.random.random(), np.random.random()])
            agent.set_scaffold(essence)

class TestAgent(Agent):

    def reveal_type(self, the_type, parameter):
        return the_type 


agents_init = [TestAgent('LEFT'), TestAgent('RIGHT')]
agent_ms = TestAgentMS('pair_of_agents', agents_init)

for agent, aux_content in agent_ms:
    agent.sense('discover_neighbour_type')
    print (list(agent.buzz.values())[0])
