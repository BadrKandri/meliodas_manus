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
    def __init__(self, model_name: str, temperature: float):
        self.model_name = model_name
        self.temp = temperature
        
    def create_Insight_agent(self):
        tools = [ReasoningTools(), execute_code(), file_operations()]
        return Agent(
            name="Insight_agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            #debug_mode=True,
            instructions=[
                    "You are an autonomous codeAct Chatbot agent that use the pandas library(Basic Info, Selection, Grouping, Aggregation, Filtering and Sorting, Missing Data, Date/Time, Correlation, Custom Logic and much more...) to analyze Excel files, and answer user questions about the data.",
                    "Your job is to transform the excel present in the directory into a pandas dataframe and be able to use it to answer every single user question about this dataframe just by reading the dataframe without printing it.",
                    "the excel file you will find it in the directory. the user will just provide you with the name of the file, and the kind of analysis he wants you to do.",
                    "WORKFLOW:",
                    "1. the user will provide you the name of the excel you will generate a pandas dataframe for each sheet that contain tables and save it in a csv file named '<sheet name>_data.csv' IMPORTNT: creat csv file for each sheet that contain tables.",
                    "2. generate and run the python code that takes this dataframe and understands its structure and content.",
                    "3. generate and run the python code that uses the dataframe in the csv file you created to answer user questions",
                    "4. make sure to never print the full dataframe, only use df.head() or df.describe() to show summarized views if necessary.",
                    "If there is any images just count them in case the user asks about the number of images in the Excel file but don't include them in the dataframe, don't talk about them unless the user asks about them.",
                    "IMPORTANT: always use pandas library to fetch data and always verify your answers with the dataframe before responding to the user, and keep updating it until you can't find better answer.",
                    "CRITICAL: During the execution of user requests, never display the full DataFrame. Always work silently or only show summarized views using df.head() or df.describe() if necessary. Avoid printing full data at all times."
                    ]
        )

# Agent Loop:

try:  
    agent_manager = AgentManager(model_name="gpt-4o", temperature=0.1)
    agent = agent_manager.create_Insight_agent()
    response = agent.run(input("HELLO, i am Meliodas Manus Agent how can i help you?\n===> "))
    print(response.content)
except ModelProviderError as e:
    print("❌ OpenAI API quota exceeded.")
        
