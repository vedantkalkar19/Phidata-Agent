from phi.tools import tool
from datetime import datetime
from database import network_status_collection, tickets_collection

@tool
def check_network_status(location: str) -> str:
    """Fetches network status based on customer location."""
    network_data = network_status_collection.find_one({"location": location})

    if not network_data:
        return f"No network status found for {location}."

    issues = []
    for device_type, devices in network_data.get("devices", {}).items():
        for device, details in devices.items():
            if details.get("status") == "not_working":
                issues.append(
                    f"{device_type.capitalize()} {device} is down. Last checked: {details.get('last_checked')}"
                )

    return "All devices operational" if not issues else "Network Issues:\n" + "\n".join(issues)

@tool
def check_or_create_ticket(issue_details: dict) -> str:
    """Search past tickets or create new ticket if none exist."""
    existing_ticket = tickets_collection.find_one({
        "customer_id": issue_details.get("customer_id"),
        "issue_type": issue_details.get("issue_type"),
        "location": issue_details.get("location")
    })

    if existing_ticket:
        return f"Existing Ticket ID {existing_ticket['_id']} - Status: {existing_ticket['status']}"

    new_ticket = {
        "customer_id": issue_details.get("customer_id"),
        "issue_type": issue_details.get("issue_type"),
        "status": "Open",
        "created_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "location": issue_details.get("location"),
    }

    result = tickets_collection.insert_one(new_ticket)
    return f"New Ticket ID {result.inserted_id} - Status: Open"