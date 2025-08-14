from Data_Extractor_Agent import AgentManager as DataExtractorManager
from Anomaly_Agent import AgentManager as AnomalyManager
from Context_Agent import AgentManager as ContextManager
from Planner_Agent import AgentManager as PlannerManager
from Reviewer_Agent import AgentManager as ReviewerManager
from Orchestrator import orchestrator
from agno.exceptions import ModelProviderError
from pathlib import Path

query=input("HELLO, i am Meliodas Manus Agent how can i help you?\n===> ")

excel_path = Path("excels/*.xlsx")
data_extractor_agent = DataExtractorManager("gpt-4o", 0.1, 50000).Data_Extractor_Agent()
anomaly_agent = AnomalyManager("gpt-4o", 0.1, 50000).create_Anomaly_Agent()
context_agent = ContextManager("gpt-4o", 0.1, 50000).create_Context_Agent()
planner_agent = PlannerManager("gpt-4o", 0.1, 50000).Planner_Agent(query, excel_path)


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

is_done = False
iteration = 0
while iteration < 5:
    if is_done == True:
        print("All tasks are done successfully!")
        break
    else:
        iteration += 1
        print(f"Iteration {iteration} of 5")
        print("the orchestrator is working now")
        decision, agents_output, task = orchestrator(query)
        print("lets check if the task is done or not")
        reviewer_agent = ReviewerManager("gpt-4o", 0.1, 50000).Review_Agent(agents_output, decision, task)
        reviewer_response = reviewer_agent.run()
        is_done = bool(reviewer_response.content.is_done)
        print(f"Task completion status: {is_done}")