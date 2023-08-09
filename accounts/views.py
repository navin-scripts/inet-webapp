from django.shortcuts import render
from django.http import HttpResponse
from social_django.models import UserSocialAuth


# Create your views here.
def authView(request):
    
    return render(request, 'userAuth.html')

def profileView(request):
    
    def microsoftProfile(user_token):
        
        import requests
        import base64
        graph_api_endpoint = "https://graph.microsoft.com/v1.0/me/photo/$value"
        headers = {
            "Authorization": "Bearer " + user_token
        }
        response = requests.get(graph_api_endpoint, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Request successful
            profile_picture_data = response.content
            # Convert the profile picture data to base64
            profile_picture_base64 = base64.b64encode(profile_picture_data).decode("utf-8")
            # Access the profile picture base64 encoded data as needed
            return profile_picture_base64
        else:
            # Request failed
            print("Failed to retrieve profile picture. Status code:", response.status_code)

    def linkedinProfile(user_token):
        import requests
        api_endpoint = "https://api.linkedin.com/v2/me"
        headers = {
            "Authorization": "Bearer " + user_token
        }
        params = {
            "projection": "(id,profilePicture(displayImage~:playableStreams))"
        }
        response = requests.get(api_endpoint, headers=headers, params=params)

        # Check the response status code
        if response.status_code == 200:
            # Request successful
            data = response.json()
            profile_picture_url = data["profilePicture"]["displayImage~"]["elements"][0]["identifiers"][0]["identifier"]
            return profile_picture_url
        else:
            # Request failed
            profile_picture_url = None


    if request.user.is_authenticated:
        user_social_auth = UserSocialAuth.objects.get(id=request.user.id)

        user_token = user_social_auth.extra_data['access_token']
        user_social_provider = user_social_auth.provider

        if user_social_provider == 'linkedin-oauth2': 
            profile_picture_base64 = linkedinProfile(user_token)
            return HttpResponse(f'<img src="{profile_picture_base64}"></img>')
        if user_social_provider == 'microsoft-graph': 
            profile_picture_base64 = microsoftProfile(user_token)
            return HttpResponse(f'<h2>{user_social_provider}</h2><img src="data:image/png;base64,{profile_picture_base64}"')
    else:
        return HttpResponse("<html><head><title>Profile</title></head><body><h1>login first</h1></body></html")
    