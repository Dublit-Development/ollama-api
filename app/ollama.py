import subprocess, shlex
import json


def listInstalledModels():
    curl_command = f'curl http://localhost:11434/api/tags'

    output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')
    res = json.loads(output)

    # Extract only the 'name' attribute and remove ':latest'
    model_names = [model.get('name', '').replace(':latest', '') for model in res.get('models', [])]

    return model_names

def listModels():
    model_names = listInstalledModels()
    return {'model_names': model_names}

# Now you can print the result or do whatever you want with it
result = listModels()
print(result)


def run_model_question(question, context):
    # Get the list of installed models (replace listInstalledModels with the correct function)
    model_names = listInstalledModels()

    # Initialize a dictionary to store responses for each model
    all_responses = {}

    for model in model_names:
        # Use shlex.quote for question and context to handle special characters
        quoted_question = shlex.quote(question)
        quoted_context = shlex.quote(context)
        
        # Define the data payload as a dictionary
        data_payload = {
            "model": model,
            "prompt": quoted_question,
            "context": quoted_context
        }

        # Convert the data payload to a JSON string
        json_data = json.dumps(data_payload)

        # Run the command and capture the output
        process = subprocess.Popen(['curl', 'http://localhost:11434/api/generate', '-d', json_data],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        # Check for errors
        if process.returncode != 0:
            print(f"Error running command for model {model}. Error message: {error.decode('utf-8')}")
            continue

        # Process the output as JSON and extract "response" values
        try:
            responses = [json.loads(response)["response"] for response in output.strip().split('\n')]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response for model {model}. Error message: {e}")
            continue

        # Add the responses to the dictionary for all models
        all_responses[model] = responses

    return all_responses

# Run the question for all installed models
results = run_model_question("What is the Dutch East India Company?", "The Dutch East India Company...")
print(results)