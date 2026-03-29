from agent_graph.workflow import build_graph

graph = build_graph()

def run_risk_analysis(company_name: str):
    return graph.invoke({"company": company_name})