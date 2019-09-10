from tastedive_service import TasteDiveService
from omdb_service import OMDbService

class SimpleMovieRecommender:
    PRIMARY_SOURCE = 'Internet Movie Database'
    
    def __init__(self, omdb_api_key):
        self._omdb = OMDbService(omdb_api_key)
        self._td = TasteDiveService()
    
    @staticmethod
    def _retrieve_rating(omdb_response):
        for rating in omdb_response['Ratings']:
            if rating['Source'] == SimpleMovieRecommender.PRIMARY_SOURCE:
                return float(rating['Value'].split('/')[0])
        return float(omdb_response['imdbRating'])

    def recommendations(self, titles, limit = 5):
        """
        Return a list of recommended movie titles up to the specified limit.
        The items are ordered according to their ratings (from top to bottom).
        """
        similar_titles = self._td.similar_titles(titles, limit)
        ratings = map(lambda title: SimpleMovieRecommender._retrieve_rating(self._omdb.retrieve_info(title)), 
                      similar_titles)      
        return list(map(lambda item: item[1], sorted(zip(ratings, similar_titles), reverse = True)))