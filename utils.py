# ---------------------------------------------------------------------------------------------
# This file is to provide helpful functions for the recommendation notebook
# الله المستعان
# ----------------------------------------------------------------------------------------------


# Imports & global values

import numpy as np
import pandas as pd
import csv
from tensorflow import keras
import joblib


DATA_PATH = './data/'
FITTED_OBJ_PATH = './fitted_objects'

# ----------------------------------------------------------------------------------------------


def load_data(data: str, cols: str = None, np_arr = False):
    """
    This function loads the provided data and returns a pandas dataframe or a numpy array

    Args:
        data: The data filename
        header: the name of the header
        np_arr: A bool value. True for returning a numpy array
    """
    data_file = f'{DATA_PATH}{data}'
    # print(data_file)
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


def recommend_movies(target_user_id, model, user_preferences: dict = None, **scalers):
    """
    This function returns the IDs for the top 10 recommended movies for the given user

    Args:
        user_id: The user id
        model  : The trained model that will recommend
        scalers: a dict contains the users, movies, and ratings scalers
        user_preferences: describe user preferences for a new user

    Returns:
        prediction_df: a pandas dataframe contains the top 10 recommendations
    """

    # get & clean users_data
    users_data = load_data("users", "users_header")
    users_data.columns = clean_col_names(users_data)
    users_data['user_id'] = users_data['user_id'].astype(int)

    
    # check if the user exist in users_data or a new user
    if target_user_id in set(users_data['user_id']):
        target_user_vector = (users_data[users_data['user_id'] == target_user_id].drop_duplicates().drop(columns = ['user_id', 'rating_count', 'rating_ave'])).values
        
    else:
        
        if not user_preferences:
            raise ValueError("New user with no preferences")
            
        # Invalid preferences
        required_preferences = set(users_data.drop(columns = ['user_id', 'rating_count', 'rating_ave']).columns)
        if not set(user_preferences) - required_preferences:
            raise ValueError("Invalid preferences")

        target_user_df = pd.DataFrame([user_preferences])
        target_user_vector = target_user_df.drop(columns = ['user_id', 'rating_count', 'rating_ave']).values

        
        
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
                'user_id' : target_user_id,
                'movie_id' : unique_movies_IDs,
                'predicted_rating' : predicted_ratings.reshape(-1,)
            }
        ).sort_values(by = ['predicted_rating'], ascending = False)
    )
        

    return prediction_df
    
    
# ----------------------------------------------------------------------------------------------

def save_object(to_save_name, obj, is_tf_obj = False):
    """
    This function saves the given obj to the FITTED_OBJ_PATH

    Args:
        to_save_name: the name required when saving the obj
        obj: the object to save
        is_tf_obj: whether or not the object represents a tensorflow object
    """

    # standardize name cases
    name = to_save_name.lower()
    
    if is_tf_obj:
        save_path = f'{FITTED_OBJ_PATH}/{name}.keras'
        obj.save(save_path)

    else:
        save_path = f'{FITTED_OBJ_PATH}/{name}.pkl'
        joblib.dump(obj, save_path) 


# ----------------------------------------------------------------------------------------------

        
    








