from Data_Extractor_Agent import AgentManager as DataExtractorManager
from Anomaly_Agent import AgentManager as AnomalyManager
from Context_Agent import AgentManager as ContextManager
from Planner_Agent import AgentManager as PlannerManager
from Reviewer_Agent import AgentManager as ReviewerManager
from Orchestrator import orchestrator
from agno.exceptions import ModelProviderError

query=input("HELLO, i am Meliodas Manus Agent how can i help you?\n===> ")

data_extractor_agent = DataExtractorManager("gpt-4o", 0.1, 50000).Data_Extractor_Agent()
anomaly_agent = AnomalyManager("gpt-4o", 0.1, 50000).create_Anomaly_Agent()
context_agent = ContextManager("gpt-4o", 0.1, 50000).create_Context_Agent()
planner_agent = PlannerManager("gpt-4o", 0.1, 50000).Planner_Agent(query)


try:
    response = data_extractor_agent.run()
    print("✅ All Data extracted successfully")
    response = anomaly_agent.run()
    print("✅ All Anomalies detected successfully")
    response = context_agent.run()
    print("✅ Context Generated successfully")
except ModelProviderError as e:
    print("❌ OpenAI API quota exceeded while analyzing the file")

planner_response = planner_agent.run(query)
print("planner answer:", planner_response.content)

while True:
    decision, is_done, agents_output, task = orchestrator(query)
    if is_done == True:
        print("All tasks are done successfully!")
        break
    reviewer_agent = ReviewerManager("gpt-4o", 0.1, 50000).Review_Agent(agents_output, decision, task)
    review= reviewer_agent.run()
