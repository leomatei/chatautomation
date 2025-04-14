from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/chat-query"

def get_sql_from_mistral(question):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": (
                f"Convert this question to an SQL query for PostgreSQL: {question}. "
                "The table is called 'users' and has columns: user_id(integer), full_name(text), email(text), "
                "status(text: active/inactive), created_at(timestamp). "
                "Please return ONLY the raw SQL query as plain text. No markdown or explanation."
            ),
            "stream": False
        }
    )
    response.raise_for_status()
    return response.json()["response"].strip()

def query_n8n(question, sql):
    response = requests.post(
        N8N_WEBHOOK_URL,
        json={"question": question, "sql": sql}
    )
    response.raise_for_status()
    return response.json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    try:
        sql = get_sql_from_mistral(question)
        result = query_n8n(question, sql)
        return jsonify({
            "sql": sql,
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
