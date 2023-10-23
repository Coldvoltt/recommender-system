from sklearn.cluster import KMeans
from pre_process import PreStage

# Create an instance of the PreStage class
preprocessor = PreStage()

# Call the prep method to perform the additional steps
preprocessor.prep()

# Access the preprocessed data and the dict dictionary via the preprocessor instance
df = preprocessor.preprocessed2
movie_id_title = preprocessor.movie_id_title

# Carry out k means
kmeans = KMeans(n_clusters=12, n_init=10)
labels = kmeans.fit_predict(df)

# Add cluster labels to the DataFrame
df['cluster'] = labels

# mapping movie title from the saved dictionary with the cluster df
df['title'] = df['movieId'].map(movie_id_title)

# Filter for movie title, cluster and rating
cluster_df = df[['title', 'cluster', 'rating']]

# Save data
f_path = 'df.csv'
cluster_df.to_csv(f_path, index=False)

# import pandas as pd
# def recommender(movie_title):

#     cluster_df = pd.read_csv(df.csv)

#     # Convert movie titles to lowercase for case-insensitive matching
#     movie_title = movie_title.lower()

#     closest_title = None

#     # Create an empty list to store matching titles
#     matching_titles = []

#     # Iterate through the DataFrame to find partial string matches
#     for title in cluster_df['title']:
#         if movie_title in title.lower():
#             matching_titles.append(title)

#     if not matching_titles:
#         return print("No matching movie title found in the database.")

#     # Select the closest matching title based on partial string match
#     title = matching_titles[0]

#     # Find the cluster of the closest matching movie title
#     cluster = cluster_df[cluster_df['title']
#                               == title]['cluster'].values[0]

#     # Filter the DataFrame to include only movies from the same cluster
#     cluster_movies = cluster_df[cluster_df['cluster'] == cluster]

#     # Exclude the closest match from the recommendations
#     cluster_movies = cluster_movies[cluster_movies['title'].str.lower(
#     ) != title.lower()]

#     # Sort the remaining movies by rating in descending order and get the top n
#     top_movies = cluster_movies.sort_values(
#         by='rating', ascending=False).head(10)

#     # Get the titles of the top movies
#     top_movie_titles = top_movies['title'].to_string(index=False)

#     result = f"Movie title closest match is: {
#         title}.\n\nTop 10 recommendations are: \n\n{top_movie_titles}"

#     return print(result)


# recommender("ultron")
