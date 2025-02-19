from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# OpenAI API Configuration
OPENAI_API_KEY = "F9d5qu6tGMECpFbxeVWCWgPG"  # Replace with your actual API key
openai.api_key = OPENAI_API_KEY

# Store conversation history for each user
conversation_history = {}

@app.route('/start_interview', methods=['POST'])
def start_interview():
    data = request.json
    user_id = data.get("user_id")
    job_role = data.get("job_role")

    prompt = f"Generate the first question for a mock interview for a {job_role} position."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=100
    )

    question = response['choices'][0]['message']['content']

    conversation_history[user_id] = [{"role": "assistant", "content": question}]

    return jsonify({"question": question})


@app.route('/answer_question', methods=['POST'])
def answer_question():
    data = request.json
    user_id = data.get("user_id")
    user_answer = data.get("answer")

    # Add user response to conversation history
    conversation_history[user_id].append({"role": "user", "content": user_answer})

    # Generate feedback and next question
    prompt = f"""
    Evaluate this interview answer: "{user_answer}".
    Provide constructive feedback and then ask the next interview question.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation_history[user_id] + [{"role": "system", "content": prompt}],
        max_tokens=300
    )

    ai_response = response['choices'][0]['message']['content']

    conversation_history[user_id].append({"role": "assistant", "content": ai_response})

    return jsonify({"response": ai_response})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
