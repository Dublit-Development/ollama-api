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


def run_model_generate(question, content):
    # Get the list of installed models (replace listInstalledModels with the correct function)
    model_names = listInstalledModels()

    # Initialize a dictionary to store responses for each model
    all_responses = {}

    for model in model_names:
        # Use shlex.quote for question and context to handle special characters
        quoted_question = shlex.quote(question)
        quoted_content = shlex.quote(content)
        
        # Define the data payload as a dictionary
        data_payload = {
            "model": model,
            "prompt": quoted_question,
            "content": quoted_content
        }

        # Convert the data payload to a JSON string
        json_data = json.dumps(data_payload)

        # Run the command and capture the output
        process = subprocess.Popen(['curl', 'http://localhost:11434/api/chat', '-d', json_data],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        
        # Decode the output from bytes to UTF-8 string
        output_str = output.decode('utf-8')

        # Print the output for debugging
        print("Raw Output:", output_str)

        # Check for errors
        if process.returncode != 0:
            print(f"Error running command. Error message: {error.decode('utf-8')}")
            return  # or exit the function, depending on your requirements

        # Process the output as JSON and extract "response" values
        try:
            responses = [json.loads(response)["response"] for response in output_str.strip().split('\n')]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response. Error message: {e}")
            return  # or exit the function, depending on your requirements

        # Add the responses to the dictionary for all models
        all_responses[model] = responses

    return all_responses

def run_model_chat(question, content):
    # Replace listInstalledModels with the correct function to get the model names
    model_names = listInstalledModels()

    # Initialize a dictionary to store responses for each model
    all_responses = {}

    for model in model_names:
        # Use shlex.quote for question and content to handle special characters
        quoted_question = shlex.quote(question)
        quoted_content = shlex.quote(content)
        
        # Define the data payload as a dictionary
        data_payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": quoted_question},
                {"role": "assistant", "content": quoted_content}
            ],
            "stream": False
        }

        # Convert the data payload to a JSON string
        json_data = json.dumps(data_payload)

        # Run the command and capture the output
        process = subprocess.Popen(['curl', 'http://localhost:11434/api/chat', '-d', json_data],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        
        # Decode the output from bytes to UTF-8 string
        output_str = output.decode('utf-8')

        # Print the output for debugging
        # print("Raw Output:", output_str)

        # Check for errors
        if process.returncode != 0:
            print(f"Error running command. Error message: {error.decode('utf-8')}")
            return  # or exit the function, depending on your requirements

        # Process the output as JSON
        try:
            response_json = json.loads(output_str)
            assistant_response = response_json.get('message', {}).get('content', '')
            all_responses[model] = assistant_response
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response. Error message: {e}")
            return  # or exit the function, depending on your requirements

    return all_responses

# Run the question for all installed models
results = run_model_chat("""What is the Dutch East India Company? How much $ did the company make? What was the % owned? Did the company""" , """The United East India Company (Dutch: Verenigde Oostindische Compagnie [vərˈeːnɪɣdə oːstˈɪndisə kɔmpɑˈɲi], abbreviated as VOC, Dutch: [veː.oːˈseː]) and commonly known as the Dutch East India Company, was a chartered trading company and the first joint-stock company in the world.[2][3] Established on 20 March 1602[4] by the States General of the Netherlands existing companies, it was granted a 21-year monopoly to carry out trade activities in Asia.[5] Shares in the company could be bought by any resident of the United Provinces (Dutch Republic) and then subsequently bought and sold in open-air secondary markets (one of which became the Amsterdam Stock Exchange).[6] The company possessed quasi-governmental powers, including the ability to wage war, imprison and execute convicts,[7] negotiate treaties, strike its own coins, and establish colonies.[8] Also, because it traded across multiple colonies and countries from both the East and the West, the VOC is sometimes considered to have been the world's first multinational corporation.[9][10]

Statistically, the VOC eclipsed all of its rivals in the Asia trade. Between 1602 and 1796 the VOC sent almost a million Europeans to work in the Asia trade on 4,785 ships and netted for their efforts more than 2.5 million tons of Asian trade goods and slaves. By contrast, the rest of Europe combined sent only 882,412 people from 1500 to 1795, and the fleet of the English (later British) East India Company, the VOC's nearest competitor, was a distant second to its total traffic with 2,690 ships and a mere one-fifth the tonnage of goods carried by the VOC. The VOC enjoyed huge profits from its spice monopoly and slave trading activities through most of the 17th century.[11]

Having been set up in 1602 to profit from the Malukan spice trade, the VOC established a capital in the port city of Jayakarta in 1609 and changed its name to Batavia (now Jakarta). Over the next two centuries the company acquired additional ports as trading bases and safeguarded their interests by taking over surrounding territory.[12] It remained an important trading concern and paid an 18% annual dividend for almost 200 years. Much of the labour that built its colonies was from people it had enslaved.

Weighed down by smuggling, corruption and growing administrative costs in the late 18th century, the company went bankrupt and was formally dissolved in 1799. Its possessions and debt were taken over by the government of the Dutch Batavian Republic.

Company name, logo, and flag

17th-century plaque to the [Dutch] United East India Company (the VOC), Hoorn

The logo of the Amsterdam Chamber of the VOC
In Dutch, the name of the company was the Vereenigde Nederlandsche Geoctroyeerde Oostindische Compagnie (abbreviated as the VOC), literally the 'United Dutch Chartered East India Company' (the United East India Company).[13] The company's monogram logo consisted of a large capital 'V' with an O on the left and a C on the right half and was possibly the first globally recognised corporate logo.[14] It appeared on various corporate items, such as cannons and coins. The first letter of the hometown of the chamber conducting the operation was placed on top. The monogram, versatility, flexibility, clarity, simplicity, symmetry, timelessness, and symbolism are considered notable characteristics of the VOC's professionally designed logo. Those elements ensured its success at a time when the concept of the corporate identity was virtually unknown.[14][15] An Australian vintner has used the VOC logo since the late 20th century, having re-registered the company's name for the purpose.[16]

Around the world, and especially in English-speaking countries, the VOC is widely known as the 'Dutch East India Company'. The name 'Dutch East India Company' is used to make a distinction from the [British] East India Company (EIC) and other East Indian companies (such as the Danish East India Company, French East India Company, Portuguese East India Company, and the Swedish East India Company). The company's alternative names that have been used include the 'Dutch East Indies Company', 'United East India Company', 'Jan Company', or 'Jan Compagnie'.[17][18]

History
Origins
See also: First Dutch Expedition to Indonesia, Second Dutch Expedition to Indonesia, and Voorcompagnie
Further information: Spice trade and Cape Route
Before the Dutch Revolt, which started in 1566/68, the Flemish city of Antwerp had played an important role as a distribution center in northern Europe. After 1591, the Portuguese used an international syndicate of the German Fugger family and Welser family, as well as Spanish and Italian firms, which operated out of Hamburg as the northern staple port to distribute their goods, thereby cutting Dutch merchants out of the trade. At the same time, the Portuguese trade system was unable to increase supply to satisfy growing demand, in particular the demand for pepper. Demand for spices was relatively inelastic; therefore, each lag in the supply of pepper caused a sharp rise in pepper prices.

In 1580, the Portuguese crown was united in a personal union with the Spanish crown (called the Iberian Union), with which the Dutch Republic was at war. The Portuguese Empire thus became an appropriate target for Dutch military incursions. These factors motivated Dutch merchants to enter the intercontinental spice trade themselves. Further, a number of Dutch merchants and explorers, such as Jan Huyghen van Linschoten and Cornelis de Houtman, went on to obtain firsthand knowledge of the "secret" Portuguese trade routes and practices that were already in place, thereby providing further opportunity for the Dutch to enter the trade.[19]

The stage was thus set for Dutch expeditions to the Indonesian islands, beginning with James Lancaster in 1591, Cornelis de Houtman in 1595 and again in 1598, Jacob Van Neck in 1598, Lancaster again in 1601, among others. During the four-ship exploratory expedition by Frederick de Houtman in 1595 to Banten, the main pepper port of West Java, the crew clashed with both Portuguese and indigenous Javanese. Houtman's expedition then sailed east along the north coast of Java, losing twelve crew members to a Javanese attack at Sidayu and killing a local ruler in Madura. Half the crew were lost before the expedition made it back to the Netherlands the following year, but with enough spices to make a considerable profit.[20]""")

print(results)