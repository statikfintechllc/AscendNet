def check_for_loops(task_log):
    return any("retry" in t for t in task_log[-10:])
