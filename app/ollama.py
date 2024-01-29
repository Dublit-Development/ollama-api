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

Dutch = """The United East India Company (Dutch: Verenigde Oostindische Compagnie, abbreviated as VOC, Dutch:]) and commonly known as the Dutch East India Company, was a chartered trading company and the first joint-stock company in the world.[2][3] Established on 20 March 1602[4] by the States General of the Netherlands existing companies, it was granted a 21-year monopoly to carry out trade activities in Asia.[5] Shares in the company could be bought by any resident of the United Provinces (Dutch Republic) and then subsequently bought and sold in open-air secondary markets (one of which became the Amsterdam Stock Exchange).[6] The company possessed quasi-governmental powers, including the ability to wage war, imprison and execute convicts,[7] negotiate treaties, strike its own coins, and establish colonies.[8] Also, because it traded across multiple colonies and countries from both the East and the West, the VOC is sometimes considered to have been the world's first multinational corporation."""

def run_model_question(question, context):
    # Get the list of installed models
    model_names = listInstalledModels()

    # Initialize a dictionary to store responses for each model
    all_responses = {}

    for model in model_names:
        # Use shlex.quote for question and context to handle special characters
        quoted_question = shlex.quote(question)
        quoted_context = shlex.quote(context)

        # Define the curl command for each model
        curl_command = f'curl http://localhost:11434/api/generate -d \'{{"model": "{model}", "prompt": {quoted_question}, "context": {quoted_context}}}\''

        # Run the command and capture the output
        output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')

        # Process the output as JSON and extract "response" values
        responses = [json.loads(response)["response"] for response in output.strip().split('\n')]

        # Add the responses to the dictionary for all models
        all_responses[model] = responses

    return all_responses

# Run the question for all installed models
results = run_model_question("What is the Dutch East India Company?", Dutch)
print(results)