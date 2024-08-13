from langchain_openai import ChatOpenAI
import os, pathlib
gpt_4o = "gpt-4o"
claude_model = "claude"

from dotenv import load_dotenv
load_dotenv(pathlib.Path(__file__).parent.parent / '.env')

def get_openai_llm():
    return ChatOpenAI(model_name=gpt_4o)
