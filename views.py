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
import requests
from PIL import Image
from django.contrib.auth.models import User



def index(request):
    if request.method == "GET":
        # If logged in, redirect to u/username
        if request.user.is_authenticated:
            social_account = SocialAccount.objects.get(user=request.user, provider='twitter')
            username = social_account.extra_data.get('screen_name')
            return redirect('graffiti', username=username)
        else:
            # <a href="{% provider_login_url 'twitter' %}">Login with Twitter</a>
            provider_login_url = lambda provider: f"/accounts/{provider}/login/"
            return redirect(provider_login_url('twitter'))

def graffiti(request, username):
    if request.method == "GET":
        # Get banner's user by username
        user = User.objects.get(username=username)
        # Get the banner's associated Twitter account
        social_account = SocialAccount.objects.get(user=user, provider='twitter')
        name = social_account.extra_data.get('name')

        # Get the requester's username
        if request.user.is_authenticated:
            social_account = SocialAccount.objects.get(user=request.user, provider='twitter')
            requester_username = social_account.extra_data.get('screen_name')
        else:
            requester_username = None

        return render(request, "graffiti/graffiti.html", {'username': username, 'name': name, 'requester_username': requester_username})
    
@login_required
def saveTwitterBanner(request):
    # Get associated Twitter account
    social_account = SocialAccount.objects.get(user=request.user, provider='twitter')
    twitter_data = social_account.extra_data  # Access Twitter data
    username = twitter_data.get('screen_name')

    # See if their banner image is already stored in /static/graffiti/banner_username
    if not os.path.exists(f'./static/graffiti/banner_{username}.jpg'):
        # Download their current banner image
        banner_image_url = twitter_data.get('profile_banner_url')  # Get banner URL
        if banner_image_url:
            response = requests.get(banner_image_url, stream=True)

            if response.status_code == 200:
                with open(f'./static/graffiti/banner_{username}.jpg', 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)

                # Copy this image to /graffiti/static/graffiti
                os.system(f'cp ./static/graffiti/banner_{username}.jpg ./graffiti/static/graffiti/banner_{username}.jpg')
            else:
                # Handle error downloading banner image
                print('Error downloading banner image')
        else:
            print('User does not have a banner image')

    # If it this process fails for any reason, make an all white image
    if not os.path.exists(f'./static/graffiti/banner_{username}.jpg'):
        banner_width = 1500  # Adjust as needed
        banner_height = 500  # Adjust as needed
        img = Image.new('RGB', (banner_width, banner_height), color='white')
        img.save(f'./static/graffiti/banner_{username}.jpg')
        os.system(f'cp ./static/graffiti/banner_{username}.jpg ./graffiti/static/graffiti/banner_{username}.jpg')

    return redirect('share')

@login_required
def share(request):
    # Get associated Twitter account
    social_account = SocialAccount.objects.get(user=request.user, provider='twitter')
    twitter_data = social_account.extra_data
    username = twitter_data.get('screen_name')

    return render(request, "graffiti/share.html", {'username': username})


def save_image(request, username):
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
                images_dir_localhost = "graffiti/static/graffiti/"

                # Get twitter username & keys
                user = User.objects.get(username=username)
                social_account = SocialAccount.objects.get(user=user, provider='twitter')
                username = social_account.extra_data.get('screen_name')
                access_token = social_account.socialtoken_set.get(account=social_account).token
                access_token_secret = social_account.socialtoken_set.get(account=social_account).token_secret

                # overwrite the image as banner_username.jpg        
                image_path = os.path.join(images_dir, f'banner_{username}.jpg')
                image_path_localhost = os.path.join(images_dir_localhost, f'banner_{username}.jpg')
                with open(image_path, 'wb') as f:
                    f.write(image_file.read())
                
                # Copy this image to /graffiti/static/graffiti
                os.system(f'cp {image_path} {image_path_localhost}')

                # Get my app's keys
                load_dotenv('./graffiti/keys.env')
                consumer_key = os.getenv('CONSUMER_KEY')
                consumer_secret = os.getenv('CONSUMER_SECRET')

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

