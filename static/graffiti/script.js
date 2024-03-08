// document.addEventListener('DOMContentLoaded', function() {
//     const canvas = document.getElementById('canvas');
//     const ctx = canvas.getContext('2d');
//     var font_size = "40px"
//     var text_color = "#000000"
//     var rotationAngle = 0;
//     const text = { content: "Really Cool Text", x: 50, y: 50, font: `${font_size} aAttackGraffiti` };
  
//     // Off-screen canvas
//     const offscreenCanvas = document.createElement('canvas');
//     const offscreenCtx = offscreenCanvas.getContext('2d');
//     offscreenCanvas.width = canvas.width;
//     offscreenCanvas.height = canvas.height;
  
//     function draw() {
//       // Clear off-screen canvas
//       offscreenCtx.clearRect(0, 0, offscreenCanvas.width, offscreenCanvas.height);
    
//       const img = new Image();
//       img.src = window.location.origin + '/static/graffiti/banner.jpg';
//       img.onload = async function() {
//         // Wait on the font to load
//         await document.fonts.load(text.font);
    
//         // Draw image on off-screen canvas
//         offscreenCtx.drawImage(img, 0, 0, offscreenCanvas.width, offscreenCanvas.height);
    
//         // Set up text properties
//         offscreenCtx.font = text.font;
//         offscreenCtx.fillStyle = text_color;
    
//         // Translate and rotate for text drawing
//         offscreenCtx.save(); // Save current state
//         offscreenCtx.translate(text.x, text.y); // Move to the text's intended x,y position
//         offscreenCtx.rotate(rotationAngle * Math.PI / 180); // Apply rotation
    
//         // Draw the text at (0, 0) since we've translated the context
//         offscreenCtx.fillText(text.content, 0, 0);
    
//         offscreenCtx.restore(); // Restore to the original state before translation and rotation
    
//         // Copy off-screen canvas to visible canvas
//         ctx.clearRect(0, 0, canvas.width, canvas.height);
//         ctx.drawImage(offscreenCanvas, 0, 0);
//       };
//     }
    
  
//     function getMousePos(canvas, evt) {
//       const rect = canvas.getBoundingClientRect();
//       return {
//         x: evt.clientX - rect.left,
//         y: evt.clientY - rect.top
//       };
//     }
  
//     let isDragging = false;
//     let offsetX, offsetY;
  
//     canvas.addEventListener('mousedown', function(evt) {
//       const mousePos = getMousePos(canvas, evt);
//       const textWidth = offscreenCtx.measureText(text.content).width;
//       const textHeight = parseInt(text.font, 10); // Rough approximation based on font size
//       if (mousePos.x >= text.x && mousePos.x <= text.x + textWidth && mousePos.y >= text.y - textHeight && mousePos.y <= text.y) {
//         isDragging = true;
//         offsetX = mousePos.x - text.x;
//         offsetY = mousePos.y - text.y;
//       }
//     });
  
    
  
//     canvas.addEventListener('mousemove', function(evt) {
//       if (isDragging) {
//         const mousePos = getMousePos(canvas, evt);
//         text.x = mousePos.x - offsetX;
//         text.y = mousePos.y - offsetY;
//         draw();
//       }
//     });
  
//     canvas.addEventListener('mouseup', function() {
//       isDragging = false;
//     });
  
//     draw();




//     // Text manipulation 

//     // Add event listener for font selector changes
//     document.getElementById('fontSelector').addEventListener('change', function(e) {
//         const selectedFont = e.target.value;
//         text.font = `${font_size} ${selectedFont}`;
//         draw();
//     });

//     // Add an event listener for font size slider
//     document.getElementById('fontSize').addEventListener('input', function(e) {
//         font_size = e.target.value + "px";
//         text.font = `${font_size} ${document.getElementById('fontSelector').value}`;
//         for(let i = 0; i < 20; i++) {
//             draw();
//         }
//     });

//     // Add event listener for font color picker
//     document.getElementById('fontColor').addEventListener('input', function(e) {
//       text_color = e.target.value;
//       draw();
//     });

//     // Add event listener for a rotation slider/input
//     document.getElementById('rotationSlider').addEventListener('input', function(e) {
//       rotationAngle = e.target.value;
//       draw();
//     });




//     // Save button
//     document.getElementById('saveButton').addEventListener('click', function() {
//         const imageDataURL = canvas.toDataURL('image/jpg');
//         saveImage(imageDataURL);
//       });
    
