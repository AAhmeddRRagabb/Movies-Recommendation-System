# ------------------------------------------------------------------------------
# This file is to serve the recommender model
# الله المستعان
# ------------------------------------------------------------------------------

# Imports & global variables

from flask import Flask, render_template, request, jsonify, redirect, url_for
from utils.inference import *


app = Flask(__name__)
PORT = 5000


ID_NOT_FOUND_ERROR = 1
INVALID_INPUT = 2
NO_ERROR = 0


# Rendering the home page
@app.route("/")
def home():
    return render_template('index.html')

# ------------------------------------------------------------------------------------

@app.route("/recommend_for_existing_user", methods = ['post'])
def recommend_for_existing_user():
    # Receiving the message
    payload = request.get_json(silent = True)


    # Validate the payload
    if not payload or not payload['user_id']:
        return jsonify({
            'message': f'Invalid Input. Please, select a valid id.',
            'error': INVALID_INPUT
        })

    user_id = int(payload['user_id'])
    is_new = check_user(user_id)

    # If a new user
    if is_new:
        return jsonify({
            "message" : f'ID {user_id} not found. Please, select your id.',
            'error' : ID_NOT_FOUND_ERROR, 
        })
    

    # Get recommendations & user-preferences
    recommendations = get_recommended_movies(user_id)
    user_preferences = get_user_preferences(user_id)

    titles = recommendations['title']
    genres = recommendations['genres']
    recommended_movies_data = []
    for title, genre in zip(titles, genres):
        recommended_movies_data.append({
            'title'  : title,
            'genres' : genre,
        })

    return jsonify({
        'recommendations': recommended_movies_data,
        'user_preferences': user_preferences,
        'error': NO_ERROR
    })

# ---------------------------------------------------------------------------

@app.route("/recommend_for_new_user", methods = ['post'])
def recommend_for_new_user():
    # Receiving the message
    payload = request.get_json(silent = True)

    # set -> to remove duplicates
    user_preferences = list(set(payload['preferences']))

    movie_features = get_movie_features()
    preferences = [5 if feature in user_preferences else 0 for feature in movie_features]

    recommendations = get_recommended_movies(None, preferences)


    titles = recommendations['title']
    genres = recommendations['genres']
    recommended_movies_data = []
    for title, genre in zip(titles, genres):
        recommended_movies_data.append({
            'title'  : title,
            'genres' : genre,
        })

    return jsonify({
        'error': NO_ERROR,
        'recommendations': recommended_movies_data,
        'user_preferences': user_preferences
    })

# -------------------------------------------------------------

@app.route('/get_movie_features', methods = ['post'])
def return_movie_features():
    features = get_movie_features()
    return {
        'error' : NO_ERROR,
        'features' : features
    }
    
# ------------------------------------------------------------------------------------

            

if __name__ == '__main__':
    app.run(
        debug = True,
        port = PORT
    )


