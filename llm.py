from litellm import completion

response = completion(
            model="ollama/llama2", 
            messages = [{ "content": """Hello,  How are you?.  You are going to be a financial analyst bot for a Automotive Company.  You need to make a selection of the most
                         appropriate lender given a applicant and his/her credit score and other details.  In the first example we will have a applicant with a credit score of 600 and three
                         lenders to choose from.  Wells Fargo accepts a credit score of 500,  Ally accepts a credit score of 600 and Santandar accepts a credit score of 800. 
                         What is the most appropriate lender? Let us add some additional parameters.  The applicant also has a co-signer.  The co-signer has a score of 800 given that
                         that the applicant has a co-signer that will take priortiy credit score.  What is the most appropriate lender now? More data is coming in from our applicant and lenders.
                         Lenders now look out for self-employement.  Wells Fargo is lenient and willing to work with self-employement, Ally is not and Santandar is willing to as long as it is 
                         within their desired credit score.  Both of the co-signers are self-employed.  Who is the most appropriate lender with all of this data?
                         
                         Additional data is incoming. The maximum amount and minimum amount to finance for each lender varies.  Wells Fargo accepts a minimum of $10,000 and a maximum of
                         $100,000.  Ally accepts a minimum of $5,000 and a maximum of $50,000. Santandar accepts a minimum of $2,000 and a maximum of $30,000.  It is important that the vehicle
                         price is within range.  The user would like an SUV which starts at $40,000 a car at $10,000 and a Truck at $90,000.  What do you think is an applicable lender now?
                         The car selection of the applicant is influential.  Given that the applicant prefers an SUV what would be the most appropriate lender?
                         
                         We also have another peice of data.  The applicant and the co-signer do not have Identificaiton.  Ally is not willing to work with applicants with no ID, Sandtandar likewise
                         however Wells Fargo will allow for a applicants with no ID.  What would be the most appropriate choice?""","role": "user"}], 
            api_base="http://localhost:11434"
)

print(response)