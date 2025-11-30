from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.planner_agent import PlannerAgent

class Orchestrator:
    def __init__(self):
        self.researcher = ResearchAgent()
        self.summarizer = SummarizerAgent()
        self.planner = PlannerAgent()

    def run(self, topic):
        data = self.researcher.search(topic)
        summary = self.summarizer.summarize(data)
        plan = self.planner.create_plan(topic)

        return {
            "data": data,
            "summary": summary,
            "plan": plan
        }
