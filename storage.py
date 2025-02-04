from phi.storage.agent.sqlite import SqlAgentStorage

def initialize_storage():
    SqlAgentStorage.create_tables()

if __name__ == "__main__":
    initialize_storage()