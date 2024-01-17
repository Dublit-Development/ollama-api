

/*
      .o8               .o8       oooo   o8o      .   
     "888              "888       `888   `"'    .o8   
 .oooo888  oooo  oooo   888oooo.   888  oooo  .o888oo 
d88' `888  `888  `888   d88' `88b  888  `888    888   
888   888   888   888   888   888  888   888    888   
888   888   888   888   888   888  888   888    888 . 
`Y8bod88P"  `V88V"V8P'  `Y8bod8P' o888o o888o   "888" 
*/



document.addEventListener('DOMContentLoaded', async function() {
  var currb64Img = ''

  // install ollama on boot
  await fetch('/install', {
      method: 'GET',
    }).then(async(repsonse) => {
    if (repsonse.status == 200) {
      console.log('Stable Diffusion and Ollama are installed on your VALDI machine 🥳🎉')
    }
  
  });

  let isProcessing = false; // flag to control dragging during install/uninstall

  // message sending
  var chatInput = document.getElementById('user-input');
  var chatButton = document.getElementById('send-button');
  var chatArea = document.getElementById('chat-area');
  var modelSelect = document.getElementById('model-select');

  // helper function to keep the chat area scrolled to the bottom
  function scrollToBottom() {
    chatArea.scroll({
      top: chatArea.scrollHeight,
      behavior: 'smooth' // this will make the scroll behavior smooth
    });
  }



  chatButton.addEventListener('click', async function() {
    if (chatInput.value.trim() != '') {
      var message = chatInput.value;
      var model = modelSelect.value;
      chatInput.value = '';
      chatArea.innerHTML += `<p class="userMessage">${message}</p>`;
      scrollToBottom();





      // SEND REQUEST


      switch (model) {
        // text to image endpoint
        case "stablediff":
          await txt2imgRequest(message,'',1,512,512,10,0.5);
          break;
        case "llava":
          await llavaRequest(currb64Img,message,model)
          break;
        // case for all text2text chats
        default:
          try {
            const response = await fetch('/api/chat', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                message: message,
                model: model
              })
            });

            const data = await response.json();
            var resArr = data.message.responses
            var resStr = resArr.join(' ')
            chatArea.innerHTML += `<p class="botMessage">${resStr}</p>`;
            scrollToBottom();
          } catch (error) {
            console.log(error);
            chatArea.innerHTML += `<p class="botMessage">${error}</p>`;
            scrollToBottom();
          }
      }

    }
});

  // send on enter
  chatInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' & chatInput.value.trim() != '') {
      chatButton.click();
    } 
  });  

  // Function to make the POST request
  async function txt2imgRequest(prompt,seed,outputs,width,height,steps,guidance_scale) {
      const url = '/txt2img'; // CHANGE TO YOUR ENDPOINT IN SECRETS

      const requestBody = {
        "prompt": prompt,
        "seed": seed, // Numeric seed
        "num_outputs": outputs, // Number of images
        "width": width, // Width of results
        "height": height, // Height of results
        "num_inference_steps": steps, // Number of inference steps
        "guidance_scale": guidance_scale // Prompt strength
      };

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // Add any other headers if needed
          },
          body: JSON.stringify(requestBody),
        });

        const responseData = await response.json();

        if (responseData.status === 'success') {
          try {
            const image = responseData.image_data;
            // Handle the image, e.g., display it in an HTML img tag
            const imgElement = document.createElement('img');
            // Generate a random ID for the <p> element
            const randomId = `image_${Math.floor(Math.random() * 100000)}`;

            imgElement.src = `data:image/png;base64,${image}`;
            chatArea.innerHTML += `<p id="${randomId}" class="botMessage"></p>`;
            document.getElementById(randomId).append(imgElement)
            scrollToBottom();

            //chatArea.innerHTML += `<p class="botMessage">${responseData.message}</p>`;
          }
          catch {
            chatArea.innerHTML += `<p class="botMessage">caught error</p>`;
            scrollToBottom();
          }

        }
        else {
          console.error(`Request failed: ${responseData.message}`);
          chatArea.innerHTML += `<p class="botMessage">${error}</p>`;
          scrollToBottom();
        }
      } 
      catch (error) {
        console.error('Error:', error);
        chatArea.innerHTML += `<p class="botMessage">${error}</p>`;
        scrollToBottom();
      }
    }


  // function to make a request to llava
  async function llavaRequest(baseEncodedImage,message,model) {
    bImg = baseEncodedImage.split('data:image/png;base64,')[1]
    try {
      const response = await fetch('/api/llava', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          'message': message,
          'model': model,
          'image': bImg
        })
      });

      const data = await response.json();
      var resArr = data.message.responses
      var resStr = resArr
      chatArea.innerHTML += `<p class="botMessage">${resStr}</p>`;
      scrollToBottom();
    } catch (error) {
      console.log(error);
      chatArea.innerHTML += `<p class="botMessage">${error}</p>`;
      scrollToBottom();
    }
  }


  var installedModelsList = document.getElementById('installed');
  var uninstalledModelsList = document.getElementById('uninstalled');

  // Assuming we've got lists of models somewhere, we'd make them draggable like this:


  installedModelsList.innerHTML += '<div id="stablediff" draggable="true" ondragstart="drag(event)" class="model-installer">Stable Diffusion</div>';

  // Making sure the model lists allow dropping
  installedModelsList.ondragover = allowDrop;
  uninstalledModelsList.ondragover = allowDrop;
  installedModelsList.ondrop = drop;
  uninstalledModelsList.ondrop = drop;


  const menuToggler = document.getElementById('menu_toggle');
  const controls = document.getElementById('controls');
  const modelInstaller = document.getElementById('model-lists')
  var open = true;
  menuToggler.addEventListener('click', async(e) => {
    switch(open) {
      case true:
        modelSelect.style.display = 'none';
        modelInstaller.style.display = 'none';
        controls.style.maxHeight = "12px";
        menuToggler.style.marginTop = '-24px';
        menuToggler.style.transform = 'rotate(0deg)';
        open = false;
        break;
      case false:
        modelSelect.style.display = 'flex';
        modelInstaller.style.display = 'flex';
        controls.style.maxHeight = "250px";
        controls.style.height = "128px";
        menuToggler.style.marginTop = '-32px';
        menuToggler.style.transform = 'rotate(180deg)';
        open = true;
        break;
      case _:
        // do nothing
    }

  });



  /* DETECT MODELS INSTALLED */
  var availableModels = [
        'neural-chat',
        'starling-lm',
        'mistral',
        'llama2',
        'codellama',
        'llama2-uncensored',
        'llama2:13b',
        'llama2:70b',
        'orca-mini',
        'vicuna',
        'llava',
        'medllama2'
    ]

  async function getInstalledModels() {
    // call on the list models request
    var response = await fetch('/list-models');
    var data = await response.json();
    var models = data.models;    

    return models
  }

  // get the installed models on boot
  var installedModels = await getInstalledModels();
  var namesArray = [];
  for (var i = 0; i < installedModels.models.length; i++) {
    var modelName = installedModels.models[i].name;
    namesArray.push(modelName);
  }
  var verifiedModels = [];
  var unverifiedModels = [];
  var isEmpty = true;
  for (var i = 0; i < availableModels.length; i++) {
    isEmpty = true; // Reset isEmpty flag for each available model
    for (var j = 0; j < namesArray.length; j++) {
      if (namesArray[j].includes(availableModels[i])) {
        verifiedModels.push(availableModels[i]);
        isEmpty = false; // Set isEmpty to false if a match is found
        break; // Break out of the inner loop once a match is found
      }
    }
    if (isEmpty) {
      unverifiedModels.push(availableModels[i]);
    }
  }
  // inject the verified models into the installed bin
  verifiedModels.forEach(model => {
    var presentedName = ''
    switch(model) {
      case 'neural-chat':
        presentedName = 'Neural Chat'
        break;
      case 'starling-lm':
        presentedName = 'Starling LM'
        break;
      case 'mistral':
         presentedName = 'Mistral'
        break;
      case 'llama2':
         presentedName = 'Llama 2'
        break;
      case 'codellama':
          presentedName = 'CodeLlama'
        break;
      case 'llama2-uncensored':
         presentedName = 'Uncensored Llama 2'
        break;
      case 'llama2:13b':
         presentedName = 'Llama 2 (13B)'
        break;
      case 'llama2:70b':
          presentedName = 'Llama 2 (70B)'
        break;
      case 'orca-mini':
         presentedName = 'Orca Mini'
        break;
      case 'vicuna':
         presentedName = 'Vicuna'
        break;
      default:
        presentedName = model
    }

    var installedModelsList = document.getElementById('installed');

    installedModelsList.innerHTML += `<div id="${model}" draggable="true" ondragstart="drag(event)" class="model-installer">${presentedName}</div>`;

  });

  // inject the unverified models into the uninstalled bin
  unverifiedModels.forEach(model => {
    var presentedName = ''
    switch(model) {
      case 'neural-chat':
        presentedName = 'Neural Chat'
        break;
      case 'starling-lm':
        presentedName = 'Starling LM'
        break;
      case 'mistral':
         presentedName = 'Mistral'
        break;
      case 'llama2':
         presentedName = 'Llama 2'
        break;
      case 'codellama':
          presentedName = 'CodeLlama'
        break;
      case 'llama2-uncensored':
         presentedName = 'Uncensored Llama 2'
        break;
      case 'llama2:13b':
         presentedName = 'Llama 2 (13B)'
        break;
      case 'llama2:70b':
          presentedName = 'Llama 2 (70B)'
        break;
      case 'orca-mini':
         presentedName = 'Orca Mini'
        break;
      case 'vicuna':
         presentedName = 'Vicuna'
        break;
      default:
        presentedName = model
    }
    var uninstalledModelsList = document.getElementById('uninstalled');
    uninstalledModelsList.innerHTML += `<div id="${model}" draggable="true" ondragstart="drag(event)" class="model-installer">${presentedName}</div>`;

  });
  function populateModelsInSelect(){
    // add all installed models to the select dropdown
    var installedModels = document.getElementById('installed').getElementsByClassName('model-installer')
    // clear out the options
    modelSelect.innerHTML = `
    <option value="" disabled selected>Select a Model</option>
    `
    for(var i = 0; i < installedModels.length; i++){
      modelSelect.innerHTML += `
      <option value="${installedModels[i].id}">${installedModels[i].innerText}</option>
      `
    }
  }
    populateModelsInSelect();


  // install/uninstall model on drop
  // Function to install a model
  async function installModel(modelName) {
    if(modelName == 'stablediff'){
      return 'stablediffusion is not able to be uninstalled'
    }
    else {
      try {
      const response = await fetch('/install-model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model_name: modelName }),
      });

      const data = await response.json();
      if (response.ok) {
        return data.message
      } else {
        console.error('Installation error:', data.error);
        return data
      }
    } 
      catch (error) {
        console.error('Fetch error:', error);
        return error
      }
    }

  }

  // Function to uninstall a model
  async function uninstallModel(modelName) {
    if(modelName == 'stablediff'){
      return 'stablediff is not able to be uninstalled'
    }
    else {
      try {
        const response = await fetch('/uninstall-model', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 'model_name': modelName }),
        });
        const data = await response.json();
        if (response.ok) {
          return data.message
        } else {
          console.error('Uninstallation error:', data.error);
          return data
        }
      } catch (error) {
        console.error('Fetch error:', error);
        return error
      }
    }
  }


  // WINDOW DRAG AND DROP MUST GO AT BOTTOM OF LOADED FUNCS
  window.allowDrop = function(event) {
    if(!isProcessing){
      event.preventDefault();
    }
  };

  window.drag = function(event) {
    if(!isProcessing){
      event.dataTransfer.setData("text", event.target.id);
    }
  };


  // Modified drop function
  window.drop = async function(event) {
    if (!isProcessing) { // Only allow dropping if not processing
      event.preventDefault();
      var data = event.dataTransfer.getData("text");
      var draggableElement = document.getElementById(data);

      // Find the closest parent that has the 'model-list' class
      var dropTarget = event.target.closest('.model-list');

      // Only allow drop if the target is '.model-list'
      if (dropTarget) {
        dropTarget.appendChild(draggableElement); // Append to '.model-list'

        isProcessing = true;
        var boxes = document.getElementById('model-lists')
        var loader = document.getElementById('loader');
        boxes.style.display = 'none';
        loader.style.display = 'flex';

        // Check if the model was dropped into 'installed' or 'uninstalled'
        if (dropTarget.id === 'installed') {
          // Call the install model function
          await installModel(draggableElement.id);
        } else if (dropTarget.id === 'uninstalled') {
          // Call the uninstall model function
          await uninstallModel(draggableElement.id);
        }

        isProcessing = false;

        loader.style.display = 'none';
        boxes.style.display = 'flex';


      }
    }
  }

  // Drag and Drop functionality for model installation
  function allowDrop(event) {
    event.preventDefault();
  }

  function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
  }

  async function drop(event) {
    if (!isProcessing) { // Only allow dropping if not processing
      event.preventDefault();
      var data = event.dataTransfer.getData("text");
      var draggableElement = document.getElementById(data);

      // Find the closest parent that has the 'model-list' class
      var dropTarget = event.target.closest('.model-list');

      // Only allow drop if the target is '.model-list'
      if (dropTarget) {
        dropTarget.appendChild(draggableElement); // Append to '.model-list'

        isProcessing = true;
        var boxes = document.getElementById('model-lists')
        var loader = document.getElementById('loader');
        boxes.style.display = 'none';
        loader.style.display = 'flex';

        // Check if the model was dropped into 'installed' or 'uninstalled'
        if (dropTarget.id === 'installed') {
          // Call the install model function
          await installModel(draggableElement.id);
        } else if (dropTarget.id === 'uninstalled') {
          // Call the uninstall model function
          await uninstallModel(draggableElement.id);
        }

        isProcessing = false;

        loader.style.display = 'none';
        boxes.style.display = 'flex';
      }


      // add all installed models to the select dropdown
      var installedModels = document.getElementById('installed').getElementsByClassName('model-installer')
      // clear out the options
      modelSelect.innerHTML = `
      <option value="" disabled selected>Select a Model</option>
      `
      for(var i = 0; i < installedModels.length; i++){
        modelSelect.innerHTML += `
        <option value="${installedModels[i].id}">${installedModels[i].innerText}</option>
        `
      }
    }
  }


  // HANDLE CONDITIONALS


    // Handle file selection and processing for llava
  function handleFileSelect(event) {
      // Retrieve the first file from the FileList object
      let file = event.target.files[0];
      if (file) {
      const reader = new FileReader();

      reader.onload = function(loadEvent) {
        const base64String = loadEvent.target.result;
        // Now you have the base64 string, you can use it where you need it
        currb64Img = base64String
        // Here you could also set up a request to send the base64 string
        // to your server, or handle it in some other way according to your needs.
      };
      reader.readAsDataURL(file);
    }
  }



  document.getElementById('llava-upload-input').addEventListener('change', handleFileSelect, false);

  modelSelect.addEventListener('change', function() {
    if(modelSelect.value == "llava"){
      document.getElementById('llava-file-upload').style.display = 'flex';
    }
    else {
      document.getElementById('llava-file-upload').style.display = 'none';
    }
    // Hide file upload area when the model other than llava is selected
    let uploadArea = document.getElementById('llava-file-upload');

  });





});





var consoleArt =`
      .o8               .o8        oooo  o8o     .   
     "888               "888       888   "'    .o8   
 .oooo888   oooo  oooo  888oooo.   888   oooo  .o888oo 
d88'  888   888   888   d88' 88b   888   888    888   
888   888   888   888   888   888  888   888    888   
888   888   888   888   888   888  888   888    888 . 
Y8bod88P"   V88V"V8P'   'Y8bod8P' o888o o888o   "888" 
`

console.log(consoleArt);
console.log(`interested in projects like this? check out https://dublit.org/`);

  // Call the function to make the request
  //txt2imgRequest();