import json
from typing import Dict, List, Optional

def account_lookup(account_id: str) -> str:
    """
    Simulates looking up account details by ID.
    """
    # Mock data
    accounts = {
        "ACC-123": {"id": "ACC-123", "owner": "Alice Smith", "balance": 15000.00, "type": "Checking"},
        "ACC-456": {"id": "ACC-456", "owner": "Bob Jones", "balance": 2500.50, "type": "Savings"},
        "ACC-789": {"id": "ACC-789", "owner": "Charlie Brown", "balance": 1000000.00, "type": "Investment"},
    }
    
    result = accounts.get(account_id)
    if result:
        return json.dumps(result, indent=2)
    return f"Account {account_id} not found."

def kb_search(query: str) -> str:
    """
    Simulates searching a knowledge base.
    """
    # Mock KB articles
    kb_articles = [
        {"id": "KB-001", "title": "Wire Transfer Limits", "content": "Standard wire transfer limit is $50,000 per day. High-value clients can request up to $250,000."},
        {"id": "KB-002", "title": "Account Opening Requirements", "content": "Valid ID, proof of address, and initial deposit of $100 required."},
        {"id": "KB-003", "title": "Investment Products", "content": "We offer ETFs, Mutual Funds, and High-Yield Savings accounts."},
    ]
    
    # Simple keyword match
    results = []
    query_terms = query.lower().split()
    for article in kb_articles:
        # Check if the full query is in the text OR if significant words match
        text = (article["title"] + " " + article["content"]).lower()
        
        # Match if the exact query is found
        if query.lower() in text:
            results.append(article)
            continue
            
        # Fallback: Match if all query terms (longer than 3 chars) are present
        # This handles "wire transfers" matching "wire transfer" if we strip 's' or just match "wire" and "transfer"
        # For simplicity in this mock, let's just check if *any* significant term matches if the full phrase fails
        # But to be safer, let's check if the query *stem* is roughly there. 
        # Actually, let's just check if "wire" AND "transfer" are in the text.
        
        if all(term.rstrip('s') in text for term in query_terms if len(term) > 3):
             results.append(article)

            
    if results:
        return json.dumps(results, indent=2)
    return "No relevant articles found."

def crm_notes(client_name: str) -> str:
    """
    Simulates retrieving CRM notes for a client.
    """
    # Mock CRM data
    notes = {
        "Alice Smith": ["Interested in home loans.", "Called about wire transfer fees on 10/20."],
        "Bob Jones": ["Saving for a new car.", "Prefer email communication."],
        "Charlie Brown": ["High net worth individual.", "Looking for tax-efficient investment strategies."],
    }
    
    # Partial match for name
    found_notes = {}
    for name, note_list in notes.items():
        if client_name.lower() in name.lower():
            found_notes[name] = note_list
            
    if found_notes:
        return json.dumps(found_notes, indent=2)
    return f"No CRM notes found for client '{client_name}'."

AVAILABLE_TOOLS = {
    "account_lookup": account_lookup,
    "kb_search": kb_search,
    "crm_notes": crm_notes,
}
