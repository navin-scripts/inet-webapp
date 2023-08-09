from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        import requests
        # Define the API endpoint URL
        url = 'http://localhost:8000/api/kits/'

        # Define your API token (replace 'your-token-here' with your actual API token)
        api_token = '44c317654079e4201c0fcbb8ea13b4434ca926aa'

        # Set the Authorization header with the token
        headers = {
            'Authorization': f'Token {api_token}'
        }

        # Make a GET request to the API endpoint with the headers
        response = requests.get(url, headers=headers)

        # Check the response
        if response.status_code == 200:
            data = response.json()
            for d in data: print(d)
        else:
            print(f"Error: {response.status_code}")
