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
results = run_model_chat("""What is the Dutch East India Company's? How much $ did the company make? What was the % owned? Did the company ""? ""?  """, """The United East India Company (Dutch: Verenigde Oostindische Compagnie [vərˈeːnɪɣdə oːstˈɪndisə kɔmpɑˈɲi], abbreviated as VOC, Dutch: [veː.oːˈseː]) and commonly known as the Dutch East India Company, was a chartered trading company and the first joint-stock company in the world.[2][3] Established on 20 March 1602[4] by the States General of the Netherlands existing companies, it was granted a 21-year monopoly to carry out trade activities in Asia.[5] Shares in the company could be bought by any resident of the United Provinces (Dutch Republic) and then subsequently bought and sold in open-air secondary markets (one of which became the Amsterdam Stock Exchange).[6] The company possessed quasi-governmental powers, including the ability to wage war, imprison and execute convicts,[7] negotiate treaties, strike its own coins, and establish colonies.[8] Also, because it traded across multiple colonies and countries from both the East and the West, the VOC is sometimes considered to have been the world's first multinational corporation.[9][10]

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

The stage was thus set for Dutch expeditions to the Indonesian islands, beginning with James Lancaster in 1591, Cornelis de Houtman in 1595 and again in 1598, Jacob Van Neck in 1598, Lancaster again in 1601, among others. During the four-ship exploratory expedition by Frederick de Houtman in 1595 to Banten, the main pepper port of West Java, the crew clashed with both Portuguese and indigenous Javanese. Houtman's expedition then sailed east along the north coast of Java, losing twelve crew members to a Javanese attack at Sidayu and killing a local ruler in Madura. Half the crew were lost before the expedition made it back to the Netherlands the following year, but with enough spices to make a considerable profit.[20]


Return of the second Asia expedition of Jacob van Neck in 1599 by Cornelis Vroom
In 1598, an increasing number of fleets were sent out by competing merchant groups from around the Netherlands. Some fleets were lost, but most were successful, with some voyages producing high profits. In 1598, a fleet of eight ships under Jacob van Neck had been the first Dutch fleet to reach the 'Spice Islands' of Maluku (also known as the Moluccas), cutting out the Javanese middlemen. The ships returned to Europe in 1599 and 1600 and the expedition made a 400 percent profit.[20]

In 1600, the Dutch joined forces with the Muslim Hituese on Ambon Island in an anti-Portuguese alliance, in return for which the Dutch were given the sole right to purchase spices from Hitu.[21] Dutch control of Ambon was achieved when the Portuguese surrendered their fort in Ambon to the Dutch-Hituese alliance. In 1613, the Dutch expelled the Portuguese from their Solor fort, but a subsequent Portuguese attack led to a second change of hands; following this second reoccupation, the Dutch once again captured Solor in 1636.[21]

East of Solor, on the island of Timor, Dutch advances were halted by an autonomous and powerful group of Portuguese Eurasians called the Topasses. They remained in control of the Sandalwood trade and their resistance lasted throughout the 17th and 18th centuries, causing Portuguese Timor to remain under the Portuguese sphere of control.[22][23]

Formative years

Mughal Bengal's baghlah was a type of ship widely used by Dutch traders in the Indian Ocean, the Arabian Sea, the Bay of Bengal, the Strait of Malacca and the South China Sea

Reproduction of a map of the city of Batavia c. 1627, collection Tropenmuseum

Dutch Batavia in 1681, built in what is now North Jakarta
At the time, it was customary for a company to be funded only for the duration of a single voyage and to be liquidated upon the return of the fleet. Investment in these expeditions was a very high-risk venture, not only because of the usual dangers of piracy, disease and shipwreck, but also because the interplay of inelastic demand and relatively elastic supply[24] of spices could make prices tumble, thereby ruining prospects of profitability. To manage such risk, the forming of a cartel to control supply would seem logical. In 1600, the English were the first to adopt this approach by bundling their resources into a monopoly enterprise, the English East India Company, thereby threatening their Dutch competitors with ruin.[25]

In 1602, the Dutch government followed suit, sponsoring the creation of a single "United East Indies Company" that was also granted monopoly over the Asian trade.[26] For a time in the seventeenth century, it was able to monopolise the trade in nutmeg, mace, and cloves and to sell these spices across European kingdoms and Emperor Akbar the Great's Mughal Empire at 14–17 times the price it paid in Indonesia;[27] while Dutch profits soared, the local economy of the Spice Islands was destroyed.[why?] With a capital of 6,440,200 guilders,[28] the new company's charter empowered it to build forts, maintain armies, and conclude treaties with Asian rulers. It provided for a venture that would continue for 21 years, with a financial accounting only at the end of each decade.[25]

In February 1603, the company seized the Santa Catarina, a 1500-ton Portuguese merchant carrack, off the coast of Singapore.[29] She was such a rich prize that her sale proceeds increased the capital of the VOC by more than 50%.[30]

Also in 1603, the first permanent Dutch trading post in Indonesia was established in Banten, West Java, and in 1611, another was established at Jayakarta (later "Batavia" and then "Jakarta").[31] In 1610, the VOC established the post of governor-general to more firmly control their affairs in Asia. To advise and control the risk of despotic governors-general, a Council of the Indies (Raad van Indië) was created. The governor-general effectively became the main administrator of the VOC's activities in Asia, although the Heeren XVII, a body of 17 shareholders representing different chambers, continued to officially have overall control.[21]


The Isle of Amboina, a 17th century print, probably English
VOC headquarters were located in Ambon during the tenures of the first three governors-general (1610–1619), but it was not a satisfactory location. Although it was at the centre of the spice production areas, it was far from the Asian trade routes and other VOC areas of activity ranging from Africa to India to Japan.[32][33] A location in the west of the archipelago was thus sought. The Straits of Malacca were strategic but became dangerous following the Portuguese conquest, and the first permanent VOC settlement in Banten was controlled by a powerful local ruler and subject to stiff competition from Chinese and English traders.[21]

In 1604, a second English East India Company voyage commanded by Sir Henry Middleton reached the islands of Ternate, Tidore, Ambon and Banda. In Banda, they encountered severe VOC hostility, sparking Anglo-Dutch competition for access to spices.[31] From 1611 to 1617, the English established trading posts at Sukadana (southwest Kalimantan), Makassar, Jayakarta and Jepara in Java, and Aceh, Pariaman and Jambi in Sumatra, which threatened Dutch ambitions for a monopoly on East Indies trade.[31]

In 1620, diplomatic agreements in Europe ushered in a period of collaboration between the Dutch and English spice trades.[31]. This ended with the notorious Amboyna massacre, where ten Englishmen were arrested, tried and beheaded for conspiracy against the Dutch government.[34] Although this caused outrage in Europe and a diplomatic crisis, the English quietly withdrew from most of their Indonesian activities (except trading in Banten) and focused on other Asian interests.

Growth

Graves of Dutch dignitaries in the ruined St. Paul's Church, Malacca, in the former Dutch Malacca

Dutch East India Company factory in Hugli-Chuchura, Mughal Bengal. Hendrik van Schuylenburgh, 1665
In 1619, Jan Pieterszoon Coen was appointed governor-general of the VOC. He saw the possibility of the VOC becoming an Asian power, both political and economic. On 30 May 1619, Coen, backed by a force of nineteen ships, stormed Jayakarta, driving out the Banten forces; and from the ashes established Batavia as the VOC headquarters. In the 1620s almost the entire native population of the Banda Islands was driven away, starved to death, or killed in an attempt to replace them with Dutch plantations.[35] These plantations were used to grow nutmeg for export. Coen hoped to settle large numbers of Dutch colonists in the East Indies, but implementation of this policy never materialised, mainly because very few Dutch were willing to emigrate to Asia.[36]

Another of Coen's ventures was more successful. A major problem in the European trade with Asia at the time was that the Europeans could offer few goods that Asian consumers wanted, except silver and gold. European traders therefore had to pay for spices with the precious metals, which were in short supply in Europe, except for Spain and Portugal. The Dutch and English had to obtain it by creating a trade surplus with other European countries. Coen discovered the obvious solution for the problem: to start an intra-Asiatic trade system, whose profits could be used to finance the spice trade with Europe. In the long run this obviated the need for exports of precious metals from Europe, though at first it required the formation of a large trading-capital fund in the Indies. The VOC reinvested a large share of its profits to this end in the period up to 1630.[37]

The VOC traded throughout Asia, benefiting mainly from Bengal. Ships coming into Batavia from the Netherlands carried supplies for VOC settlements in Asia. Silver and copper from Japan were used to trade with the world's wealthiest empires, Mughal India and Qing China, for silk, cotton, porcelain, and textiles. These products were either traded within Asia for the coveted spices or brought back to Europe. The VOC was also instrumental in introducing European ideas and technology to Asia. The company supported Christian missionaries and traded modern technology with China and Japan. A more peaceful VOC trade post on Dejima, an artificial island off the coast of Nagasaki, was for more than two hundred years the only place where Europeans were permitted to trade with Japan.[38] When the VOC tried to use military force to make Ming dynasty China open up to Dutch trade, the Chinese defeated the Dutch in a war over the Penghu islands from 1623 to 1624, forcing the VOC to abandon Penghu for Taiwan. The Chinese defeated the VOC again at the Battle of Liaoluo Bay in 1633.

The Vietnamese Nguyen lords defeated the VOC in a 1643 battle during the Trịnh–Nguyễn War, blowing up a Dutch ship. The Cambodians defeated the VOC in the Cambodian–Dutch War from 1643 to 1644 on the Mekong River.


Dutch settlement in Bengal Subah
In 1640, the VOC obtained the port of Galle, Ceylon, from the Portuguese and broke the latter's monopoly of the cinnamon trade. In 1658, Gerard Pietersz Hulft laid siege to Colombo, which was captured with the help of King Rajasinghe II of Kandy. By 1659, the Portuguese had been expelled from the coastal regions, which were then occupied by the VOC, securing for it the monopoly over cinnamon. To prevent the Portuguese or the English from ever recapturing Sri Lanka, the VOC went on to conquer the entire Malabar Coast from the Portuguese, almost entirely driving them from the west coast of India.

In 1652, Jan van Riebeeck established a resupply outpost at the Cape of Storms (the southwestern tip of Africa, now Cape Town, South Africa) to service company ships on their journey to and from East Asia. The cape was later renamed Cape of Good Hope in honour of the outpost's presence. Although non-company ships were welcome to use the station, they were charged exorbitantly. This post later became a full-fledged colony, the Cape Colony, when more Dutch and other Europeans started to settle there.

Through the seventeenth century VOC trading posts were also established in Persia, Bengal, Malacca, Siam, Formosa (now Taiwan), as well as the Malabar and Coromandel coasts in India. Direct access to mainland China came in 1729 when a factory was established in Canton.[39] In 1662, however, Koxinga expelled the Dutch from Taiwan[40] (see History of Taiwan).

In 1663, the VOC signed the "Painan Treaty" with several local lords in the Painan area that were revolting against the Aceh Sultanate. The treaty allowed the VOC to build a trading post in the area and eventually to monopolise the trade there, especially the gold trade.[41]

By 1669, the VOC was the richest private company the world had ever seen, with over 150 merchant ships, 40 warships, 50,000 employees, a private army of 10,000 soldiers, and a dividend payment of 40% on the original investment.[42]

Many of the VOC employees inter-mixed with the indigenous peoples and expanded the population of Indos in pre-colonial history.[43][44]""")

print(results)