//       function saveImage(imageDataURL) {
//         fetch('http://127.0.0.1:8000/graffiti/save_image', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//           },
//           body: JSON.stringify({ image_data: imageDataURL }),
//         })
//         .then(response => {
//           if (!response.ok) {
//             throw new Error('Failed to save image');
//           }
//           console.log('Image saved successfully');
//           // Optionally handle success response
//         })
//         .catch(error => {
//           console.error('Error saving image:', error);
//           // Optionally handle error
//         });
//       }
//   });
// If the page isn't 127.0.0.1, redirect to https://
if (window.location.hostname !== '127.0.0.1') {
  if (window.location.protocol === 'http:') {
    window.location.href = window.location.href.replace('http:', 'https:');
  }
}

document.addEventListener('DOMContentLoaded', function() {

  var canvas = new fabric.Canvas('canvas');

  // Function to resize and scale the canvas and its contents
  function resizeAndScaleCanvas() {
      // Adjust these variables according to your initial canvas dimensions or the desired aspect ratio
      const container = document.getElementById('canvasContainer'); // Ensure you have a container with this ID
      const scaleRatio = container.offsetWidth / canvas.getWidth();

      canvas.setWidth(container.offsetWidth);
      canvas.setHeight(canvas.getHeight() * scaleRatio);

      canvas.getObjects().forEach(function(object) {
          object.scaleX *= scaleRatio;
          object.scaleY *= scaleRatio;
          object.left *= scaleRatio;
          object.top *= scaleRatio;
          object.setCoords();
      });

      if (canvas.backgroundImage) {
          // Adjust the background image to cover the new canvas size
          var bi = canvas.backgroundImage;
          bi.scaleX = canvas.width / bi.width;
          bi.scaleY = canvas.height / bi.height;
      }

      canvas.renderAll();
      canvas.calcOffset();
  }

  // Initial resize and scale
  resizeAndScaleCanvas();

  // Listen to window resize event to adjust the canvas accordingly
  window.addEventListener('resize', resizeAndScaleCanvas);

    // Load font
    async function loadFont(fontName) {
      return new Promise((resolve, reject) => {
        if ('fonts' in document) {
          document.fonts.load(`10pt "${fontName}"`).then(() => {
            console.log(`${fontName} font loaded`);
            resolve();
          }).catch(error => {
            console.error(`Failed to load ${fontName} font`, error);
            reject(error);
          });
        } else {
          // Fallback if Font Loading API is not supported
          console.warn('Font Loading API not supported. Attempting to set font directly.');
          resolve();
        }
      });
    }

// Function to load image with empty cache and hard reload
function loadImageWithHardReload(url, callback) {
  var timestamp = new Date().getTime(); // Adding timestamp to URL to ensure it's always different
  var newUrl = url + '?' + timestamp; // Appending timestamp to URL
  fabric.Image.fromURL(newUrl, function(img) {
      // Execute callback function once image is loaded
      if (typeof callback === 'function') {
          callback(img);
      }
  });
}
  
  // Load the background image and scale it
  const username = document.getElementById('username').getAttribute('username');
  const opacity = .50;
  loadImageWithHardReload(window.location.origin + `/static/graffiti/banner_${username}.jpg`, function(img) {
      img.set({
          scaleX: canvas.width / img.width,
          scaleY: canvas.height / img.height,
          opacity: opacity
      });
      canvas.setBackgroundImage(img, function() {
          canvas.renderAll();
          resizeAndScaleCanvas();
      }, {
          originX: 'left',
          originY: 'top',
      });
  });
  
  var initialFontSize = window.innerWidth < 600 ? 20 : 40;
  var text = new fabric.IText('leave a note', {
    left: 50,
    top: 50,
    fontFamily: 'Trebuchet MS',
    fontSize: initialFontSize,
    fill: '#000000',
    selectable: true,
  });
  canvas.add(text);
  canvas.setActiveObject(text);

  // Listener for text input changes
  document.getElementById('textInput').addEventListener('change', function(e) {
    text.set('text', e.target.value);
    canvas.renderAll();
  });

  // Listener for font selection changes
  document.getElementById('fontSelector').addEventListener('change', function(e) {
    loadFont(e.target.value).then(() => {
      text.set('fontFamily', e.target.value);
      canvas.renderAll();
    });
  });

    // Function to update single color fill
    function updateSingleColor() {
      var color = document.getElementById('singleColor').value;
      text.set('fill', color);
      canvas.renderAll();
  }

  // Function to update gradient fill
  function updateGradient() {
      var color1 = document.getElementById('color1').value;
      var color2 = document.getElementById('color2').value;

      text.set('fill', new fabric.Gradient({
          type: 'linear',
          coords: { x1: 0, y1: 0, x2: text.width, y2: 0 },
          colorStops: [
              { offset: 0, color: color1 },
              { offset: 1, color: color2 }
          ]
      }));
      canvas.renderAll();
  }

  // Event listeners for color changes
  document.getElementById('singleColor').addEventListener('input', updateSingleColor);
  document.getElementById('color1').addEventListener('input', updateGradient);
  document.getElementById('color2').addEventListener('input', updateGradient);

  // Function to scale canvas to a specific size (1500x500) and adjust its content
  function scaleCanvasToSpecificSize() {
    const targetWidth = 1500;
    const targetHeight = 500;
    const scaleX = targetWidth / canvas.getWidth();
    const scaleY = targetHeight / canvas.getHeight();
    
    // Resize the canvas
    canvas.setWidth(targetWidth);
    canvas.setHeight(targetHeight);
    
    // Scale and reposition the canvas background image
    if (canvas.backgroundImage) {
      const bgImg = canvas.backgroundImage;
      bgImg.scaleX *= scaleX;
      bgImg.scaleY *= scaleY;
      bgImg.top *= scaleY;
      bgImg.left *= scaleX;
      bgImg.setCoords();
    }
    
    // Scale and reposition all objects (e.g., text) on the canvas
    canvas.getObjects().forEach(function(object) {
      object.scaleX *= scaleX;
      object.scaleY *= scaleY;
      object.left *= scaleX;
      object.top *= scaleY;
      object.setCoords();
    });
    
    
    canvas.renderAll();
    canvas.calcOffset();
  }


  // Zoom buttons
  document.getElementById('zoomInButton').addEventListener('click', function() {
    var currentZoom = parseFloat(document.getElementById('canvasContainer').style.zoom) || 1;
    var newZoom = currentZoom + 0.1; // Increase zoom by 10%
    // document.body.style.zoom = newZoom;
    // Zoom just the canvas container
    document.getElementById('canvasContainer').style.zoom = newZoom;
  });

  document.getElementById('zoomOutButton').addEventListener('click', function() {
    var currentZoom = parseFloat(document.getElementById('canvasContainer').style.zoom) || 1;
    var newZoom = currentZoom - 0.1; // Decrease zoom by 10%
    // document.body.style.zoom = newZoom;
    document.getElementById('canvasContainer').style.zoom = newZoom;
  });

  // Save button functionality
  document.getElementById('saveButton').addEventListener('click', function() {
    // Get the current text content
    const currentText = text.text;

    // Validation
    if (currentText.trim() === '' || currentText === 'leave a note') {
        alert('Don\'t leave the defualt text :)');
    } else {
        // Scale image to 1500 by 500
        scaleCanvasToSpecificSize();
        // Make the image 0% opaque (fully visible)
        canvas.backgroundImage.set('opacity', 1);
        const imageDataURL = canvas.toDataURL({ format: 'jpg' });
        saveImage(imageDataURL);
        // Scale screen back up/down
        resizeAndScaleCanvas();
        resizeAndScaleCanvas();
        // Set the opacity again
        canvas.backgroundImage.set('opacity', opacity);
    }
  });
  
    // Function to save image
    function saveImage(imageDataURL, event) {

        // Get the CSRF token from a hidden input field 
        var csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

        fetch(window.location.origin + `/graffiti/save_image/${username}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ image_data: imageDataURL }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to save image');
            }
            console.log('Image saved successfully');
            document.getElementById('goodMessage').textContent = 'Image saved successfully';
            document.getElementById('profileLink').style.display = 'block';
            // Reload the image
            loadImageWithHardReload(window.location.origin + `/static/graffiti/banner_${username}.jpg`, function(img) {
                img.set({
                    scaleX: canvas.width / img.width,
                    scaleY: canvas.height / img.height,
                    opacity: opacity
                });
                canvas.setBackgroundImage(img, function() {
                    canvas.renderAll();
                    resizeAndScaleCanvas();
                }, {
                    originX: 'left',
                    originY: 'top',
                });
            });
            // Reset the text content and location
            text.set('text', 'leave another?');
            text.set('left', 50);
            text.set('top', 50);
            canvas.renderAll();
        })
        .catch(error => {
            console.error('Error saving image:', error);
            document.getElementById('errorMessage').textContent = '** Failed to save image **';
        });
    }
});
