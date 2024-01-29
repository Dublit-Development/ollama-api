import subprocess
import json

import subprocess
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

def run_model_question(question):
    # Get the list of installed models
    model_names = listInstalledModels()

    # Initialize an empty list to store responses for each model
    all_responses = []

    for model in model_names:
        # Define the curl command for each model
        curl_command = f'curl http://localhost:11434/api/generate -d \'{{"model": "{model}", "prompt": "{question}"}}\''

        # Run the command and capture the output
        output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')

        # Process the output as JSON and extract "response" values
        responses = [json.loads(response)["response"] for response in output.strip().split('\n')]

        # Add the responses to the list for all models
        all_responses.append({model: responses})

    return all_responses

# Run the question for all installed models
results = run_model_question("Why is the sky blue?")
print(results)