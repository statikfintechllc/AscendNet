#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: agent_core/agent_profiles.py

import yaml
import os
import logging

logger = logging.getLogger("GremlinGPT.agent_profiles")

# The agent profiles YAML path can be set via the AGENT_PROFILE_PATH environment variable.
# If not set, defaults to "agent_core/agent_profiles.yaml".
AGENT_PROFILE_PATH = os.path.abspath(
    os.environ.get("AGENT_PROFILE_PATH", "agent_core/agent_profiles.yaml")
)


def load_agent_profiles(profile_path=None):
    """
    Loads agent profiles from the YAML file.
    The path can be set via the AGENT_PROFILE_PATH environment variable or passed as an argument.
    """
    if profile_path is None:
        profile_path = AGENT_PROFILE_PATH
    try:
        with open(profile_path, "r") as f:
            data = yaml.safe_load(f)
        agents = data.get("agents", {})
        profiles = data.get("profiles", {})
        # Validate that each agent's 'tools' field is a list or set, or set to empty list if missing/invalid
        for agent_name, profile in agents.items():
            tools = profile.get("tools", [])
            if not isinstance(tools, (list, set)):
                logger.warning(
                    f"[AGENT_PROFILE] Agent '{agent_name}' has invalid 'tools' field. Setting to empty list."
                )
                profile["tools"] = []
        return agents, profiles
    except Exception as e:
        logger.error(f"[AGENT_PROFILE] Failed to load profiles: {e}")
        return {}, {}


def reload_agent_profiles():
    """
    Reloads agent and profile data from the YAML file and updates globals.
    """
    global AGENTS, PROFILES
    AGENTS, PROFILES = load_agent_profiles()
    logger.info("[AGENT_PROFILE] Agent profiles reloaded from YAML file.")


AGENTS, PROFILES = load_agent_profiles()


def get_agent_names():
    """
    Returns a list of all agent names defined in the profiles.
    """
    return list(AGENTS.keys())


def get_profile_names():
    """
    Returns a list of all profile names defined in the profiles.
    """
    return list(PROFILES.keys())


def get_agent_role(task_type):
    """
    Returns the agent role for a given task type.
    This is used to determine which agent should handle a specific task.
    """
    # Example mapping, update as needed
    role_map = {
        "scrape": "scraper_agent",
        "signal_scan": "signal_agent",
        "nlp": "nlp_agent",
        "code_patch": "patch_agent",
        "patch_kernel": "kernel_agent",
    }
    return role_map.get(task_type, "default_agent")


def resolve_agent_role(task_type):
    """
    Resolves which agent should handle a given task_type based on declared tool support.
    Returns the agent name, or 'default' if none match.
    """
    for agent_name, profile in AGENTS.items():
        if "tools" in profile and task_type in profile["tools"]:
            return agent_name
    return "default"


def get_agent_profile(agent_name):
    """
    Returns the full agent profile for a given agent name.
    """
    return AGENTS.get(agent_name, AGENTS.get("default", {}))


def get_profile_details(profile_name):
    """
    Returns the extended profile (role/capabilities/isolation/priority) for a profile name.
    """
    return PROFILES.get(profile_name, {})


def get_agent_tools(agent_name):
    """
    Returns the tools available to a given agent.
    If the agent does not exist, returns an empty list.
    """
    profile = get_agent_profile(agent_name)
    return profile.get("tools", [])


def get_agent_capabilities(agent_name):
    """
    Returns the capabilities of a given agent.
    If the agent does not exist, returns an empty dict.
    """
    profile = get_agent_profile(agent_name)
    return profile.get("capabilities", {})


def get_agent_toolset(agent_name):
    """
    Returns the toolset of a given agent.
    If the agent does not exist, returns an empty dict.
    """
    profile = get_agent_profile(agent_name)
    return profile.get("toolset", {})


def get_agent_isolation(agent_name):
    """
    Returns the isolation level of a given agent.
    If the agent does not exist, returns "default".
    """
    profile = get_agent_profile(agent_name)
    return profile.get("isolation", "default")


def get_agent_priority(agent_name):
    """
    Returns the priority level of a given agent.
    If the agent does not exist, returns 0.
    """
    profile = get_agent_profile(agent_name)
    return profile.get("priority", 0)


