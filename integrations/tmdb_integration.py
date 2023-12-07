import os
import random

import requests


def discover_movies(emotion):
    try:
        movie_list = []

        for i in range(1, 5):
            url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&vote_average.gte=6&with_origin_country=US&include_video=false&language=en-US&primary_release_year=2016|2017|2018|2019|2020|2021|2022|2023&page={i}&sort_by=popularity.desc&with_genres="

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {os.getenv('TMDB_BEARER_TOKEN')}"
            }

            if emotion == 'sadness':
                genre = "18|35"
                url = url + genre
            elif emotion == 'joy':
                genre = "12|28|16"
                url = url + genre
            elif emotion == 'anger':
                genre = "10751"
                url = url + genre
            elif emotion == 'love':
                genre = "10749"
                url = url + genre
            elif emotion == 'surprise':
                genre = "9648|27"
                url = url + genre
            elif emotion == 'disgust':
                genre = "10402"
                url = url + genre
            else:
                print("Wrong emotion")

            response = requests.get(url, headers=headers).json()
            for result in response['results']:
                movie = {'title': result['original_title'], 'id': result['id'],
                         'image': f'https://image.tmdb.org/t/p/w500{result["backdrop_path"]}',
                         'rating': result['vote_average'],
                         'release_date': result['release_date'],
                         'overview': result['overview']}
                movie_list.append(movie)


        random.shuffle(movie_list)
        return movie_list[:30]
    except Exception as ex:
        print(ex)

