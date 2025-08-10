import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.exceptions import ModelProviderError
from tools import execute_code, file_operations
from tools import execute_code, file_operations,read_file_utf8,save_file_utf8

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 
        
class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens

    def create_Context_Agent(self):
        tools = [execute_code(), file_operations(), read_file_utf8, save_file_utf8]
        return Agent(
            name="Context_Agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            #debug_mode=True,
            instructions=[
                "You are an autonomous Excel analysis agent. You always start with thinking and understanding the excel file present in the 'excels' folder.",
                "Your job is to read *without printing* the Excel files present in the 'excels' folder + the anomalies.json file and the csv files present in the 'outputs' folder + images and charts in the images and charts folders to generate a global 'context.json' file that contains a deep analysis of the Excel file.",
                "your output is a 'context.json' file that you save in the 'outputs' folder.",
                "You must deeply understand the structure and content of the Excel file.",
                "IMPORTANT: the summary should be rich(+200 word) and detailed, providing a comprehensive overview of the Excel file's content and structure, and it should contain informations about images or charts only if they exist.",
                "IF THERE ARE NO IMAGES OR CHARTS DO NOT mention them in the summary NEVER EVER",
                "WORKFLOW:",
                "1. consider yourself a profetional Excel file analyst and understand the content of the Excel file.",
                "2. read and inspect the images and charts folders dont print anything just understand the content of all the images and charts.",
                "3. read and inspect the csv files in the outputs folder dont print anything just understand the content of the csv files.",
                "4. read and inspect the 'anomalies.json' file in the outputs folder dont print anything just understand the content of the anomalies.json file.",
                "5. combine all the information you gathered from the Excel file, the csv files, the images and charts, and the anomalies.json file to generate a comprehensive analysis.",
                "6. create and run the python code that use the 'save_file_utf8' tool to save the final analysis in a 'context.json' file in the 'outputs' folder.",
                "You should always output a JSON structured like this:",
                r"""
                {
                    "Analysis": "the json that contains deep analysis of the Excel file",
                    "summary": "A human-readable paragraph resuming deeply the content of the Excel file",
                    "media": {
                        "images": ["image1.png", "image2.png"],
                        "charts": ["chart1.png", "chart2.png"]
                    },
                    "columns": ["column1", "column2", ...], // List of all columns in the Excel file with a description of each column respecting its content
                    "problems": "the issues found in the anomalies json file.",
                    "exemple_data": "5 first and last rows of the wxcel file in a json format"
                }
                """,
                "You should never output that JSON like that you should put it in the context.json file.",
            ]
        )

try:  
    agent_manager = AgentManager(model_name="gpt-4o", temperature=0.1, max_tokens=50000)
    agent = agent_manager.create_Context_Agent()
    response = agent.run()
    print(response.content)
except ModelProviderError as e:
    print("❌ OpenAI API quota exceeded.")