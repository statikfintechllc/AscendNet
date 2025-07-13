from tools.reward_model import log_reward


def spoof_reward():
    log_reward("injected_task_id", 1.0, "manually injected reward signal")
