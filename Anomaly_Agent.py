import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.exceptions import ModelProviderError
from tools import execute_code, file_operations
from tools import execute_code, file_operations,save_file_utf8

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 
        
class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens

    def create_Anomaly_Agent(self):
        tools = [execute_code(), file_operations(), save_file_utf8]
        return Agent(
            name="Anomaly_Agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            #debug_mode=True,
            instructions=[
                "Consider yourself now as an expert-level senior data analyst. Your goal is to produce a comprehensive data quality report by performing both a systematic check and an exploratory analysis.",
                "ALWAYS use the excel files present in the 'excels' folder",
                "your output is a 'anomalies.json' file that you save in the 'outputs' folder.",
                "*Part 1: Systematic Quality Check*",
                    "Write and execute a Python script to perform a thorough analysis of the Excel file. Your script MUST check for the following common issues:",
                    "1.  *Missing Data*: Count nulls in all columns.",
                    "2.  *Outliers: Use the IQR method for numeric columns. **Crucially, your script should only store a small, representative sample (e.g., the first 20 found) of the outlier values for the report.* Do not store all of them.",
                    "3.  *Low Variability*: Identify columns with only one unique value.",
                    "4.  *Duplicate Rows*: Check for complete duplicate entries.",
                    "5.  *Data Type Consistency*: Verify appropriate data types.",
                    "6.  *High Cardinality*: Flag columns with a very high number of unique values (like IDs).",
                "*Part 2: Exploratory & Logical Analysis*",
                    "1. After the systematic check, your goal is to find issues that require logical reasoning or business context, you should think like a detective. Are there patterns that don't make sense? For example:",
                        "- Do quantities or costs have illogical negative values?",
                        "- Are there strange patterns in dates (e.g., all transactions on one day)?",
                        "- Are there relationships that seem odd (e.g., a 'Unit Price' of 0 for a non-free item)?",
                    "2. This part is about your intelligence as an analyst, not just a checklist. Document and combine all findings from both Part 1 and Part 2 into a single, comprehensive JSON report. and use the 'save_file_utf8' tool to save it in a file named 'anomalies.json' in the 'outputs' folder."
                "IMPORTANT: You should never output any detailed overview or something to the user you should do your work silently",
            ]
        )

try:  
    agent_manager = AgentManager(model_name="gpt-4o", temperature=0.1, max_tokens=50000)
    agent = agent_manager.create_Anomaly_Agent()
    response = agent.run()
    print(response.content)
except ModelProviderError as e:
    print("❌ OpenAI API quota exceeded.")