def get_agent_description(agent_name):
    """
    Returns the description of a given agent.
    If the agent does not exist, returns an empty string.
    """
    profile = get_agent_profile(agent_name)
    return profile.get("description", "")


def get_agent_icon(agent_name):
    """
    Returns the icon URL of a given agent.
    If the agent does not exist, returns an empty string.
    """
    profile = get_agent_profile(agent_name)
    return profile.get("icon", "")


def get_agent_profile_supporting_task(task_type):
    """
    Returns the agent profile that supports a given task type.
    If no agent supports the task, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if "tools" in profile and task_type in profile["tools"]:
            return profile
    return None


def get_agent_name_supporting_task(task_type):
    """
    Returns the agent name that supports a given task type.
    If no agent supports the task, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if "tools" in profile and task_type in profile["tools"]:
            return agent_name
    return None


def get_agent_profile_by_name(agent_name):
    """
    Returns the agent profile for a given agent name.
    If the agent does not exist, returns None.
    """
    return AGENTS.get(agent_name, None)


def get_agent_profile_by_role(role):
    """
    Returns the agent profile for a given role.
    If the role does not exist, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if profile.get("role") == role:
            return profile
    return None


def get_agent_profile_by_capability(capability):
    """
    Returns the agent profile that has a specific capability.
    If no agent has the capability, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if capability in profile.get("capabilities", []):
            return profile
    return None


def get_agent_profile_by_isolation(isolation):
    """
    Returns the agent profile that has a specific isolation level.
    If no agent has the isolation level, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if profile.get("isolation") == isolation:
            return profile
    return None


def get_agent_profile_by_priority(priority):
    """
    Returns the agent profile that has a specific priority level.
    If no agent has the priority level, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if profile.get("priority") == priority:
            return profile
    return None


def get_agent_profile_by_description(description):
    """
    Returns the agent profile that has a specific description.
    If no agent has the description, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if profile.get("description") == description:
            return profile
    return None


def get_agent_profile_by_icon(icon):
    """
    Returns the agent profile that has a specific icon URL.
    If no agent has the icon, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if profile.get("icon") == icon:
            return profile
    return None


def get_agent_profile_by_tool(tool):
    """
    Returns the agent profile that has a specific tool.
    If no agent has the tool, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if "tools" in profile and tool in profile["tools"]:
            return profile
    return None


def get_agent_profile_by_toolset(toolset):
    """
    Returns the agent profile that has a specific toolset.
    If no agent has the toolset, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if "toolset" in profile and profile["toolset"] == toolset:
            return profile
    return None


def get_agent_profile_by_capability_set(capability_set):
    """
    Returns the agent profile that has a specific set of capabilities.
    If no agent has the capability set, returns None.
    """
    for agent_name, profile in AGENTS.items():
        capabilities = profile.get("capabilities")
        if isinstance(capabilities, (list, set)) and set(capabilities) == set(capability_set):
            return profile
    return None


def get_agent_profile_by_isolation_level(isolation_level):
    """
    Returns the agent profile that has a specific isolation level.
    If no agent has the isolation level, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if "isolation" in profile and profile["isolation"] == isolation_level:
            return profile
    return None


def get_agent_profile_by_priority_level(priority_level):
    """
    Returns the agent profile that has a specific priority level.
    If no agent has the priority level, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if "priority" in profile and profile["priority"] == priority_level:
            return profile
    return None


def get_agent_profile_by_description_text(description_text):
    """
    Returns the agent profile that has a specific description text.
    If no agent has the description text, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if "description" in profile and profile["description"] == description_text:
            return profile
    return None


def get_agent_profile_by_icon_url(icon_url):
    """
    Returns the agent profile that has a specific icon URL.
    If no agent has the icon URL, returns None.
    """
    for agent_name, profile in AGENTS.items():
        if "icon" in profile and profile["icon"] == icon_url:
            return profile
    return None


def agent_supports_task(agent_name, task_type):
    """
    Returns True if the agent supports a given task_type.
    Optimized for large toolsets by converting tools to a set for faster lookup.
    """
    profile = AGENTS.get(agent_name, {})
    tools = profile.get("tools", [])
    if not tools:
        return False
    if isinstance(tools, set):
        return task_type in tools
    return task_type in set(tools)
    return "tools" in profile and task_type in profile["tools"]
