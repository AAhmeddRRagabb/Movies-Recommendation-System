# Movies Recommendation System

## Overview
This project was developed to practice building a recommendation system using a Neural Network (NN) model implemented in `Keras`. It applies a content-based filtering approach on movie data. The dataset includes user preferences (favorite genres), movie genre details, and user ratings. The model predicts a user’s rating for each movie and recommends the top 10 movies with the highest predicted ratings.

## Project Workflow
This project mainly passed through four stages
1. Data Exploration with `Pandas & NumPy`: Conducted a comprehensive analysis to understand the dataset, identify dependencies between tables, clean and standardize the data, and extract relevant features for model building.
2. Model Building: Used `scikit-learn` and `Keras` to preprocess the data, build the neural network model, and evaluate its performance.
3. Recommendations: Applied the trained model to generate movie recommendations based on user preferences, tested on both new and existing users.
4. Model Deployment: Served the model in a `Flask` environment with a simple user interface built using `CSS` and `JavaScript`.

## Project Structure
The project contains:
- A Jupyter notebook for data exploration, model training, and experimentation, along with a utility script.
- A Flask-based server application for deployment, including templates, static assets (CSS/JS), and inference utilities.
- The datasets used for training and evaluation.
- Saved trained objects (the model and scalers).

## Data Source
The dataset used in this project is originally from the [MovieLens dataset](https://grouplens.org/datasets/movielens/latest/) but was accessed through the course materials provided in [ML Specialization](https://www.coursera.org/specializations/machine-learning-introduction).

---
***ALHAMDULILLAH***
---
