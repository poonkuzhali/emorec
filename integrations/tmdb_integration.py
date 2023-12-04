import requests


def discover_movies(emotion):
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres="

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwOTNlOGM5ODRkNjNiMDFiNTg0NTE0ZWZmNDg5NTc4YSIsInN1YiI6IjY1MDM0ZDYwZGI0ZWQ2MTAzNjQwMmZiMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.e54c6oWSx9_4w1llzMG9vSe1Z5XiEUQm1LuszzoPADQ"
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
    movie_list = []
    for result in response['results']:
        movie = {'title': result['original_title'], 'id': result['id'],
                 'image': f'https://image.tmdb.org/t/p/w500{result["backdrop_path"]}',
                 'rating': result['vote_average'],
                 'release_date': result['release_date'],
                 'overview': result['overview']}
        movie_list.append(movie)


    return movie_list

