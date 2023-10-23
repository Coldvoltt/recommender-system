from sklearn.cluster import KMeans
from pre_process import PreStage


from sklearn.cluster import KMeans
from pre_process import PreStage


def recommender(movie_title, n=10, k=8):
    # Create an instance of the PreStage class
    preprocessor = PreStage()

    # Call the prep method to perform the additional steps
    preprocessor.prep()

    # Access the preprocessed data and the dict dictionary via the preprocessor instance
    df = preprocessor.preprocessed2
    movie_id_title = preprocessor.movie_id_title

    # Choose the number of clusters (K)
    K = k
    # Carry out k means
    kmeans = KMeans(n_clusters=K, n_init=10)
    labels = kmeans.fit_predict(df)

    # Add cluster labels to the DataFrame
    df['cluster'] = labels

    # mapping movie title from the saved dictionary with the cluster df
    df['title'] = df['movieId'].map(movie_id_title)

    # Filter for movie title, cluster and rating
    titles_clusters = df[['title', 'cluster', 'rating']]

    # Convert movie titles to lowercase for case-insensitive matching
    movie_title = movie_title.lower()

    closest_title = None

    # Create an empty list to store matching titles
    matching_titles = []

    # Iterate through the DataFrame to find partial string matches
    for title in df['title']:
        if movie_title in title.lower():
            matching_titles.append(title)

    if not matching_titles:
        return print("No matching movie title found in the database.")

    # Select the closest matching title based on partial string match
    title = matching_titles[0]

    # Find the cluster of the closest matching movie title
    cluster = df[df['title'] == title]['cluster'].values[0]

    # Filter the DataFrame to include only movies from the same cluster
    cluster_movies = df[df['cluster'] == cluster]

    # Exclude the closest match from the recommendations
    cluster_movies = cluster_movies[cluster_movies['title'].str.lower(
    ) != title.lower()]

    # Sort the remaining movies by rating in descending order and get the top n
    top_movies = cluster_movies.sort_values(
        by='rating', ascending=False).head(n)

    # Get the titles of the top movies
    top_movie_titles = top_movies['title'].to_string(index=False)

    result = f"Movie title closest match is: {title}.\n\nTop {
        n} recommendations are: \n\n{top_movie_titles}"

    return print(result)


recommender("ultron")
