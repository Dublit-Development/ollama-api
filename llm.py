from litellm import completion

response = completion(
            model="ollama/llama2", 
            messages = [{ "content": """Hello,  How are you?.  You are going to be a financial analyst bot for a Automotive Company.  You need to make a selection of the most
                         appropriate lender given a applicant and his/her credit score and other details.  In the first example we will have a applicant with a credit score of 600 and three
                         lenders to choose from.  Wells Fargo accepts a credit score of 500,  Ally accepts a credit score of 600 and Santandar accepts a credit score of 800. 
                         What is the most appropriate lender? Let us add some additional parameters.  The applicant also has a co-signer.  The co-signer has a score of 800 given that
                         that the applicant has a co-signer that will take priortiy credit score.  What is the most appropriate lender now?""","role": "user"}], 
            api_base="http://localhost:11434"
)

print(response)