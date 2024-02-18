from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.files.base import ContentFile
import base64
import tweepy

def index(request):
    if request.method == "GET":
        return render(request, "graffiti/index.html")
    
def temp(request):
    if request.method == "GET":
        return render(request, "graffiti/temp.html")
    
@csrf_exempt
def save_image(request):
    if request.method == "POST":
        if request.body:  # Check if the request body has content
           try:
                data = json.loads(request.body)
                # Process the data here
                # Assuming you receive a JSON payload with an image_data field
                data = json.loads(request.body)
                image_data = data.get('image_data')
                if not image_data:
                    return JsonResponse({'error': 'No image data provided'}, status=400)

                # Strip the header from the image data
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]  # You should validate this is 'jpeg'

                # Decode the base64 data
                image_file = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

                # Define the path where you want to save the image
                # Ensure this directory exists and is writable by your Django application
                images_dir = "./static/graffiti/"
                #images_dir = "graffiti/static/graffiti/"

                # overwrite the image as banner.jpg        
                image_path = os.path.join(images_dir, 'banner.jpg')
                with open(image_path, 'wb') as f:
                    f.write(image_file.read())

                # Update my twitter banner
                # Your Twitter API credentials
                consumer_key = 'UfehC4dEmEVOcan9ic85xJGp1'
                consumer_secret = 'VGyJaOboaNdSvGK3Jcef7X3CJ4S6Jo8111jylS0sxMoYGNoURh'
                access_token = '1206002867917774848-HvptijLOkHdfVZbRsKSDOQhlOrzhEa'
                access_token_secret = 'GUhlXTjuWr7XbkTYIohuYjjcoqMNf0t82WhACBol2BVtn'

                # Authenticate with the Twitter API
                auth = tweepy.OAuth1UserHandler(
                    consumer_key, consumer_secret,
                    access_token, access_token_secret
                )
                api = tweepy.API(auth)

                # Update banner
                api.update_profile_banner(filename=image_path)

                return JsonResponse({'status': 'success', 'message': 'Image saved successfully'})

           except json.decoder.JSONDecodeError:
               return HttpResponseBadRequest("Invalid JSON data")
        else:
           return HttpResponseBadRequest("Missing JSON data")
            
    else:
        return JsonResponse({'status': 'fail', 'message': 'GET request'})

