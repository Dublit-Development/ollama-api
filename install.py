import subprocess

# Define the command
curl_command = "curl https://ollama.ai/install.sh | sh"

llama2 = "ollama pull llama2"


""" Create a while loop with options."""
# Run the command
subprocess.run(curl_command, shell=True)

subprocess.run(llama2)
