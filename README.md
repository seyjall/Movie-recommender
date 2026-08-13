Hybrid Movie Recommender System

A hybrid movie recommendation system combining content-based filtering and item-item collaborative filtering to generate personalized top-5 movie recommendations.

Project Description

The system combines movie-content similarity from the TMDB 5000 dataset with user-rating patterns from MovieLens. Content-based recommendations use Bag-of-Words and cosine similarity, while collaborative filtering compares movies based on user rating patterns. The two signals are combined using a hybrid ranking approach.

Features

Content-based recommendation using movie metadata

Bag-of-Words feature extraction with CountVectorizer

Text preprocessing and stemming using NLTK

Cosine similarity for movie-to-movie similarity

Item-item collaborative filtering using MovieLens ratings

Hybrid ranking with equal weighting of both models

Top-5 recommendations with movie posters

Interactive Streamlit web application

Datasets

TMDB 5000 Movies Dataset

Used for the content-based component.

Approximately 4.8K movies

Movie metadata such as title, genres, cast and crew

TMDB movie IDs are used in the final recommendation pipeline

MovieLens Dataset

Used for collaborative filtering.

User-movie ratings

Fields: userId, movieId, rating, timestamp

894 movies were matched between MovieLens and TMDB

8 matched movies had no MovieLens ratings

Therefore, 886 movies were used for collaborative filtering

Recommendation Pipeline

TMDB Movie Metadata
        |
        v
Text Preprocessing + Stemming
        |
        v
Bag-of-Words (CountVectorizer)
        |
        v
Content Similarity
        |
        +----------------------+
                               |
MovieLens Ratings              |
        |                      |
        v                      |
User-Movie Matrix              |
        |                      |
        v                      |
Movie-Movie Similarity         |
        |                      |
        +----------+-----------+
                   |
                   v
          Hybrid Candidate Set
                   |
                   v
       Rank-based Hybrid Scoring
                   |
                   v
              Top-5 Movies

Content-Based Filtering

Movie metadata is combined into text features and preprocessed using NLP techniques.

Stemming

NLTK stemming reduces related words to a common stem before vectorization.

Example:

playing -> play
played  -> play

Bag-of-Words

CountVectorizer converts processed movie text into numerical feature vectors.

CountVectorizer(
    max_features=5000,
    stop_words="english"
)

It builds a vocabulary from the movie corpus and represents each movie using word-frequency features.

Cosine Similarity

Cosine similarity is calculated between movie vectors to identify movies with similar content.

The similarity matrix follows the same movie ordering as the processed movie dataset, allowing its indices to be mapped back to TMDB movie IDs.

Collaborative Filtering

The collaborative component uses MovieLens user ratings.

User-Movie Matrix

matched_matrix = ratings_matched.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
)

This creates:

Rows    -> Users
Columns -> Movies
Values  -> Ratings

Item-Item Similarity

The matrix is transposed so each movie is represented by its ratings across users.

movie_similarity_matched = cosine_similarity(
    matched_matrix.T.fillna(0)
)

This produces an 886 × 886 movie-to-movie similarity matrix.

Movies with similar user-rating patterns receive higher similarity scores.

Hybrid Recommendation

The two models use different movie ID systems:

Content-based     -> TMDB movie IDs
Collaborative     -> MovieLens movie IDs

MovieLens IDs are mapped to TMDB IDs so both recommendation sources can be combined.

The top 50 candidates from each model are merged into one candidate set.

Hybrid Ranking

Each candidate receives a rank from both models. Reciprocal rank scoring is used:

1 / (rank + 1)

The models are given equal weight:

Hybrid Score =
    0.5 × Content Rank Score
    +
    0.5 × Collaborative Rank Score

Movies ranked highly by both models receive higher hybrid scores.

Streamlit Application

The Streamlit app allows users to:

Select a movie from a dropdown.

Click Recommend.

Receive the top-5 hybrid recommendations.

View movie titles and posters.

Run the application with:

streamlit run app.py



Tools & Technologies

Python

Pandas - data processing

NumPy - numerical operations

Scikit-learn - CountVectorizer, cosine similarity, MinMaxScaler

NLTK - stemming and NLP preprocessing

Pickle - serialization of precomputed Python objects

Streamlit - interactive ML web application

TMDB 5000 Movies Dataset - movie metadata

MovieLens Dataset - user ratings

Key Concepts

Natural Language Processing

Feature extraction using Bag-of-Words

Text preprocessing and stemming

Cosine similarity

Item-item collaborative filtering

User-movie rating matrices

Dataset matching and ID mapping

Hybrid recommendation

Rank-based scoring

Model/data serialization with Pickle

Interactive ML application development

Output

For a selected movie, the system returns the top-5 hybrid recommendations based on both movie-content similarity and user-rating similarity.

Future Improvements

Tune content/collaborative weights

Add genre, year and preference filters

Cache poster requests to reduce repeated API calls
