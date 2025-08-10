from Data_Extractor_Agent import AgentManager as DataExtractorManager
from Anomaly_Agent import AgentManager as AnomalyManager
from Context_Agent import AgentManager as ContextManager
from Orchestrator import sub_agent
from agno.exceptions import ModelProviderError

data_extractor_agent = DataExtractorManager("gpt-4o", 0.1, 50000).Data_Extractor_Agent()
anomaly_agent = AnomalyManager("gpt-4o", 0.1, 50000).create_Anomaly_Agent()
context_agent = ContextManager("gpt-4o", 0.1, 50000).create_Context_Agent()

query=input("HELLO, i am Meliodas Manus Agent how can i help you?\n===> ")

try:
    response = data_extractor_agent.run()
    print("✅ All Data extracted successfully")

    response = anomaly_agent.run()
    print("✅ All Anomalies detected successfully")

    response = context_agent.run()
    print("✅ Context Generated successfully")
    
except ModelProviderError as e:
        print("❌ OpenAI API quota exceeded while analyzing the file")

try:
    sub_agent(query)
except ModelProviderError as e:
        print("❌ OpenAI API quota exceeded while analyzing the file")
