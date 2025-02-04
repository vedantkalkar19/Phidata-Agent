from phi.agent import Agent
from phi.model.huggingface import HuggingFaceChat
from phi.storage.agent.sqlite import SqlAgentStorage
from tools import check_network_status, check_or_create_ticket

def create_agent(name: str, tools: list, instructions: list, table_name: str):
    return Agent(
        name=name,
        model=HuggingFaceChat(
            model_name="meta-llama/Meta-Llama-3-8B-Instruct",
            token="HF_TOKEN",  # Replace with actual token
            max_tokens=4096,
        ),
        tools=tools,
        instructions=instructions,
        storage=SqlAgentStorage(table_name=table_name, db_file="agents.db"),
        add_history_to_messages=True,
        markdown=True,
    )

# Network Expert Agent
network_expert = create_agent(
    name="Network Expert",
    tools=[check_network_status],
    instructions=["Analyze network status and identify outages"],
    table_name="network_expert"
)

# Ticketing Agent
ticketing_expert = create_agent(
    name="Ticketing Expert",
    tools=[check_or_create_ticket],
    instructions=["Manage support tickets and provide ticket status"],
    table_name="ticketing_expert"
)

# Customer Support Agent
customer_support_agent = create_agent(
    name="Customer Support Agent",
    tools=[check_network_status, check_or_create_ticket],
    instructions=["Resolve customer issues or create tickets"],
    table_name="customer_support_agent"
)