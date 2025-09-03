# ---------------------------------------------------------------------------------------------
# This file is to provide helpful functions for the recommendation notebook
# الله المستعان
# ----------------------------------------------------------------------------------------------


# Imports & global values

import numpy as np
import pandas as pd
import csv
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from tensorflow import keras
import joblib

from pathlib import Path


DATA_BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = f'{DATA_BASE_DIR.parent.parent}/data/'

OBJ_BASE_DIR = Path(__file__).resolve().parent
FITTED_OBJ_PATH = f'{OBJ_BASE_DIR.parent.parent}/fitted_objects'


# ----------------------------------------------------------------------------------------------

#### Inference Logic #####
def recommend_for_new_user(user_preferences):
    model = load_object('recommender_dnn_model', is_tf_obj = True)
    scalers = load_object('fitted_scalers')

    target_user_df = pd.DataFrame([user_preferences])
    target_user_vector = target_user_df.values

    # get & clean movies features
    movies_data = load_data("movies", "movies_header")
    movies_data.columns = clean_col_names(movies_data)
    
    unique_movies_matrix = movies_data.drop_duplicates().drop(columns = ['movie_id']).values
    unique_movies_IDs = movies_data.drop_duplicates()['movie_id']


    # processing
    target_user_vector_repeated = np.repeat(target_user_vector, unique_movies_matrix.shape[0], axis = 0) # map the user to each unique movie
    target_user_vector_repeated_scaled = scalers['users_scaler'].transform(target_user_vector_repeated)  # scaling user_vector
    unique_movies_matrix_scaled = scalers['movies_scaler'].transform(unique_movies_matrix)               # scaling movies_matrix

    # predicting
    yhat = model.predict(x = (
        target_user_vector_repeated_scaled,
        unique_movies_matrix_scaled
    ))
    predicted_ratings = scalers['ratings_scaler'].inverse_transform(yhat)


    # make a df for the top 10 recommended movies
    prediction_df = (
        pd.DataFrame(
            {
                'movie_id' : unique_movies_IDs,
                'predicted_rating' : predicted_ratings.reshape(-1,)
            }
        ).sort_values(by = ['predicted_rating'], ascending = False).head(10)
    )

    return prediction_df['movie_id']



    
# ----------------------------------------------------------------------------------------------


def recommed_for_existing_user(target_user_id):
    """
    This function returns the IDs for the top 10 recommended movies for the given user

    Args:
        user_id: The user id
        model  : The trained model that will recommend
        scalers: a dict contains the users, movies, and ratings scalers

    Returns:
        prediction_df: a pandas dataframe contains the top 10 recommendations
    """

    model = load_object('recommender_dnn_model', is_tf_obj = True)
    scalers = load_object('fitted_scalers')

    # get & clean users_data
    users_data = load_data("users", "users_header")
    users_data.columns = clean_col_names(users_data)
    users_data['user_id'] = users_data['user_id'].astype(int)

    
    # check if the user exists in users_data
    if target_user_id in set(users_data['user_id']):
        target_user_vector = (
            users_data[users_data['user_id'] == target_user_id]
            .drop_duplicates()
            .drop(columns = ['user_id', 'rating_count', 'rating_ave'])
        ).values
        
    else:
        raise ValueError("ID NOT FOUND")
        

    # get & clean movies features
    movies_data = load_data("movies", "movies_header")
    movies_data.columns = clean_col_names(movies_data)
    
    unique_movies_matrix = movies_data.drop_duplicates().drop(columns = ['movie_id']).values
    unique_movies_IDs = movies_data.drop_duplicates()['movie_id']


    # processing
    target_user_vector_repeated = np.repeat(target_user_vector, unique_movies_matrix.shape[0], axis = 0) # map the user to each unique movie
    target_user_vector_repeated_scaled = scalers['users_scaler'].transform(target_user_vector_repeated)  # scaling user_vector
    unique_movies_matrix_scaled = scalers['movies_scaler'].transform(unique_movies_matrix)               # scaling movies_matrix

    # predicting
    yhat = model.predict(x = (
        target_user_vector_repeated_scaled,
        unique_movies_matrix_scaled
    ))
    predicted_ratings = scalers['ratings_scaler'].inverse_transform(yhat)


    # make a df for the top 10 recommended movies
    prediction_df = (
        pd.DataFrame(
            {
                'movie_id' : unique_movies_IDs,
                'predicted_rating' : predicted_ratings.reshape(-1,)
            }
        ).sort_values(by = ['predicted_rating'], ascending = False).head(10)
    )

        

    return prediction_df['movie_id']

