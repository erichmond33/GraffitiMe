from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.files.base import ContentFile
import base64
import tweepy
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == "GET":
        return render(request, "graffiti/index.html")
    
def temp(request):
    if request.method == "GET":

        # try:
        #     social_app = SocialApp.objects.get(provider='twitter')
        #     print('Found Twitter SocialApp with ID:', social_app.id)
        #     print('SITE_ID:', social_app.sites.all()[0].id)
        # except SocialApp.DoesNotExist:
        #     print('Twitter SocialApp not found!')

        return render(request, "graffiti/temp.html")
    
@login_required
def profile_view(request):
    # Get associated Twitter account
    # try:
    social_account = SocialAccount.objects.get(user=request.user, provider='twitter')
    twitter_data = social_account.extra_data  # Access Twitter data
    
    # except SocialAccount.DoesNotExist:
    #     # Handle if no Twitter account is linked
    #     return redirect('temp') 

    # Example of accessing Twitter data (replace with what you need)
    username = twitter_data.get('screen_name')
    name = twitter_data.get('name')

    # Send a tweet with this user
    access_token = social_account.socialtoken_set.get(account=social_account).token
    access_token_secret = social_account.socialtoken_set.get(account=social_account).token_secret

    context = {
        'username': username, 
        'name': name,
        'access_token': access_token,
        'access_token_secret': access_token_secret
    }
    return render(request, 'graffiti/profile.html', context)
    
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
                load_dotenv()
                consumer_key = os.getenv('CONSUMER_KEY')
                consumer_secret = os.getenv('CONSUMER_SECRET')
                access_token = os.getenv('ACCESS_TOKEN')
                access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

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

