import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.exceptions import ModelProviderError
from tools import execute_code, file_operations, image_verif, pdf_verif

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 
        
class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens

    def Review_Agent(self, result: str, decision: str, task: str):
        tools = [execute_code(), file_operations(), image_verif, pdf_verif]
        return Agent(
            name="Review_Agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            #debug_mode=True,
            instructions=[
                "You are a reviewing agent of an agentic system, your job is to review the outputs of other agents and edit the todo list.",
                "an orchestrator agent has called an agent to do a specific task so your job is to verify if the agent did his work or he failed, and check [ x ] the task accordingly in the 'todo.md' file present in the 'outputs' folder.",
                f"if {decision} == 'insight_agent' you should see {task} and {result} and see if the {result} is relevant to the {task} and if it is correct, if yes check [ x ] the task in the todo list",
                f"if {decision} == 'plot_agent' use image_verif() to check if the plot images exist in the outputs folder, if yes check [ x ] the task in the todo list",
                f"if {decision} == 'report_agent' use pdf_verif() to check if the report PDF exists in the outputs folder, if yes check [ x ] the task in the todo list",

                "your should decide to check [ x ] the task if its done in the 'outputs/todo.md' folder",
                "if the agent failed doing a task don't change nothing in the todo.md",
                "NEVER CHANGE THE WORKFLOW OF THE TODO LIST JUST ADD [ x ] IF the task is DONE"
            ]
        )

if __name__ == "__main__":
    try:  
        agent_manager = AgentManager(model_name="gpt-4o", temperature=0.1, max_tokens=50000)
        agent = agent_manager.Review_Agent()
        response = agent.run("hello, plot me the carrots evolution over the years")
    except ModelProviderError as e:
        print("❌ OpenAI API quota exceeded.")