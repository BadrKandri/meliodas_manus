from Report_Agent import AgentManager as ReportManager
from Insight_Agent import AgentManager as InsightManager
from Plot_Agent import AgentManager as PlotManager
from agno.agent import Agent

# Create your sub-agent
report_agent = ReportManager("gpt-4o", 0.1, 50000).create_Report_agent()
insight_agent = InsightManager("gpt-4o", 0.1, 50000).create_Insight_agent()
plot_agent = PlotManager("gpt-4o", 0.1, 50000).create_Plot_Agent()

# Create the orchestrator
orchestrator = Agent(
    name="Orchestrator",
    instructions="""
    You are An Orchestrator Agent you have 3 agents at your disposal, Your Job is to decide which sub-agent to call:
    - If query is about generating reports → call Report_Agent.
    - If query is a question that needs analysis to be answered → call Insight_Agent.
    - If query is about plotting data → call Plot_Agent.
    - Otherwise, → call Insight_Agent.
    dont use any agent just Respond with only the agent name you chose
    """
)


query = "i have 20 dollars can u help me make a list of food i can buy with this money? use the food csv"

def sub_agent(query):
    decision=orchestrator.run(query)
    print("🧠 Orchestrator decision:", decision.content)
    if decision.content == "Report_Agent":
        response = report_agent.run(query)
        print("📊 Report Agent Done")
    elif decision.content == "Insight_Agent":
        response = insight_agent.run(query)
        print("🔍 Insight Agent response:", response.content)
    elif decision.content == "Plot_Agent":
        response = plot_agent.run(query)
        print("📈 Plot Agent Done:")
