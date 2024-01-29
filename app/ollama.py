import subprocess
import json

def listInstalledModels():
    curl_command = f'curl http://localhost:11434/api/tags'

    output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')
    res = json.loads(output)

    return [model.get('name', '') for model in res.get('models', [])]  # Extract only the 'name' attribute

def listModels():
    model_names = listInstalledModels()
    return {'model_names': model_names}

# Now you can print the result or do whatever you want with it
result = listModels()
print(result)



