from flask import Flask, request, jsonify, render_template
import subprocess, sys
import json
import re
import sys
import base64
from PIL import Image
from io import BytesIO
import torch
import diffusers
import os


app = Flask(__name__)


'''
made with <3 by
      .o8               .o8       oooo   o8o      .   
     "888              "888       `888   `"'    .o8   
 .oooo888  oooo  oooo   888oooo.   888  oooo  .o888oo 
d88' `888  `888  `888   d88' `88b  888  `888    888   
888   888   888   888   888   888  888   888    888   
888   888   888   888   888   888  888   888    888 . 
`Y8bod88P"  `V88V"V8P'  `Y8bod8P' o888o o888o   "888"    

below is a mix of Flask API functionality and Stable Diffusion model installations

The Stable Diffusion installations will check for what isinstalled on your machine, and install the
requirements that are missing. After the first boot, the installer will only connect and load
the engines into memory and not install anything new. Roughly 6GB of disk space needed
to download all of the necessary packages for the models


Massive thank you to @cantrell on GitHub for their open source contributions related
to Stable Diffusion 
'''
OLLAMA_INSTALL = False

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/api/question', methods=['POST'])
def process_question():
    # Get the question from the request
    data = request.get_json()
    question = data.get('question', '')
    model = data.get('model', '')

    # Run a command and capture the output
    result = run_model_question(question, model)
    print(result)

    # Return the result as JSON
    return jsonify({"message":result})

@app.route('/api/vlm', methods=['POST'])
def vlm_model():
    data = request.get_json()
    model = data.get('model', '')
    prompt = data.get('prompt', '')
    image = data.get('image', '')

    result = run_vlm_question(model, prompt, image)

    # Return the result as a JSON
    return jsonify({"message":result})

@app.route('/api/pull', methods=['POST'])
def pull_model():
    data = request.get_json()
    model = data.get('model', '')

    result = run_pull_model(model)
    print(result)

    return jsonify({"message":result})

# change to post if it doesnt work. some intermediaries block json body when attatched to a DELETE
@app.route('/api/delete', methods=['DELETE']) 
def delete_model():
    data = request.get_json()
    model = data.get('model', '')

    result = run_delete_model(model)
    print(result)

    return jsonify({"message":result})

@app.route('/api/install', methods=['GET'])
def install():
    global OLLAMA_INSTALL

    if not OLLAMA_INSTALL:
        response = install_ollama()
        OLLAMA_INSTALL = True
        return jsonify({'message': response})
    else:
        return jsonify({'message': 'OLLAMA_INSTALL is already set to True'})

@app.route('/api/list-models', methods=['GET'])
def listModels():
    res = listInstalledModels()
    return jsonify({'models':res})

######  HELPER FUNCTIONS   ######
def listInstalledModels():
    curl_command = f'curl http://localhost:11434/api/tags'

    output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')
    res = json.loads(output)

    return res

def run_delete_model(model):
    # Define the curl command
    curl_command = f'curl -X DELETE http://localhost:11434/api/delete -d \'{{"name": "{model}"}}\''

    output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')

    response = json.loads(output)
    return response

def run_pull_model(model):
    # Define the curl command
    curl_command = f'curl http://localhost:11434/api/pull -d \'{{"name": "{model}", "stream": false}}\''

    # Run the command and capture the output
    output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')

    response = json.loads(output)
    return response

def run_vlm_question(model, prompt, image):
    # Define the curl command
    #curl_command = f'curl http://localhost:11434/api/generate -d \'{{"model": "{model}", "prompt": "{prompt}", "stream": false, "images": ["{image}"]}}\''
    curl_command = f'curl http://localhost:11434/api/generate -d \'{{"model": "{model}", "prompt": "{prompt}", "stream": false, "images": ["{image[0]}"]}}\''

    # Run the command and capture the output
    output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')
    print(output)
    # Parse the JSON string in the output variable
    output_json = json.loads(output)
    print(output_json)

    # Extract the "response" value
    responses = output_json.get("response", None)

    # Create a JSON containing only "response" values
    response_json = {'responses': responses}

    return response_json

