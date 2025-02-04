from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from phi.playground import Playground
from agents import network_expert, ticketing_expert, customer_support_agent

# Initialize FastAPI
app = FastAPI(title="Customer Support AI Playground")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Playground with proper routing
playground = Playground(
    base_path="/v1/playground",
    agents=[network_expert, ticketing_expert, customer_support_agent],
    debug_endpoints=True,
    enable_session_management=True
)

# Explicitly register routes
playground.register_routes(app)

@app.get("/v1/playground/status", include_in_schema=False)
async def status_check():
    return {"status": "active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="localhost",
        port=7777,
        reload=True,
        # Required for clean shutdown
        timeout_keep_alive=5
    )