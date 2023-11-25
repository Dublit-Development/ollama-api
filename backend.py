from flask import Flask, request, jsonify, render_template

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

    # Run a command (echo the question in this case)
    result = run_command(question)

    # Return the result as JSON
    return jsonify({'result': result})

def run_command(question):
    # For simplicity, just echo the question
    return f"You asked: {question}"

if __name__ == '__main__':
    app.run(debug=True)
