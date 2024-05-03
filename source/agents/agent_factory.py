from agents.answer_agent import AnswerAgent
from agents.reflection_agent import ReflectionAgent

class AgentFactory:

    def create(self, agent_type, model, topic):

        # Create the agent
        if agent_type in ["baseline", "retry", "keywords", "advice", "explanation", "instructions", "solution", "composite", "unredacted"]:
            return AnswerAgent(model, topic)

        elif agent_type == "reflection":
            return ReflectionAgent(model, topic)

        else:
            raise Exception(f"Unknown agent type: {agent_type}")
        