def run_model_question(question, model):
    # Define the curl command
    curl_command = f'curl http://localhost:11434/api/generate -d \'{{"model": "{model}", "prompt": "{question}"}}\''

    # Run the command and capture the output
    output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')

    # Process the output as JSON and extract "response" values
    responses = [json.loads(response)["response"] for response in output.strip().split('\n')]

    # Create a JSON containing only "response" values
    response_json = {'responses': responses}

    return response_json

def working_directory():
    
    # Get the current working directory
    current_directory = os.getcwd()

    # Define the file name you are looking for
    file_to_find = "config.json"

    # Contruct the full path to the file
    file_path = os.path.join(current_directory, file_to_find)

    return file_path

def install_ollama():
    try:
        curl_command = 'curl https://ollama.ai/install.sh | sh'
        # Use curl to install latest Ollama package
        subprocess.check_call(curl_command, shell=True, encoding='utf-8')
        
        return "Success"

    except subprocess.CalledProcessError as e:
        # print(f"Error downloading Ollama: {e}")
        return e

##################################################
# Utils

def retrieve_param(key, data, cast, default):
    if key in data:
        value = request.form[ key ]
        value = cast( value )
        return value
    return default

def pil_to_b64(input):
    buffer = BytesIO()
    input.save( buffer, 'PNG' )
    output = base64.b64encode( buffer.getvalue() ).decode( 'utf-8' ).replace( '\n', '' )
    buffer.close()
    return output

def b64_to_pil(input):
    output = Image.open( BytesIO( base64.b64decode( input ) ) )
    return output

def get_compute_platform(context):
    try:
        import torch
        if torch.cuda.is_available():
            return 'cuda'
        elif torch.backends.mps.is_available() and context == 'engine':
            return 'mps'
        else:
            return 'cpu'
    except ImportError:
        return 'cpu'

##################################################
# Engines

class Engine(object):
    def __init__(self):
        pass

    def process(self, kwargs):
        return []

class EngineStableDiffusion(Engine):
    def __init__(self, pipe, sibling=None, custom_model_path=None, requires_safety_checker=True):
        super().__init__()
        if sibling == None:
            self.engine = pipe.from_pretrained( 'runwayml/stable-diffusion-v1-5', use_auth_token=hf_token.strip() )
        elif custom_model_path:
            if requires_safety_checker:
                self.engine = diffusers.StableDiffusionPipeline.from_pretrained(custom_model_path,
                                                                                safety_checker=sibling.engine.safety_checker,
                                                                                feature_extractor=sibling.engine.feature_extractor)
            else:
                self.engine = diffusers.StableDiffusionPipeline.from_pretrained(custom_model_path,
                                                                                feature_extractor=sibling.engine.feature_extractor)
        else:
            self.engine = pipe(
                vae=sibling.engine.vae,
                text_encoder=sibling.engine.text_encoder,
                tokenizer=sibling.engine.tokenizer,
                unet=sibling.engine.unet,
                scheduler=sibling.engine.scheduler,
                safety_checker=sibling.engine.safety_checker,
                feature_extractor=sibling.engine.feature_extractor
            )
        self.engine.to( get_compute_platform('engine') )

    def process(self, kwargs):
        output = self.engine( **kwargs )
        return {'image': output.images[0], 'nsfw':output.nsfw_content_detected[0]}

class EngineManager(object):
    def __init__(self):
        self.engines = {}

    def has_engine(self, name):
        return ( name in self.engines )

    def add_engine(self, name, engine):
        if self.has_engine( name ):
            return False
        self.engines[ name ] = engine
        return True

    def get_engine(self, name):
        if not self.has_engine( name ):
            return None
        engine = self.engines[ name ]
        return engine

##################################################
# App

# Load and parse the config file:
try:
    config_file = open(working_directory(), 'r')
except:
    sys.exit('config.json not found.')

config = json.loads(config_file.read())

hf_token = config['hf_token']

if (hf_token == None):
    sys.exit('No Hugging Face token found in config.json.')

custom_models = config['custom_models'] if 'custom_models' in config else []

# Initialize engine manager:
manager = EngineManager()

