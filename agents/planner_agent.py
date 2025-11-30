class PlannerAgent:
    def create_plan(self, topic):
        return [f"Step {i+1} for {topic}" for i in range(3)]
