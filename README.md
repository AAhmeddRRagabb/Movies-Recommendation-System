# Movies Recommendation System

## Overview
This project is designed to practice building a recommendation system using a Neural Network (NN) model implemented in `Keras`. The system applies content-based filtering on movie datasets. The dataset used in this project is originally from the [MovieLens dataset](https://grouplens.org/datasets/movielens/latest/) but was accessed through the course materials provided in [ML Specialization](https://www.coursera.org/specializations/machine-learning-introduction).

## Overflow
This project mainly passed through four stages
1. Exploring the data using `Pandas & NumPy`: In this phase, a comprehensive exploration of the data was conducted in order to understand the data, dependecies between different tables,
   clean the data & standardize the data format, and finally extract the relavent features to the model building process.
2. The model building process: Using `sk-learn` and `keras` to prepare the data for modeling, build the model, then evaluate the model performance.
3. Recommending: Use the trained model to get recommendations based on users's preferences. The result was observed on both new & existing users.
4. Serving the model: Use the `flask` enviroment to sever the model with a sumple UI with `CSS & JS`

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
