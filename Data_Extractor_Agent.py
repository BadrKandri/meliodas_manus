import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.exceptions import ModelProviderError
from tools import excel_parser, execute_code, file_operations,save_file_utf8

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 
        
class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens

    def Data_Extractor_Agent(self):
        tools = [excel_parser(), execute_code(), file_operations(), save_file_utf8]
        return Agent(
            name="Data_Extractor_Agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            #debug_mode=True,
            instructions=[
                "You are an autonomous Excel analysis agent, you ALWAYS use Excel files in the 'excels' folder",
                "Your job is to extract all the important data from the Excel file that we will need later in this agentic system. and to analyze Excel files using strict function calls.",
                "WORKFLOW:",
                "1. Creat an empty json named 'media.json' and put it in the 'outputs' folder",
                "2. Call the `file_operations.read_file(file_path)` tool to read the Excel file and get the file_path",
                "2. Call the `excel_parser.excel_parser(file_path)` tool to get the sheet structure and data.",
                "3. Call the `excel_parser.extract_and_analyze_charts(file_path)` tool to extract and analyze all charts, save charts in the charts folder and append the charts analysis in the 'media.json' file you create.",
                "4. Call the `excel_parser.extract_and_analyze_images(file_path)` tool to extract and analyze all images, save images in the images folder and append the images analysis in the 'media.json' file you create.",
                "5. create and run the python code that read the excel file and transform it into a pandas dataframe you should do that for each sheet that contain all the tables and save it in a csv file named '<sheet name>_data.csv' and save it in the 'outputs' folder IMPORTNT: creat csv file for each sheet that contain tables.",
                "IMPORTANT: You should extract the whole table NEVER EXTRACT A PART OF THE TABLE.",
                "You should never output any detailed overview or something to the user you should do your work silently, an affirmation that contain the number of rows and columns is enough.",
            ]
        )

if __name__ == "__main__":
    try:  
        agent_manager = AgentManager(model_name="gpt-4o", temperature=0.1, max_tokens=50000)
        agent = agent_manager.Data_Extractor_Agent()
        response = agent.run()
        print(response.content)
    except ModelProviderError as e:
        print("❌ OpenAI API quota exceeded.")