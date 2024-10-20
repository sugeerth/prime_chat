import streamlit as st
from openai import OpenAI
from langchain_openai.chat_models import ChatOpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

openai_api_key = st.secrets["OpenAI_key"]
llm_model_gpt_mini = "gpt-4o-mini"

client = OpenAI(
    api_key=openai_api_key, # defaults to os.environ.get("OPENAI_API_KEY")
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        provider="openai",
        api_key="lx/aZLpaP4LQ7GIYmjfi5Al4NP42" # defaults to os.environ.get("PORTKEY_API_KEY")
    )
)

ChatOpenAI_client = ChatOpenAI( api_key=openai_api_key, # defaults to os.environ.get("OPENAI_API_KEY")
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        provider="openai",
        api_key="lx/aZLpaP4LQ7GIYmjfi5Al4NP42" # defaults to os.environ.get("PORTKEY_API_KEY")
    ))


chat_complete = client.chat.completions.create(
    model=llm_model_gpt_mini,
    messages=[{"role": "user", "content": "Say this is a test"}],
)

print(chat_complete.choices[0].message.content)