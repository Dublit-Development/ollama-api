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
