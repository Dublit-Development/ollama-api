import subprocess

# Define the command
curl_command = "curl https://ollama.ai/install.sh | sh"

# Run the command
subprocess.run(curl_command, shell=True)
