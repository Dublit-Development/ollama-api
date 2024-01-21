# Ollama API: A backend server to interact with Ollama and Stable Diffusion
Ollama is a fantastic software that allows you to get up and running open-source LLM models quickly alongside with Stable Diffusion this repository is the quickest way to chat with multiple LLMs, generate images and perform VLM analysis.  The complied code will deploy a Flask Server on your choice of hardware.

![demo](/assets/demo.png)

## Roadmap
- **Apache Support**:  We plan to support a production service API using WSGI 
- **Restful Support** Creating a quick RESTful deployment to query your favorite models with ease
- **Docker** Ensure deployment is seamless and simple using docker
- **API Route Documentation** Documentation to create your own interfaces or interactions with the backend service

## How to Run
1. Complete all the prequisite steps
2. Run the program `python3 app.py`

![run](./assets/run_server.gif)

#### Interact with the server (UI)
We made this task as simple as possile using the powers of Replit and Valdi.  Valdi is our HPC provider which runs the backend and infrastucture to chat, generate images and perform VLM analysis.  Replit serves as a easy way to deploy our Modular UI to perform actions speciffic to the server.  You can easily fork our public UI on Replit to configure any changes but also interact with the backend service.  Only two steps are required:
1. Fork the UI on Replit
2. When prompted enter your Server Address into the secrets manager

[Modular LLM UI](https://replit.com/@bkr-studio/VALDI-LLMs-1?v=1)

#### Hardware Specs
Ensure that you have a machine with the following Hardware Specifications:
1. Ubuntu Linux or Macintosh (Windows is not supported)
2. 32 GB of RAM
3. 6 CPUs/vCPUs
4. 50 GB of Storage
5. NVIDIA GPU

#### Prerequisites
1. In order to run Ollama including Stable Diffusion models you must create a read-only HuggingFace API key.  [Creation of API Key](https://huggingface.co/docs/hub/security-tokens)
2. Upon completion of generating an API Key you need to edit the config.json located in the `./app/config.json`

![config](./assets/config_demo.gif)
3. Install neccessary dependencies and requirements: 

```sh
# Update your machine (Linux Only)
sudo apt-get update
# Install pip
sudo apt-get install python3-pip 
# Navigate to the directory containing requirements.txt
./app
# Run the pip install command
pip install -r requirements.txt
```

## VALDI Modular LLM Fontend
This project contains a user interface for interacting with various language models through chat in the browser. It integrates with the Modular LLM backend server to allow users to select different models, send messages, and view responses.

The Modular LLM backend server can be found at the following [Github](https://github.com/Dublit-Development/ollama-api)

It would be great if you can support the project and give it a ⭐️.

### Features

- **Dynamic Model Selection**: Users can select from a range of installed language models to interact with.
- **Installation Management**: Users can install or uninstall models by dragging them between lists.
- **Chat Interface**: Interactive chat area for users to communicate with the chosen language model.
- **Support for Text-to-Image Generation**: It includes a feature to send requests to a Stable Diffusion endpoint for text-to-image creation.
- **Image Uploads for LLaVA**: Allows image uploads when interacting with the LLaVA model.

### Frontend

- **HTML**: `templates/index.html` provides the structure of the chat interface and model management area.
- **JavaScript**: `static/js/script.js` contains all the interactive logic, including event listeners, fetch requests, and functions for managing models.
- **CSS**: `static/css/style.css` presents the styling for the web interface.

### Proxy-Backend

- **Python with Flask**: `main.py` acts as the server, handling the various API endpoints, requests to the VALDI endpoint, and serving the frontend files. While python, this is more of a frontend file than backend; similar to cloud functions on firebase. It functions as a serverless backend endpoint, but is a proxy to your real backend

### API Endpoints
This directly interacts with the Backend Server hosted on VALDI.

- `/`: Serves the main chat interface.
- `/api/chat`: Handles chat messages sent to different language models.
- `/api/llava`: Specialized chat handler for the LLaVA model that includes image data.
- `/txt2img`: Endpoint for handling text-to-image generation requests.
- `/list-models`: Returns the list of available models installed on the server.
- `/install-model`: Installs a given model.
- `/uninstall-model`: Uninstalls a given model.
- `/install`: Endpoint used for initial setup, installing necessary components.

### Installation Instructions

To get the VALDI Modular LLM Chat Interface running:

1. Fork or clone this repository to your local machine or Replit environment.
2. Install the required Python modules with `pip install -r requirements.txt` or run the program to install dependencies on Replit.
4. Set the `VALDI_ENDPOINT` stored in secrets on Replit environment variable to your backend's endpoint.
5. Run `main.py` to start the Flask server.
6. Access the web interface by opening `localhost:81` in your web browser (or the port you configured), or in the webview of Replit.

## Credits ✨
This project would not be possible without continous contributions from the Open Source Community.
### Ollama
[Ollama Github](https://github.com/jmorganca/ollama)

[Ollama Website](https://ollama.ai/)

### @cantrell
[Cantrell Github](https://github.com/cantrell)

[Stable Diffusion API Server](https://github.com/cantrell/stable-diffusion-api-server)

### Valdi
Our preferred HPC partner  🖥️

[Valdi](https://valdi.ai/)

[Support us](https://valdi.ai/signup?ref=YZl7RDQZ)

### Replit
Our preferred IDE and deployment platform  🚀

[Replit](https://replit.com/)

--
Created by [Dublit](https://dublit.org/) - Delivering Ollama to the masses

# Cuda update drivers 
sudo apt-get install -y cuda-drivers


# directory permission error 
chmod 600 Ojama.pem

# update python version
https://cloudbytes.dev/snippets/upgrade-python-to-latest-version-on-ubuntu-linux

# Enable 5000 firewall
sudo ufw allow 5000
sudo ufw status