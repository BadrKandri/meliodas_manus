import os,glob
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.exceptions import ModelProviderError
from tools import execute_code, file_operations

load_dotenv()
key = os.getenv("OPENAI_API_KEY") 
os.environ["OPENAI_API_KEY"] = key 

csv_files = glob.glob(os.path.join("outputs", "*.csv"))

class AgentManager:
    def __init__(self, model_name: str, temperature: float, max_tokens: int):
        self.model_name = model_name
        self.temp = temperature
        self.max_tokens = max_tokens

    def create_Plot_Agent(self):
        tools = [execute_code(), file_operations()]
        return Agent(
            name="Plot_Agent",
            model=OpenAIChat(self.model_name),
            tools=tools,
            #debug_mode=True,
            instructions=[
                "Your are a profetional plotly expert Agent",
                f"Your Job is to create and customize plots using the Plotly library based on csv files that you find inside the {csv_files}.",
                "the user will ask you to create a plot based on the data in a specific csv file, you use the Plotly library to generate the plot.",
                "you generate the plot as an image and you save it in the output folder."
            ]
        )

if __name__ == "__main__":
    try:  
        agent_manager = AgentManager(model_name="gpt-4o", temperature=0.1, max_tokens=50000)
        agent = agent_manager.create_Plot_Agent()
        response = agent.run(input("HELLO, i am Meliodas Manus Agent how can i help you?\n===> "))
        print(response.content)
    except ModelProviderError as e:
        print("❌ OpenAI API quota exceeded.")