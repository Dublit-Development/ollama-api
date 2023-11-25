from flask import Flask, request, jsonify, render_template
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/api/question', methods=['POST'])
def process_question():
    # Get the question from the request
    data = request.get_json()
    question = data.get('question', '')

    # Run a command and capture the output
    result = run_curl_command(question)

    print(result)

    # Return the result as JSON
    return jsonify({'result': result})

def run_curl_command(question):
    # Define the curl command
    curl_command = f'curl http://localhost:11434/api/generate -d \'{{"model": "llama2", "prompt": "{question}"}}\''

    # Run the command and capture the output
    output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')

    # Process the output as JSON
    responses = [json.loads(response) for response in output.strip()]

    return responses

app.run(host='0.0.0.0', port=5000, debug=True)


