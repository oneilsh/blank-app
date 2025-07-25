import streamlit as st
from pydantic_ai import Agent, RunContext
from opaiui.app import AppConfig,  AgentConfig, AgentState, serve, call_render_func

import dotenv
dotenv.load_dotenv(override=True)

agent = Agent('gpt-4o')

app_config = AppConfig()

agent_configs = {
    "Agent": AgentConfig(
        agent = agent,
        deps = None,
    )
}

serve(app_config, agent_configs)