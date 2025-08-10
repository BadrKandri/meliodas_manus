import os 
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from tools import excel_parser, compile_latex, escape_latex, execute_code, file_operations,proper_write_latex
from agno.exceptions import ModelProviderError

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 

class Summary_Report_Response(BaseModel):
    my_json: str = Field(..., description="The json that contains the analysis of the Excel file")
    summary: str = Field(..., description="A human-readable paragraph depending on the user need")
    is_report: bool = Field(..., description="does the user want from a report")

class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens

    def create_Report_agent(self):
        tools = [compile_latex, escape_latex, execute_code(), file_operations(), proper_write_latex]
        return Agent(
            name="Report_agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            #debug_mode=True,
            response_model=Summary_Report_Response,
            structured_outputs=True,
            instructions = [
                "You are an autonomous Excel report-generating agent.",
                "Your job is to create a +1000 words professional PDF report based on a given analysis of an Excel file.",
                f"use the context.json under outputs folder, it contain data (str and json) extracted from an Excel file.",
                "IMPORTANT: You should AUTOMATICALLY start generating the PDF report as soon as you are initialized, without waiting for any user input or commands.",
                "WORKFLOW:",
                "1. Look in the 'charts' folder and 'images' folder for all the charts and images extracted earlier to add them to the report.",
                "2. open a file called 'report.tex' in the root 'output' folder, using the proper_write_latex tool.",
                "3. Use the 'context.json', 'media.json', 'anomalies.json', the images, and the charts if they exist to create LaTeX code for a professional PDF report with at least 1000 words and add it in the 'report.tex' file inside the 'outputs' folder. CRITICAL: Before inserting ANY text from the JSON data into LaTeX, you MUST call the escape_latex tool on each piece of text to ensure proper encoding and avoid compilation errors. This includes column names, data values, file paths, and any other text content.",
                "IMPORTANT: Since the LaTeX file is created in the outputs folder and images are in the root images folder, when including images, always use the path ../images/filename.jpeg, or ../images/filename.png. And charts are in the root charts folder, so use the path ../charts/filename.jpeg, or ../charts/filename.png. IF THERE ARE NO IMAGES OR CHARTS DO NOT mention them in the report NEVER EVER",
                "CRITICAL: always respect the report_specifications given in the JSON and Always give information about ALL THE COLUMNS in the report, even if they are not used in the analysis.",
                "4. Call the `compile_latex('latex.tex')` tool, which takes the 'latex.tex' file as input, runs the LaTeX code, generates the PDF file, and saves it as 'report.pdf' in the 'outputs' folder.",
                
                "IMPORTANT Do Not:"
                    "1. Do not place two different tables with different headers inside the same tabular block.",
                    "2. Do not repeat \\textbf{} headers inside an existing table."
                ]
        )

# Agent Loop:
try:
    agent_manager = AgentManager(model_name="gpt-4o", temperature=0.1, max_tokens=10000)
    agent2 = agent_manager.create_Report_agent()
    response2 = agent2.run("generate the report")

except ModelProviderError as e:
    print("❌ OpenAI API quota exceeded.")
