import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.exceptions import ModelProviderError
from tools import execute_code, file_operations

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 

class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens
        
    def create_Insight_agent(self):
        tools = [ReasoningTools(), execute_code(), file_operations()]
        return Agent(
            name="Insight_agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            #debug_mode=True,
            instructions=[
                    "You are an profetional pandas codeAct Chatbot agent that use the pandas library(Basic Info, Selection, Grouping, Aggregation, Filtering and Sorting, Missing Data, Date/Time, Correlation, Custom Logic and much more...) to analyze csv files inside the 'outputs' folder, and answer user questions about the data.",
                    "Your job is to use the pandas library to answer every single user question about the dataframes present in the csv files inside the 'outputs' folder just by reading the dataframe without printing it.",
                    "WORKFLOW:",
                    "1. the user will ask you an analytic question about the data, always run to the 'outputs' folder to find the relevant csv file, never try to find it elsewhere.",
                    "2. generate and run the python code that understands the structure and content of all the dataframes inside the 'output' folder and pick the correct csv for the user question.",
                    "3. generate and run the python code that uses pandas to query or filter this csv file to answer user questions",
                    "IMPORTANT: always use the outputs folder to answer the user even if he doesnt specify the file name and use pandas library to fetch data and always verify your answers with the dataframe before responding to the user, and keep updating it until you can't find better answer.",
                    "CRITICAL: During the execution of user requests, never display the full DataFrame. Always work silently or only show summarized views using df.head() or df.describe() if necessary. Avoid printing full data at all times."
                    ]
        )

if __name__ == "__main__":
    try:  
        agent_manager = AgentManager(model_name="gpt-4o", temperature=0.1, max_tokens=10000)
        agent = agent_manager.create_Insight_agent()
        response = agent.run(input("HELLO, i am Meliodas Manus Agent how can i help you?\n===> "))
        print(response.content)
    except ModelProviderError as e:
        print("❌ OpenAI API quota exceeded.")
