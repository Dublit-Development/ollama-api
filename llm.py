from litellm import completion

response = completion(
            model="ollama/llama2", 
            messages = [{ "content": "Hello,  How are you?","role": "user"}], 
            api_base="http://localhost:11434"
)

print(response)