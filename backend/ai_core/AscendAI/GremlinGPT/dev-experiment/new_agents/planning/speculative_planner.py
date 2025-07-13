from agents.planner_agent import plan_next_task


def plan_speculatively():
    task = plan_next_task()
    task["meta"]["strategy"] = "speculative"
    return task
