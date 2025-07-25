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



class AgentStuff():
    def __init__(self):
        self.state = AgentState()
        self.state.captured = None



async def render_pydantic(deps: AgentStuff):
    with st.chat_message("assistant"):
        with st.container(border = True):
            test = MyModel(name="John Doe", age=30, has_pets=True)
            result = sp.pydantic_form(model=test, key="my_model_input")
            if result:
                logger.info(f"Captured data: {result}")
                deps.state.captured = result
                st.success("Data received successfully!")
                st.rerun()



agent = Agent('gpt-4o')

@agent.tool
async def capture_pydantic_input(ctx: RunContext):
    """Capture user input using Pydantic and render it in a dialog."""
    await call_render_func('render_pydantic', {"deps": ctx.deps})
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