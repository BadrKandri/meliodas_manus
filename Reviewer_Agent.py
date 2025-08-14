import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.exceptions import ModelProviderError
from tools import execute_code, file_operations, image_verif, pdf_verif, read_file_utf8, save_file_utf8, report_verif_2, insight_verif
from agno.agent import Agent
from pydantic import BaseModel, Field

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 

class Summary_Response(BaseModel):
    is_done: bool = Field(..., description="always set to False until if all tasks in the 'outputs/todo.md' are [ x ] then set is_done to True")
    
class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens

    def Review_Agent(self, result: str, decision: str, task: str):
        tools = [execute_code(), file_operations(), image_verif, pdf_verif, report_verif_2, insight_verif, read_file_utf8, save_file_utf8]
        return Agent(
            name="Review_Agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            response_model=Summary_Response,
            #debug_mode=True,
            instructions=[
                "You are a reviewing agent of an agentic system, your job is to review the outputs of other agents and edit the todo list.",
                "An orchestrator agent has called an agent to do a specific task so your job is to verify if the agent did his work or he failed, and check [ x ] the task accordingly in the 'todo.md' file present in the 'outputs' folder.",
                "workflow:",
                "1. First, read the 'outputs/todo.md' file to see the current tasks.",
                f"2. You need to verify if the {decision} agent completed its task successfully:",
                f"   - if {decision} == 'report_agent': Use the pdf_verif() or report_verif_2() tools to check if a PDF report exists in the outputs folder",
                f"   - if {decision} == 'plot_agent': Use image_verif() to check if plot images exist in the outputs folder",
                f"   - if {decision} == 'insight_agent': First use insight_verif() to check if results were saved to outputs folder. If no file was saved but the agent provided a valid answer in the response, still mark as completed. The insight agent completes its task by either saving results OR providing the answer.",
                "3. If the verification tools return True (meaning the task was completed successfully):",
                "   - Update the todo.md file by changing [  ] to [ x ] for the completed task",
                "   - Use the file_operations tool to modify the todo.md file",
                "4. After updating the todo.md file, read it again to check if ALL tasks are marked as [ x ]",
                "5. Set is_done to True ONLY if ALL tasks in todo.md are marked as [ x ], otherwise set is_done to False",
                "IMPORTANT RULES:",
                "- NEVER CHANGE THE TASK TEXT, only change [  ] to [ x ] if the task is completed",
                "- Use the verification tools to actually check if files exist",
                "- Always read and update the todo.md file using the file_operations tool",
                "- Only mark a task as done if the verification tools confirm success"
            ]
        )

if __name__ == "__main__":
    try:  
        agent_manager = AgentManager(model_name="gpt-4o", temperature=0.0, max_tokens=50000)
        agent = agent_manager.Review_Agent()
        response = agent.run("hello, plot me the carrots evolution over the years")
    except ModelProviderError as e:
        print("❌ OpenAI API quota exceeded.")