import os 
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools import tools
from agno.tools.reasoning import ReasoningTools

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 

# Load instructions from a file
with open("prompt.txt", "r", encoding="utf-8") as file:
    prompt_instructions = file.read()
    
    
tools.append(ReasoningTools())    
    
agent = Agent(model=OpenAIChat("gpt-4o") , tools=tools , instructions= prompt_instructions) 

while(True) : 
    query = input("what do you want from the agent? : ")
    if query.lower() in ["exit" , "quit"] : 
        break 
    agent.print_response(query , stream=True)
