import requests

class OMDbService:
    API_URL = 'http://www.omdbapi.com/'
    
    def __init__(self, api_key):
        self._api_key = api_key

    def retrieve_info(self, title):
        """Returns information about the movie title in JSON format."""
        params = {'apikey': self._api_key, 't': title, 'type': 'movie', 'r': 'json'}
        return requests.get(OMDbService.API_URL, params).json()