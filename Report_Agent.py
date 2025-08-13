import os 
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from tools import compile_latex, escape_latex, execute_code, file_operations,proper_write_latex
from agno.exceptions import ModelProviderError

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 

class Summary_Report_Response(BaseModel):
    my_json: str = Field(..., description="The json that contains the analysis of the Excel file")
    summary: str = Field(..., description="A human-readable paragraph depending on the user need")

class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens

    def create_Report_agent(self):
        tools = [ReasoningTools(), execute_code(), file_operations(), proper_write_latex, compile_latex, escape_latex]
        return Agent(
            name="Report_agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            #debug_mode=True,
            response_model=Summary_Report_Response,
            structured_outputs=True,
            instructions = [
                "You are an autonomous Excel report-generating agent.",
                "Your job is to create a professional PDF report based exactly on the user's request — no more, no less.",
                f"You will find everything in the outputs folder, which contains data (csv, json, images) extracted from an Excel file.",
                "Before generating, determine: does the user want a FULL report or only specific information?",
                "RULES:",
                "- If the user wants a FULL report: write a detailed report of at least 1000 words, covering all available data, charts, and images.",
                "- If the user asks for SPECIFIC information: only include that information. Keep it concise and exclude unrelated data.",
                "WORKFLOW:",
                "1. Look in the 'charts' and 'images' folders for relevant visual content, but only include those relevant to the request.",
                "2. Open 'report.tex' in the 'outputs' folder using the proper_write_latex tool.",
                "3. Use 'context.json', 'media.json', 'anomalies.json', and relevant images/charts to create LaTeX code for the report.",
                "4. Escape ALL text from JSON before inserting into LaTeX using escape_latex.",
                "5. When including images: use '../images/filename' for images, and '../charts/filename' for charts. Only include them if relevant.",
                "6. Respect report_specifications in JSON if provided.",
                "7. Call compile_latex('report.tex') to create 'report.pdf' in the 'outputs' folder.",
                "DO NOT:",
                "- Include unrelated data.",
                "- Mention missing images/charts.",
                "- Merge unrelated tables."
            ]

        )
    
if __name__ == "__main__":
    try:
        agent_manager = AgentManager(model_name="gpt-4o", temperature=0.1, max_tokens=10000)
        agent = agent_manager.create_Report_agent()
        response = agent.run(input("HELLO, i am Meliodas Manus Agent how can i help you?\n===> "))

    except ModelProviderError as e:
        print("❌ OpenAI API quota exceeded.")
