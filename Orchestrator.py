from dotenv import load_dotenv
import os
from agno.models.openai import OpenAIChat
from tools import execute_code, file_operations
from Report_Agent import AgentManager as ReportManager
from Insight_Agent import AgentManager as InsightManager
from Plot_Agent import AgentManager as PlotManager
from agno.agent import Agent
from pydantic import BaseModel, Field
from pathlib import Path
from agno.exceptions import ModelProviderError

# Create your sub-agent
report_agent = ReportManager("gpt-4o", 0.1, 50000).create_Report_agent()
insight_agent = InsightManager("gpt-4o", 0.1, 50000).create_Insight_agent()
plot_agent = PlotManager("gpt-4o", 0.1, 50000).create_Plot_Agent()

class Summary_Response(BaseModel):
    chosen_agent: str = Field(..., description="the name of the agent you chose, report_agent, insight_agent, plot_agent")
    is_done: bool = Field(..., description="always set to False until if all tasks in the 'outputs/todo.md' are [v] then set is_done to True")
    status: str = Field(..., description="a description of what the agent called did, succeeded his task or it failed")
    task: str = Field(..., description="the task that was assigned to the agent")

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 

todo_path = Path("outputs/todo.md")


class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens

    def Orchestrator_Agent(self):
        tools = [execute_code(), file_operations()]
        return Agent(
            name="Orchestrator_Agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            response_model=Summary_Response,
            structured_outputs=True,
            #debug_mode=True,
            instructions=[
                "You are An Orchestrator Agent you have 3 agents at your disposal, Your Job is to chose the correct agent depending on the task.",
                "you will find the todo tasks in the 'outputs/todo.md' file you should always execute it line by line",
                "you select only 1 task from the todo list never try to select more than 1",
                "If query is about generating reports → set chosen_agent to report_agent",
                "If query is a question that needs analysis to be answered → set chosen_agent to insight_agent",
                "If query is about plotting data → set chosen_agent to plot_agent",
                "How to choose the next task:"
                "SO IMPORTANT: if you find a task [  ] this is the next task."
                "if you find a task done [ x ] this task is done move to the next one"
                "if all tasks are [ x ] set is_done to True",
                "never move the next task until the task before is done [ x ]"
                "after choosing the task you should put it in task",
                "IMPORTANT: 1 and only 1 agent should be called",
            ]
)
def run_agent(query, decision):
    if decision == "report_agent":
        report_response=report_agent.run(query)
        result= report_response.content
        print("📊 Report Agent Done")
    elif decision == "insight_agent":
        insight_response = insight_agent.run(query)
        result = insight_response.content
        print("🔍 Insight Agent response:", insight_response.content)
    elif decision == "plot_agent":
        plot_response = plot_agent.run(query)
        result = plot_response.content
        print("📈 Plot Agent Done")
    return result

def orchestrator(query):
    try:  
        orchestrator_agent = AgentManager("gpt-4o", 0.1, 50000).Orchestrator_Agent()
        response = orchestrator_agent.run()
        decision = response.content.chosen_agent.lower()
        is_done = response.content.is_done
        task = response.content.task
        print("Orchestrator decision:", decision)

        agents_output = run_agent(query, decision)
    except ModelProviderError as e:
        print("❌ OpenAI API quota exceeded.")

    return decision, is_done, agents_output, task
