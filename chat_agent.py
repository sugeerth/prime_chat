from langchain.llms import openai
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st


class ChatAgent:
    def __init__(self, llm_api_key, model_name: str):
        # self.llm = openai(temperature=0, streaming=True, llm_api_key)
        self.llm = ChatOpenAI(temperature=0.7,  model=model_name, api_key=llm_api_key, streaming = True)
        self.tools = load_tools(["ddg-search"])
        self.agent = initialize_agent(
            self.tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )
    
    def get_agent(self):
        return self.agent
    
    def initialize_chat(self):
        if prompt := st.chat_input():
            st.chat_message("user").write(prompt)
            with st.chat_message("assistant"):
                st_callback = StreamlitCallbackHandler(st.container())
                response = self.agent.run(prompt, callbacks=[st_callback])
                st.write(response)