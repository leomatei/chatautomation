import requests

# Ask user for a question
question = input("Ask your question: ")

# Step 1: Ask Mistral (via Ollama) to convert to SQL
mistral_response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral",
        "prompt": f"Convert this question to an SQL query for PostgreSQL: {question}. The table is called 'users' and has columns: user_id(integer), full_name(text), email(text), status(text: active/inactive), created_at(timestamp). Please just give me the raw sql in plain text, no other text, you response should only be the plain text sql query since i want to parse the response to an automation tool and any other info besides the sql query will cause an error in my workflow.",
        "stream": False
    }
)

sql_query = mistral_response.json()["response"]
print(f"\nGenerated SQL:\n{sql_query}")

# Step 2: Send to n8n via webhook
n8n_response = requests.post(
    "http://localhost:5678/webhook-test/chat-query",  # Update this if your webhook path is different
    json={
        "question": question,
        "sql": sql_query
    }
)

print("\nFormatted Result from n8n:")
print(n8n_response.json())
