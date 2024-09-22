import requests
from .parser import CountyParser, DistrictParser, LocationParser, AreaParser
import json

class Fetcher():
    def __init__(self, token):
        self.token = token
    
    def fetch_all(self, url, parser_class):
        # Set the headers with the authentication token
        headers = {'Authorization': f'Token {self.token}'}

        # Make the GET request to the API endpoint
        response = requests.get(url, headers=headers)
    
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the data from the response JSON
            result = response.json()
            #Parse Results
            if result['data']:
                data = parser_class(result['data']).parse()
                return data
            return []
        else:
            # Handle the error response
            print(f'Request error: {response.status_code} - {response.text}')
        
        return None

    def counties(self):
        return self.fetch_all("http://localhost:8000/api/county",CountyParser)
        
    def districts(self):
        return self.fetch_all("http://localhost:8000/api/district",DistrictParser)

    def locations(self):
        return self.fetch_all("http://localhost:8000/api/location",LocationParser)
    
    def areas(self):
        return self.fetch_all("http://localhost:8000/api/area",AreaParser)