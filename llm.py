from litellm import completion

response = completion(
            model="ollama/llama2", 
            messages = [{ "content": "I need to determine how large of a prompt I can make.  You are going to conduct a financial analysis to match a lender from an applicant.  For example an applicant with a 500 credit score will be matched with lenders from Ally, Wells Fargo and Santandar.  Ally accepts applicants with a credit score of 600, Wells Fargo accepts applicants with a credit score of 500 and Santandar accepts applicants with a credit score of 900.  Which is the best lender?","role": "user"}], 
            api_base="http://localhost:11434"
)

