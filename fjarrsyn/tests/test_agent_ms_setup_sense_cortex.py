'''Integration test of AMS where the two agents can sense each others cortices

'''
import pytest

from fjarrsyn.core.agent_ms import AgentManagementSystem

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.instructor import Sensor, Cortex
from fjarrsyn.core.message import Buzz, Feature, Essence

REF_VALUES = [[('type_sense', 0.50078), ('honesty_sense', 0.5)],
              [('type_sense', 0.50067), ('honesty_sense', 0.2)]]

FLOATPOOL = [0.5006681263403812,0.4680674259481151,0.5007825256422324,0.14917816545210816]

class XTestAgentMS(AgentManagementSystem):

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

        for node in self:
            agent = node.agent_content
            buzz = Buzz('type_discovery', ('type_sense', 'honesty_sense'))
            sensor = Sensor('discover_neighbour_type', self.type_query, buzz,
                            agent_id_to_engine=True)
            feature = Feature('revealed_type', ('revealed_type',))
            essence = Essence('who_am_i', ('my_type', 'my_mood'))
            cortex = Cortex('my_type', agent.reveal_type, essence, feature)
            agent.set_organs(sensor, cortex)

            essence.set_values([FLOATPOOL.pop(0), FLOATPOOL.pop(0)])
            agent.set_scaffold(essence)
            print (agent.essence.values())

class XTestAgent(Agent):

    def reveal_type(self, the_type, parameter):
        return the_type 

def test_main():
    agents_init = [XTestAgent('LEFT', strict_engine=True), XTestAgent('RIGHT', strict_engine=True)]
    agent_ms = XTestAgentMS('pair_of_agents', agents_init)

    cnt = 0
    for node in agent_ms:
        agent = node.agent_content
        agent.sense('discover_neighbour_type')
        the_buzz = agent.buzz['type_discovery']

        xx = the_buzz['type_sense']
        yy = the_buzz['honesty_sense']

        assert (xx == pytest.approx(REF_VALUES[cnt][0][1], abs=1e-5))
        assert (yy == pytest.approx(REF_VALUES[cnt][1][1], abs=1e-5))

        cnt += 1
