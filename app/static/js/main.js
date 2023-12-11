

/*
      .o8               .o8       oooo   o8o      .   
     "888              "888       `888   `"'    .o8   
 .oooo888  oooo  oooo   888oooo.   888  oooo  .o888oo 
d88' `888  `888  `888   d88' `88b  888  `888    888   
888   888   888   888   888   888  888   888    888   
888   888   888   888   888   888  888   888    888 . 
`Y8bod88P"  `V88V"V8P'  `Y8bod8P' o888o o888o   "888" 


use the function below to TEST the functionality. this will trigger an text to image
request and load it into the browser window 
                                                      
*/



// Function to make the POST request
async function txt2imgRequest() {
    const url = '/txt2img';
  
    const requestBody = {
      "prompt": 'fluffy cat',
      "seed": 123456789, // Numeric seed
      "num_outputs": 1, // Number of images
      "width": 512, // Width of results
      "height": 512, // Height of results
      "num_inference_steps": 10, // Number of inference steps
      "guidance_scale": 0.5 // Prompt strength
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
        const image = responseData.images[0];
        // Handle the image, e.g., display it in an HTML img tag
        const imgElement = document.createElement('img');
        imgElement.src = `data:${image.mimetype};base64,${image.base64}`;
        document.body.appendChild(imgElement);
      } else {
        console.error(`Request failed: ${responseData.message}`);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  
  // Call the function to make the request
  //txt2imgRequest();