# Add supported engines to manager:
manager.add_engine( 'txt2img', EngineStableDiffusion( diffusers.StableDiffusionPipeline,        sibling=None ) )
manager.add_engine( 'img2img', EngineStableDiffusion( diffusers.StableDiffusionImg2ImgPipeline, sibling=manager.get_engine( 'txt2img' ) ) )
manager.add_engine( 'masking', EngineStableDiffusion( diffusers.StableDiffusionInpaintPipeline, sibling=manager.get_engine( 'txt2img' ) ) )
for custom_model in custom_models:
    manager.add_engine( custom_model['url_path'],
                        EngineStableDiffusion( diffusers.StableDiffusionPipeline, sibling=manager.get_engine( 'txt2img' ),
                        custom_model_path=custom_model['model_path'],
                        requires_safety_checker=custom_model['requires_safety_checker'] ) )

# Define routes:
@app.route('/ping', methods=['GET'])
def stable_ping():
    return jsonify( {'status':'success'} )

@app.route('/custom_models', methods=['GET'])
def stable_custom_models():
    if custom_models == None:
        return jsonify( [] )
    else:
        return custom_models

@app.route('/txt2img', methods=['POST','GET'])
def stable_txt2img():
    return _generate('txt2img')

@app.route('/img2img', methods=['POST'])
def stable_img2img():
    return _generate('img2img')

@app.route('/masking', methods=['POST'])
def stable_masking():
    return _generate('masking')

@app.route('/custom/<path:model>', methods=['POST'])
def stable_custom(model):
    return _generate('txt2img', model)

def _generate(task, engine=None):
    # Retrieve engine:
    if engine == None:
        engine = task

    engine = manager.get_engine( engine )

    # Prepare output container:
    output_data = {}

    # Handle request:
    try:
        seed = retrieve_param( 'seed', request.form, int, 0 )
        count = retrieve_param( 'num_outputs', request.form, int,   1 )
        total_results = []
        for i in range( count ):
            if (seed == 0):
                generator = torch.Generator( device=get_compute_platform('generator') )
            else:
                generator = torch.Generator( device=get_compute_platform('generator') ).manual_seed( seed )
            new_seed = generator.seed()
            prompt = request.get_json(force=True).get('prompt')
            args_dict = {
                'prompt' : [ prompt ],
                'num_inference_steps' : retrieve_param( 'num_inference_steps', request.form, int,   100 ),
                'guidance_scale' : retrieve_param( 'guidance_scale', request.form, float, 7.5 ),
                'eta' : retrieve_param( 'eta', request.form, float, 0.0 ),
                'generator' : generator
            }
            if (task == 'txt2img'):
                args_dict[ 'width' ] = retrieve_param( 'width', request.form, int,   512 )
                args_dict[ 'height' ] = retrieve_param( 'height', request.form, int,   512 )
            if (task == 'img2img' or task == 'masking'):
                init_img_b64 = request.form[ 'init_image' ]
                init_img_b64 = re.sub( '^data:image/png;base64,', '', init_img_b64 )
                init_img_pil = b64_to_pil( init_img_b64 )
                args_dict[ 'init_image' ] = init_img_pil
                args_dict[ 'strength' ] = retrieve_param( 'strength', request.form, float, 0.7 )
            if (task == 'masking'):
                mask_img_b64 = request.form[ 'mask_image' ]
                mask_img_b64 = re.sub( '^data:image/png;base64,', '', mask_img_b64 )
                mask_img_pil = b64_to_pil( mask_img_b64 )
                args_dict[ 'mask_image' ] = mask_img_pil
            # Perform inference:
            pipeline_output = engine.process( args_dict )
            pipeline_output[ 'seed' ] = new_seed
            total_results.append( pipeline_output )
        # Prepare response
        output_data[ 'status' ] = 'success'
        images = []
        for result in total_results:
            images.append({
                'base64' : pil_to_b64( result['image'].convert( 'RGB' ) ),
                'seed' : result['seed'],
                'mime_type': 'image/png',
                'nsfw': result['nsfw']
            })
        output_data[ 'images' ] = images        
    except RuntimeError as e:
        output_data[ 'status' ] = 'failure'
        output_data[ 'message' ] = 'A RuntimeError occurred. You probably ran out of GPU memory. Check the server logs for more details.'
        print(str(e))
    return jsonify( output_data )

def run_api():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

run_api()