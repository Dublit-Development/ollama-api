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

context = """The United East India Company (Dutch: Verenigde Oostindische Compagnie, abbreviated as VOC, Dutch:]) and commonly known as the Dutch East India Company, was a chartered trading company and the first joint-stock company in the world.[2][3] Established on 20 March 1602[4] by the States General of the Netherlands existing companies, it was granted a 21-year monopoly to carry out trade activities in Asia.[5] Shares in the company could be bought by any resident of the United Provinces (Dutch Republic) and then subsequently bought and sold in open-air secondary markets (one of which became the Amsterdam Stock Exchange).[6] The company possessed quasi-governmental powers, including the ability to wage war, imprison and execute convicts,[7] negotiate treaties, strike its own coins, and establish colonies.[8] Also, because it traded across multiple colonies and countries from both the East and the West, the VOC is sometimes considered to have been the world's first multinational corporation.[9][10]

Statistically, the VOC eclipsed all of its rivals in the Asia trade. Between 1602 and 1796 the VOC sent almost a million Europeans to work in the Asia trade on 4,785 ships and netted for their efforts more than 2.5 million tons of Asian trade goods and slaves. By contrast, the rest of Europe combined sent only 882,412 people from 1500 to 1795, and the fleet of the English (later British) East India Company, the VOC's nearest competitor, was a distant second to its total traffic with 2,690 ships and a mere one-fifth the tonnage of goods carried by the VOC. The VOC enjoyed huge profits from its spice monopoly and slave trading activities through most of the 17th century.[11]

Having been set up in 1602 to profit from the Malukan spice trade, the VOC established a capital in the port city of Jayakarta in 1609 and changed its name to Batavia (now Jakarta). Over the next two centuries the company acquired additional ports as trading bases and safeguarded their interests by taking over surrounding territory.[12] It remained an important trading concern and paid an 18% annual dividend for almost 200 years. Much of the labour that built its colonies was from people it had enslaved.

Weighed down by smuggling, corruption and growing administrative costs in the late 18th century, the company went bankrupt and was formally dissolved in 1799. Its possessions and debt were taken over by the government of the Dutch Batavian Republic."""

def run_model_question(question, context):
    # Get the list of installed models
    model_names = listInstalledModels()

    # Initialize a dictionary to store responses for each model
    all_responses = {}

    for model in model_names:
        # Define the curl command for each model
        curl_command = f'curl http://localhost:11434/api/generate -d \'{{"model": "{model}", "prompt": "{question}", "context": {context}"}}\''

        # Run the command and capture the output
        output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')

        # Process the output as JSON and extract "response" values
        responses = [json.loads(response)["response"] for response in output.strip().split('\n')]

        # Add the responses to the dictionary for all models
        all_responses[model] = responses

    return all_responses

# Run the question for all installed models
results = run_model_question("What is the Dutch East India Company?")
print(results)