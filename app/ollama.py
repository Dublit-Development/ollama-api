import subprocess
import json

def listInstalledModels():
    curl_command = f'curl http://localhost:11434/api/tags'

    output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')
    res = json.loads(output)

    return res

def listModels():
    res = listInstalledModels()
    return {'models': res}  # Return the dictionary directly

# Now you can print the result or do whatever you want with it
result = listModels()
print(result)


