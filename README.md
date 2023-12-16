# Ollama API: A backend service to stream Ollama model responses
Ollama is a fantastic software that allows you to get up and running open-source LLM models quickly. Credits to the team and contributors at Ollama for building such a great software.  The goal of this repository is spin up a version of Ollama running on your HPC / Cloud Service Provider of choice and still interact with the API.

## Support Ollama
[Github](https://github.com/jmorganca/ollama)
[Website](https://ollama.ai/)

## Current Product
We only support python based responses using a simple Flask Route API running on a Linux platform.

## Roadmap
- **Apach Support**:  We plan to support a production service API using WSGI
- **Multi Language** Adding support for additional languages using a REST service
- **Docker** Ensure deployment is seamless and simple using docker

## How to Install

Docker install:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

#### Prerequisites
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
--
Created by [Dublit](https://dublit.org/) - Delivering Ollama to the masses
