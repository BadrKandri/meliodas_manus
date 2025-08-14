import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.exceptions import ModelProviderError
from tools import execute_code, file_operations,save_file_utf8, read_file_utf8

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 
        
class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens

    def Planner_Agent(self, query, excel_path):
        tools = [execute_code(), file_operations(), save_file_utf8, read_file_utf8]
        return Agent(
            name="Planner_Agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            #debug_mode=True,
            instructions=[
                "You are a planning agent of an agentic system, your job is to create a todo list for the orchestrator agent from the user query",
                "there is 3 agents in this agentic system a report agent that generates reports, a plot agent that use plotly to creat plots depending on the user needs and an Insight agent that use pandas to answer the user questions about the data, the report agent should always be the last choice",
                "the user will some times ask for a simple task that needs one agent but some times he will ask for a task that needs multiple agent calls",
                "you will find all the data you will need in a folder named 'outputs' in the same directory it contain: the data frames in csv format, and a 'context.json' file that has all the relevant information about the excel file present in the 'excels' folder,so never add the extracting step in the todo list",
                "this is the structure of the project:",
                "project_root/",
                "│",
                "├── excels/",
                "│   ├── .gitkeep",
                "│   └── <the excel file name>.xlsx",
                "│",
                "├── outputs/",
                "│   ├── .gitkeep",
                "│   ├── anomalies.json",
                "│   ├── context.json",
                "│   ├── <the csv of the tablea from the excel file>.csv",
                "│   └── media.json",
                
                "WORKFLOW:",
                "1. concider yourself as a CEO that got an offer and he needs to devide the work between his employes, use this mentality to analyze and understand the user query",
                "2. separate the work depending on the agents you have and create a todo list and add it to the 'todo.md' file and store it in the 'outputs' folder",
                "3. always add the location of the task output if the next task will need that output( exemple: [  ] 3. call the report agent and don't forget to add the image generated in the task number 2 'it is in the outputs folder' to the report)",
                "IMPORTANT: You should obligatorily call 1 and only 1 agent at the minimum in each step AND ALWAYS MINIMISE THE TASKS 3 TASKS MAX",
                "3. ALWAY RESPECT THIS SYNTAX IN THE TODO LIST :[  ] 1. call the x agent and ask it to do xxx using the data from the available xxx.file_type files in the 'outputs' folder and store the result in the 'outputs' folder",
                "RESPECT THIS: Never call the insight agent to perform something that you can do directly by calling an other agent"
                
            ]
        )

if __name__ == "__main__":
    try:  
        agent_manager = AgentManager(model_name="gpt-4o", temperature=0.1, max_tokens=50000)
        agent = agent_manager.Planner_Agent(query="hello, plot me the carrots evolution over the years")
        response = agent.run("hello,generate me a report that contain a plot of the carrots evolution over the years")
    except ModelProviderError as e:
        print("❌ OpenAI API quota exceeded.")