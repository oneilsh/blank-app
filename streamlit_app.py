import streamlit as st
from pydantic_ai import Agent, RunContext
from opaiui.app import AppConfig,  AgentConfig, AgentState, serve, call_render_func, get_logger
import streamlit_pydantic as sp
from pydantic import BaseModel
from models import MyModel

import dotenv
dotenv.load_dotenv(override=True)

logger = get_logger()


class AgentStuff():
    def __init__(self):
        self.state = AgentState()
        self.state.captured = None



async def render_pydantic(deps_state: AgentState, input: MyModel):
    with st.chat_message("assistant"):
        with st.container(border = True):
            result = sp.pydantic_form(model=input, key="my_model_input")
            if result:
                logger.info(f"Captured data: {result}")
                logger.info(f"state before: {deps_state.captured}")
                deps_state.captured = result.model_dump()
                logger.info(f"state after: {deps_state.captured}")
                st.success("Data received successfully!")
                st.rerun()



agent = Agent('gpt-4o')

@agent.tool
async def capture_pydantic_input(ctx: RunContext, input: MyModel):
    """Capture user input using Pydantic and render it in a dialog."""
    await call_render_func('render_pydantic', {"deps_state": ctx.deps.state, "input": input})
    return "A user interface has been rendered in the chat for the user to enter data."


async def render_sidebar(deps):
    st.write(deps.state.captured)


app_config = AppConfig(
    rendering_functions=[render_pydantic]
)

agent_configs = {
    "Agent": AgentConfig(
        agent = agent,
        deps = AgentStuff(),
        sidebar_func= render_sidebar,
    )
}


serve(app_config, agent_configs)