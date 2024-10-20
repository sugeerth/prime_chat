Prime Health 

MVP of a AI agent to manage diabetes plans. 

Setup:
pip install requirements:
  streamlit
  openai
  langchain

To run:
set up secrets file:
  1) Add folder .streamlit in root if not exists
  2) Add secrets.toml file in .streamlit folder if not exists
     OpenAI_key = "<LLM_PROVIDER_KEY>"
     Vectara_api_key = "<corpus_key_general>"
     Vectarakey_diabetes_pan_api_key = "<corpus_key_plan>"
     
Go to root and run:> streamlit run search_and_chat.py
  
