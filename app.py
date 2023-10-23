from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load your cluster data when the app starts
cluster_df = pd.read_csv('df.csv')


@app.route('/recommender', methods=['POST'])
def recommender():

    # Get the JSON data from the request body
    data = request.get_json()

    if 'movie_title' not in data:
        return jsonify({"error": "Movie title parameter is missing."})

    # Extract the movie title from the JSON data
    movie_title = data['movie_title']

    # Convert movie titles to lowercase for case-insensitive matching
    movie_title = movie_title.lower()

    closest_title = None

    # Create an empty list to store matching titles
    matching_titles = []

    # Iterate through the DataFrame to find partial string matches
    for title in cluster_df['title']:
        if movie_title in title.lower():
            matching_titles.append(title)

    if not matching_titles:
        return jsonify({"message": "No matching movie title found in the database."})

    # Select the closest matching title based on partial string match
    title = matching_titles[0]

    # Find the cluster of the closest matching movie title
    cluster = cluster_df[cluster_df['title'] == title]['cluster'].values[0]

    # Filter the DataFrame to include only movies from the same cluster
    cluster_movies = cluster_df[cluster_df['cluster'] == cluster]

    # Exclude the closest match from the recommendations
    cluster_movies = cluster_movies[cluster_movies['title'].str.lower(
    ) != title.lower()]

    # Sort the remaining movies by rating in descending order and get the top n
    top_movies = cluster_movies.sort_values(
        by='rating', ascending=False).head(10)

    # Get the titles of the top movies
    top_movie_titles = top_movies['title'].to_string(index=False)

    result = top_movie_titles.split('\n')
    message = f"from search resut '{matching_titles}': "

    # Create a dictionary with a message and the result
    response_data = {
        "Best Match": message,
        "recommendations": result
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)


# response = request.get("http://localhost:5000/recommender")
# data = response.json()
# print(data)