# ----------------------------------------------------------------------------------------------
    
def get_recommended_movies(target_user_id = None, user_preferences = None):
    """
    This function returns the recommended movies for a given user

    Args:
        target_user_id: The user id for an existing user
        user_prefernces: A dict contains the user preferences for a new user

    Returns:
        recommended_movies: The top 10 matched movies
    """

    
    movies_info = load_data('info_movies')
    movies_info.columns = clean_col_names(movies_info)
    
    if target_user_id:
        recommeded_movies_ids = recommed_for_existing_user(target_user_id)
    
    else:
        recommeded_movies_ids = recommend_for_new_user(user_preferences)

    recommended_movies = movies_info[movies_info['movieid'].isin(recommeded_movies_ids)]
    return recommended_movies





# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
######## Helper Functions #########


def load_data(data: str, cols: str = None, np_arr = False):
    """
    This function loads the provided data and returns a pandas dataframe or a numpy array

    Args:
        data: The data filename
        header: the name of the header
        np_arr: A bool value. True for returning a numpy array
    """
    data_file = f'{DATA_PATH}{data}'

    if not cols:
        if np_arr:
            output = np.loadtxt(f'{data_file}.csv', delimiter = ',')
        else:
            output = pd.read_csv(f'{data_file}.csv')
        return output
        
    with open(f'{DATA_PATH}{cols}.txt') as f:
        col_names = list(csv.reader(f))[0]
    return pd.read_csv(f'{data_file}.csv', names = col_names)

# ----------------------------------------------------------------------------------------------

def clean_col_names(data):
    """
    This function standardize the col names in the input data frame
    """
    columns = data.columns.map(
        lambda col: "_".join(word.lower() for word in col.split())
    )
    return columns

# ----------------------------------------------------------------------------------------------

def get_user_preferences(target_user_id):
    users_data = load_data('users', cols = 'users_header')
    users_data.columns = clean_col_names(users_data)
    the_user_data = (
        users_data[users_data['user_id'] == target_user_id]
        .drop_duplicates()
        .drop(columns = ['user_id', 'rating_count', 'rating_ave'])
    )

    user_preferences = [col for col in the_user_data.columns if float(the_user_data[col].values) > 0]
    return user_preferences


# ----------------------------------------------------------------------------------------------

def get_movie_features():
    movies_features = load_data('movies', cols = 'movies_header')
    movies_features.columns = clean_col_names(movies_features)
    return movies_features.drop(columns = ['movie_id', 'year', 'ave_rating']).columns.to_list()

# ----------------------------------------------------------------------------------------------

def load_object(name_to_load, is_tf_obj = False):
    """
    This function loads the required object from the FITTED_OBJ_PATH
    
    Args:
        name_to_load: the name of the saved object
        is_tf_obj: whether or not the object represents a tensorflow object

    Returns:
        obj: the loaded object
    """

    name = name_to_load.lower()

    if is_tf_obj:
        obj_path = f'{FITTED_OBJ_PATH}/{name}.keras'
        obj = keras.models.load_model(obj_path)

    else:
        obj_path = f'{FITTED_OBJ_PATH}/{name}.pkl'
        obj = joblib.load(obj_path)

    return obj
        
    

# ----------------------------------------------------------------------------------------------

def check_user(user_id):
    """
    This function checks if the given user is new or not

    Returns:
        new: bool indicates if a user is new or not
    """

    # get & clean users_data
    users_data = load_data("users", "users_header")
    users_data.columns = clean_col_names(users_data)
    users_data['user_id'] = users_data['user_id'].astype(int)

    
    if user_id in set(users_data['user_id']):
        new = False
    
    else:
        new = True
    
    return new


# ----------------------------------------------------------------------------------------------





