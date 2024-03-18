from litellm import completion
import json

def llm_query(applicantPrompt, allyPrompt, santandarPrompt, wellFargo, capitalOne, questionPrompt):
    response = completion(
                model="ollama/gemma:7b", 
                messages = [{ "content": f"""  The applicant has provided the following information {applicantPrompt}. {questionPrompt}.
                {allyPrompt}, {santandarPrompt}, {wellFargo}, {capitalOne}.""","role": "user"}], 
                api_base="http://localhost:11434"
    )

    return response

class Prompt:
    lenders_info_filename = './data/lenders_info.json'

    def __init__(self, lender_name, name, creditScore, amountToFinance, chapter7, chapter13):
        self.lender = lender_name
        self.creditScore = creditScore
        self.amtFinance = amountToFinance
        self.ch7 = chapter7
        self.ch13 = chapter13
        self.name = name
        self.load_data()

    def load_data(self):
        with open(self.lenders_info_filename, 'r') as file:
            self.info_data = json.load(file)

    def applicant_prompt(self):
        applicantPrompt = "You are a financial loan assistant at an automotive company,  this prompt is the applicant data to choose the best lender."

        applicantPrompt += f"""{self.name} is looking to find the most suitable lender and has provided criteria for the process.  
                            The applicant has a credit score of {self.creditScore}.
                            The applicant has an amount to finance of {self.amtFinance}.
                            Has the applicant filed for chapter 7? {self.ch7}.
                            Has the applicant filed for chapter 13? {self.ch13}.
                            """
        return applicantPrompt

    def lender_prompt(self):
        lenderPrompt = '''Here are the prompts of each lender and criteria they look for.'''
        
        creditRange = self.info_data[self.lender]["CreditRange"]
        FirstTimeBuyers = self.info_data[self.lender]["FirstTimeBuyers"]
        Ghosts = self.info_data[self.lender]["Ghosts"]
        # Identification = self.info_data[self.lender]["Identification"]
        SecondJobTime = self.info_data[self.lender]["SecondJobTime"]
        SecondAutomotive = self.info_data[self.lender]["SecondAutomotive"]
        Chapter7 = self.info_data[self.lender]["Chapter7"]
        Chapter13 = self.info_data[self.lender]["Chapter13"]
        FinanceRange = self.info_data[self.lender]["FinanceRange"]
        TemporaryJobs = self.info_data[self.lender]["TemporaryJobs"]
        UberorLyft = self.info_data[self.lender]["UberorLyft"]
        Niche = self.info_data[self.lender]["Niche"]
        Niche1 = self.info_data[self.lender]["Niche1"]
        Niche2 = self.info_data[self.lender]["Niche2"]
        Niche3 = self.info_data[self.lender]["Niche3"]
        Niche4 = self.info_data[self.lender]["Niche4"]
        Niche5 = self.info_data[self.lender]["Niche5"]
        Niche6 = self.info_data[self.lender]["Niche6"]
        Watchout = self.info_data[self.lender]["Watchout"]
        Watchout1 = self.info_data[self.lender]["Watchout1"]
        Watchout2 = self.info_data[self.lender]["Watchout2"]

        lenderPrompt += f'''n\n\{self.lender} is willing to work within a credit range of {creditRange}.
                    Does {self.lender} accept Ghosts applicants without a credit score? {Ghosts}.
                    Does {self.lender} accept first time buyers? {FirstTimeBuyers}.
                    Does {self.lender} accept a history of chapter 7 bankrupcy? {Chapter7}.
                    Does {self.lender} accept a history of chapter 13 banktupcy? {Chapter13}
                    Does {self.lender} allow for a second automotive loan? {SecondAutomotive}.
                    Does {self.lender} allow for temporary jobs? {TemporaryJobs}.
                    Does {self.lender} accept Uber or Lyft as employment? {UberorLyft}.
                    {self.lender} extremly prefers applicants with the following six niches, {Niche}, {Niche1}, {Niche2}, {Niche3}, {Niche4}, {Niche5} and {Niche6}.
                    {self.lender} does not accept applicants with {Watchout}, {Watchout1} and {Watchout2}.
                    \n\n'''
        
        return lenderPrompt 
    
    def question_prompt(self):
        questionPrompt = """What is the most appropriate lender for the applicant based on the information provided?  Be sure to take into consideration all of the lender data and make a decision that could
        be supported by the data provided."""

        return questionPrompt
    

ally = Prompt('Ally',"Joseph",750, 25000,"False","False")
santandar = Prompt('Santandar', "Joseph", 500, 25000, "True", "No")
wellsFargo = Prompt('WellsFargo', "Joseph", 500, 25000, "True", "No")
CapitalOne = Prompt('CapitalOne', "Joseph", 500, 25000, "True", "No")

print(ally.applicant_prompt())

print(llm_query(applicantPrompt=ally.applicant_prompt(), allyPrompt=ally.lender_prompt(), santandarPrompt=santandar.lender_prompt(), wellFargo=wellsFargo.lender_prompt(), capitalOne=CapitalOne.lender_prompt(), questionPrompt=ally.question_prompt()))