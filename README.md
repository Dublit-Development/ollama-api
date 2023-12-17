# Ollama API: A backend service to stream Ollama model responses
Ollama is a fantastic software that allows you to get up and running open-source LLM models quickly. Credits to the team and contributors at Ollama for building such a great software.  The goal of this repository is spin up a version of Ollama running on your HPC / Cloud Service Provider of choice and still interact with the API.

## Current Product
We only support python based responses using a simple Flask Route API running on a Linux platform.

## Roadmap
- **Apache Support**:  We plan to support a production service API using WSGI 
- **Restful Support** Creating a quick RESTful deployment to query your favorite models with ease
- **Docker** Ensure deployment is seamless and simple using docker

## How to Install

Docker install:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04


## Hardware Specs
Ensure that you have a machine with the following Hardware Specifications:
1. Ubuntu Linux
2. 32 GB of RAM
3. 6 CPUs/vCPUs
4. 50 GB of Storage
5. NVIDIA GPU

#### Prerequisites
1. Git clone the 
1. In order to run Ollama including Stable Diffusion models you must create a read-only HuggingFace API key.  [Creation of API Key](https://huggingface.co/docs/hub/security-tokens)

2. Upon completion of generating an API Key you need to edit the config.json located in the `./app/config.json` file.
![config](./assets/config_demo.gif)


You may need to run the following commands on your Linux Server before getting started with the scripts.

```sh
sudo apt-get update 
sudo apt-get install python3-pip 
pip install Flask requests
pip install pillow
pip install torch
pip install diffusers
pip install transformers
pip install accelerate
```
## Credits ✨
This project would not be possible without continous contributions from the Open Source Community.
### Ollama
Massive thanks to Ollama and the contiributors sustaining the project.  This service would not be possible without continued development.

[Ollama Github](https://github.com/jmorganca/ollama)

[Ollama Website](https://ollama.ai/)

### @cantrell
Cantrell is a developer who insipired this modular service to use LLMs and Stable Diffusion inclusively.  Massive thanks to his contribution!

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
