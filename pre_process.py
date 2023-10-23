import pandas as pd
import os


class PreStage:
    """
    Class: PreStage

        Description:
        The PreStage class is designed to facilitate the preprocessing of movie-related data, 
        including movies and ratings. It provides methods to prepare, clean, and transform 
        data for further analysis.

        Constructor:
        - PreStage():
        Initializes the PreStage object and loads movie and rating data from CSV files.

        Methods:
        1. init_prep()
        - Description: Performs initial data preprocessing by merging movie and rating data,
        handling genres, and addressing sparsity.
        - Output: Preprocessed data is stored in the 'preprocessed1' attribute.

        2. title_dict()
        - Description: Creates a dictionary mapping movie IDs to their titles.
        - Output: The 'movie_id_title' attribute contains the movie ID-title mapping.

        3. prep()
        - Description: Completes the data preprocessing pipeline by calling 'init_prep' 
        and 'title_dict' and then applies further transformations by removing movie titles, 
        grouping by 'movieId', and filtering by ratings.
        - Output: Preprocessed data is stored in the 'preprocessed2' attribute.

        Attributes:
        - movies_data: Contains movie data loaded from the CSV file.
        - ratings_data: Contains rating data loaded from the CSV file.
        - preprocessed1: Stores the result of the initial data preprocessing.
        - preprocessed2: Stores the fully preprocessed data after calling 'prep'.
        - movie_id_title: Holds the movie ID-title mapping.

        Usage Example:
        ```python
        # Create an instance of the PreStage class
        preprocessor = PreStage()

        # Perform data preprocessing
        preprocessor.prep()

        # Access preprocessed data and the movie ID-title dictionary
        processed_data1 = preprocessor.preprocessed1
        processed_data2 = preprocessor.preprocessed2
        movie_id_title = preprocessor.movie_id_title
    """

    def __init__(self):
        # Define the file paths for movies and ratings data

        movies_data = 'ml-latest-small/movies.csv'
        ratings_data = 'ml-latest-small/ratings.csv'

        self.movies_data = pd.read_csv(movies_data)
        self.ratings_data = pd.read_csv(ratings_data)
        self.preprocessed1 = None
        self.preprocessed2 = None
        self.movie_id_title = None

    def init_prep(self):
        # load movies and rating data
        movies_data = self.movies_data
        ratings_data = self.ratings_data

        # merge both tables
        movie_db = pd.merge(movies_data, ratings_data,
                            on='movieId', how='inner')

        # Consider Genres by converting into dummies
        genre_dumies = movie_db['genres'].str.get_dummies('|')

        # Drop useless genre (No genres listed)
        genre_dumies = genre_dumies.drop('(no genres listed)', axis=1)

        # Join genre dummies with the main DataFrame and drop genre column
        movie_db_new = pd.concat([movie_db, genre_dumies], axis=1).drop(
            ['genres', 'timestamp'], axis=1)

        # Count occurrences of ratings using movieId
        ratings_count = movie_db_new['movieId'].value_counts()
        # Index movies appearing more than 10 times
        valid_movie_ids = ratings_count[ratings_count >= 10].index
        # Filter the DataFrame to exclude movie IDs that appear less than 10 times
        movie_db_new = movie_db_new[movie_db_new['movieId'].isin(
            valid_movie_ids)]

        # Convert userId into dummy variables
        movie_dbs = pd.get_dummies(movie_db_new, columns=[
                                   'userId'], prefix='User')

        # A function to reduce sparsity
        def drop_high_zero_columns(df, threshold=99.7):
            # Calculate the percentage of zeros in each column
            zero_percentage = (df == 0).mean() * 100

            # Check for columns with over the specified threshold of zeros
            columns_to_drop = zero_percentage[zero_percentage >
                                              threshold].index

            # Drop the identified columns
            df = df.drop(columns=columns_to_drop)

            return df

        # Call the function to drop high-zero columns
        df1 = drop_high_zero_columns(movie_dbs, threshold=99.7)

        self.preprocessed1 = df1  # Store the preprocessed data in an instance variable

    def title_dict(self):
        movie_id_title = dict(
            zip(self.preprocessed1['movieId'], self.preprocessed1['title']))
        # Store the movie_id_title dictionary in an instance variable
        self.movie_id_title = movie_id_title

    def prep(self):
        # Call init_prep to run the initial preprocessing
        self.init_prep()
        # Call title_dict to create the movie_id_title dictionary
        self.title_dict()

        # we drop the movie title.
        df2 = self.preprocessed1.drop(columns='title')
        # Group the DataFrame by 'movieId' and calculate the mean for each group
        df2 = df2.groupby('movieId').mean().reset_index()
        # Drop movies with ratings less than 3.0/5.0: Not suitable for recommendation
        df2 = df2[df2['rating'] > 3]

        self.preprocessed2 = df2


# Create an instance of the PreStage class
preprocessor = PreStage()

# Call the prep method to perform the additional steps
preprocessor.prep()

# Access the preprocessed data and the movie_id_title dictionary via the preprocessor instance
main_df = preprocessor.preprocessed2
movie_id_title = preprocessor.movie_id_title

# Print the preprocessed data and the movie_id_title dictionary
# print("\nProcessed Data 2:")
# print(main_df)
