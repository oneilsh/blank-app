import streamlit as st
from pydantic_ai import Agent, RunContext
from opaiui.app import AppConfig,  AgentConfig, AgentState, serve, call_render_func, get_logger
import streamlit_pydantic as sp
from pydantic import BaseModel

import dotenv
dotenv.load_dotenv(override=True)

logger = get_logger()


class MyModel(BaseModel):
    name: str
    age: int
    has_pets: bool



async def render_pydantic():
    with st.container(border = True):
        result = sp.pydantic_input(model=MyModel, key="my_model_input")
        if result:
            st.json(result)
            st.success("Data received successfully!")



agent = Agent('gpt-4o')

@agent.tool
async def capture_pydantic_input(ctx: RunContext):
    """Capture user input using Pydantic and render it in a dialog."""
    await call_render_func('render_pydantic', {})
    return "A user interface has been rendered in the chat for the user to enter data."

app_config = AppConfig(
    rendering_functions=[render_pydantic]
)

agent_configs = {
    "Agent": AgentConfig(
        agent = agent,
        deps = None,
    )
}


serve(app_config, agent_configs)