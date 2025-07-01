# Movie Recommender System (Content-Based)

This project is a **Content-Based Movie Recommender System** developed using **Python** and basic **Machine Learning** techniques. It analyzes movie metadata to suggest similar movies based on textual similarity. When a user searches for a movie title, the system uses **TF-IDF vectorization** to find and recommend the **top 5 most similar movies** from the dataset. 

## Features

- Provides personalized, content-based movie recommendations by analyzing metadata such as genres, keywords, and movie overviews.
- Uses **TF-IDF (Term Frequency-Inverse Document Frequency)** vectorization to convert movie descriptions and metadata into numerical representations for similarity calculation.
- Allows users to search for any movie title within the dataset and instantly get relevant suggestions.
- Displays the top 5 movies most similar to the searched title, helping users discover new films they may enjoy.
- Runs locally in a **Python** environment and was developed using **PyCharm** for a smooth development experience.

---

##  Dataset

This recommender system uses the **TMDB 5000 Movies Dataset**, which provides extensive metadata for thousands of movies. The dataset includes the following files:

- `tmdb_5000_movies.csv` — Contains detailed information about each movie, including title, genres, keywords, and overview.
- `tmdb_5000_credits.csv` — Includes data about the cast and crew for each movie, which can be used to enhance recommendation quality.

---

##  Technologies Used

- **Python 3.x:** Main programming language for building the recommender system.
- **Pandas:** For loading, cleaning, and manipulating large datasets.
- **Scikit-learn:** Used for TF-IDF vectorization, similarity measurement, and other essential machine learning tasks.
- **NumPy:** Provides numerical operations and efficient handling of arrays and matrices.
- **PyCharm:** Integrated Development Environment (IDE) used for writing, testing, and debugging the code.

---
## Visit the Website : 

### 1. Clone the Repository
```bash
git clone https://github.com/seyjall/Movie-recommender.git
cd Movie-recommender
