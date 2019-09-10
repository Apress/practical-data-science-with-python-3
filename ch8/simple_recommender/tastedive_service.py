import requests

class TasteDiveService:
    SUPPORTED_ARTIFACTS = ['music', 'movies', 'shows', 'podcasts', 'books', 'authors', 'games']
    API_URL = 'https://tastedive.com/api/similar'
    
    def __init__(self, artifact_type = 'movies'):
        assert artifact_type in TasteDiveService.SUPPORTED_ARTIFACTS, 'Invalid artifact type'

        self._artifact_type = artifact_type

    def _retrieve_artifacts(self, name, limit):
        params = {'q': name, 'type': self._artifact_type, 'limit': limit} 
        return requests.get(TasteDiveService.API_URL, params).json()

    @staticmethod
    def _extract_titles(response):
        artifacts = response['Similar']['Results']
        return [artifact['Name'] for artifact in artifacts]
    
    def similar_titles(self, titles, limit = 5):
        """
        Returns a set of similar titles up to the defined limit. Each instance of
        this class is supposed to work only with one artifact type. This type is specified
        during object construction.
        """
        assert 0 < limit <= 50, 'Limit must be in range (0, 50].'

        return {similar_title 
                for title in titles
                    for similar_title in TasteDiveService._extract_titles(self._retrieve_artifacts(title, limit))}
