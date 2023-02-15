import math
import pickle

import pandas as pd
import numpy as np
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def getSuggestions(give_movie):
    #####LOAD DATA
    movies = pd.read_csv("movies.csv")
    #####SELECT FEATURES
    selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
    for feature in selected_features:
        movies[feature] = movies[feature].fillna('')
    #####MAKE SINGLE STRING OF FEATURES
    combined_features = movies['genres'] + ' ' + movies['keywords'] + ' ' + movies['tagline'] + ' ' + movies[
        'cast'] + ' ' + movies['director']

    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)

    similarity = cosine_similarity(feature_vectors)

    list_of_all_titles = movies['title'].tolist()

    find_close_match = difflib.get_close_matches(give_movie, list_of_all_titles)

    close_match = find_close_match[0]

    index_of_the_movie = movies[movies.title == close_match]['index'].values[0]

    similarity_score = list(enumerate(similarity[index_of_the_movie]))

    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)[:10]

    i = 1
    response = []
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies[movies.index == index]['title'].values[0]
        link_from_index = movies[movies.index == index]['homepage'].values[0]
        director_from_index = movies[movies.index == index]['director'].values[0]
        director_from_index =bytes(director_from_index, 'utf-8').decode('unicode-escape')
        rating_from_index = movies[movies.index == index]['vote_average'].values[0]
        # print(title_from_index, link_from_index)
        # print(type(title_from_index))
        if not isinstance(title_from_index, str):
            if math.isnan(float(title_from_index)):
                title_from_index = "Unknown"

        if not isinstance(link_from_index, str):
            if math.isnan(float(link_from_index)):
                link_from_index = "https://google.com/"

        if not isinstance(director_from_index, str):
            if math.isnan(float(director_from_index)):
                director_from_index = "Unknown"

        if not isinstance(rating_from_index, str):
            if math.isnan(float(rating_from_index)):
                rating_from_index = "NA"
        print(director_from_index)

        # print(title_from_index, link_from_index)

        if (i < 11):
            #print(i, '.', title_from_index)
            response.append({"title":title_from_index,"link":link_from_index, "rating":rating_from_index, "director":director_from_index })
            i += 1

    return {"items":response}

