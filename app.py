import streamlit as st
import pickle
import pandas as pd
import requests
import os


# --------------------------------------------------
# Download similarity matrix if not present
# --------------------------------------------------

def download_similarity():
    if not os.path.exists("similarity.pkl"):
        print("Downloading similarity.pkl...")

        url = "https://drive.google.com/uc?export=download&id=1bZdkWLdSptJDANlNw9Z9unb_5_Eum0OZ"

        response = requests.get(url)

        with open("similarity.pkl", "wb") as f:
            f.write(response.content)

        print("Download complete.")


download_similarity()


# --------------------------------------------------
# Load content-based model
# --------------------------------------------------

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)


# --------------------------------------------------
# Load collaborative filtering model
# --------------------------------------------------

with open("collaborative_model.pkl", "rb") as f:
    collaborative_model = pickle.load(f)


movie_similarity_matched = collaborative_model["movie_similarity"]

matched_movie_id_to_index = collaborative_model[
    "movie_id_to_index"
]

matched_movie_ids = collaborative_model[
    "matched_matrix_columns"
]

ml_to_tmdb = collaborative_model["ml_to_tmdb"]

tmdb_to_ml = collaborative_model["tmdb_to_ml"]


# --------------------------------------------------
# Load movie data
# --------------------------------------------------

movies_dict = pickle.load(
    open("movie_dict.pkl", "rb")
)

movies = pd.DataFrame(movies_dict)


# --------------------------------------------------
# TMDB ID → content similarity index
# --------------------------------------------------

tmdb_ids_ordered = list(
    movies_dict["movie_id"].values()
)

tmdb_id_to_content_index = {
    movie_id: index
    for index, movie_id in enumerate(tmdb_ids_ordered)
}


# --------------------------------------------------
# Fetch movie poster
# --------------------------------------------------

def fetch_poster(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}/images"
        f"?api_key=fc1bb5b46712b8f459d907ab2083d2be"
    )

    try:

        res = requests.get(url)

        data = res.json()

        if data.get("posters"):

            poster_path = data["posters"][0]["file_path"]

            image_url = (
                f"https://image.tmdb.org/t/p/w500"
                f"{poster_path}"
            )

            return image_url

        return None

    except requests.exceptions.RequestException as e:

        print("Error:", e)

        return None


# --------------------------------------------------
# Hybrid Recommendation
# --------------------------------------------------

def recommend(movie):

    # ----------------------------------------------
    # Get TMDB movie ID
    # ----------------------------------------------

    movie_row = movies[
        movies["title"] == movie
    ].iloc[0]

    movie_id = movie_row["movie_id"]


    # ----------------------------------------------
    # Content-based recommendations
    # ----------------------------------------------

    content_idx = tmdb_id_to_content_index[movie_id]

    content_scores = similarity[content_idx]

    content_indices = (
        content_scores
        .argsort()[::-1][1:51]
    )

    content_candidates = {
        tmdb_ids_ordered[i]: content_scores[i]
        for i in content_indices
    }


    # ----------------------------------------------
    # Collaborative filtering
    # ----------------------------------------------

    ml_id = tmdb_to_ml.get(movie_id)


    # If movie is not present in MovieLens,
    # fall back to content-based recommendations

    if (
        ml_id is None
        or ml_id not in matched_movie_id_to_index
    ):

        recommended_ids = list(
            content_candidates.keys()
        )[:5]


    else:

        collab_idx = matched_movie_id_to_index[ml_id]

        collab_scores = (
            movie_similarity_matched[collab_idx]
        )

        collab_indices = (
            collab_scores
            .argsort()[::-1][1:51]
        )

        collab_candidates = {
            ml_to_tmdb[matched_movie_ids[i]]:
            collab_scores[i]

            for i in collab_indices

            if matched_movie_ids[i] in ml_to_tmdb
        }


        # ------------------------------------------
        # Hybrid candidate pool
        # ------------------------------------------

        candidate_ids = (
            set(content_candidates)
            | set(collab_candidates)
        )


        # ------------------------------------------
        # Content ranking
        # ------------------------------------------

        content_rank = {
            movie_id: rank

            for rank, movie_id in enumerate(
                sorted(
                    content_candidates,
                    key=content_candidates.get,
                    reverse=True
                )
            )
        }


        # ------------------------------------------
        # Collaborative ranking
        # ------------------------------------------

        collab_rank = {
            movie_id: rank

            for rank, movie_id in enumerate(
                sorted(
                    collab_candidates,
                    key=collab_candidates.get,
                    reverse=True
                )
            )
        }


        # ------------------------------------------
        # Hybrid score
        # ------------------------------------------

        hybrid_scores = {}

        for candidate in candidate_ids:

            c_rank = content_rank.get(
                candidate,
                100
            )

            cf_rank = collab_rank.get(
                candidate,
                100
            )

            hybrid_scores[candidate] = (
                0.5 / (c_rank + 1)
                +
                0.5 / (cf_rank + 1)
            )


        # ------------------------------------------
        # Top 5 recommendations
        # ------------------------------------------

        recommended_ids = [
            movie_id

            for movie_id, score in sorted(
                hybrid_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        ]


    # ----------------------------------------------
    # Movie names and posters
    # ----------------------------------------------

    recommended_movies = []

    recommended_movies_posters = []


    for movie_id in recommended_ids:

        row = movies[
            movies["movie_id"] == movie_id
        ]


        if not row.empty:

            title = row.iloc[0]["title"]

            recommended_movies.append(title)

            recommended_movies_posters.append(
                fetch_poster(movie_id)
            )


    return (
        recommended_movies,
        recommended_movies_posters
    )


# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------

st.title(
    "Movie Recommender System"
)


selected_movie = st.selectbox(
    "Search Your Favourite Movie",
    movies["title"].values
)


if st.button("Recommend"):

    names, posters = recommend(
        selected_movie
    )


    cols = st.columns(5)


    for i in range(5):

        if names[i] and posters[i]:

            with cols[i]:

                st.text(names[i])

                st.image(posters[i])


        elif names[i]:

            with cols[i]:

                st.text(names[i])

                st.write(
                    "No image available"
                )


        else:

            with cols[i]:

                st.write(
                    "No data available"
                )