import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from pre_process import PreStage

# Create an instance of the PreStage class
preprocessor = PreStage()

# Call the prep method to perform the additional steps
preprocessor.prep()

# Access the preprocessed data and the movie_id_title dictionary via the preprocessor instance
main_df = preprocessor.preprocessed2


def clustering_evaluation(df, k_start=5, k_end=12):
    """
    Function: clustering_evaluation

    Description:
    The `clustering_evaluation` function is designed to assess the optimal number
      of clusters (K) for a dataset using two common methods: the Elbow Method and the 
      Silhouette Score. This function generates both types of plots within a single 
      figure for visual analysis.

    Parameters:
    - df (pd.DataFrame): The dataset to be analyzed for clustering. It should have 
    features/columns for clustering.
    - k_start (int): The starting value of K for the range of clusters to test (default is 5).
    - k_end (int): The ending value of K for the range of clusters to test (default is 12).

    Usage Example:
    ```python
    # Call the combined function with the dataset and range of K values
    clustering_evaluation(main_df, k_start=5, k_end=12)

    """
    def elbow_test(df, k_start, k_end):
        wcss = []
        k_values = range(k_start, k_end)

        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=10)
            kmeans.fit(df)
            wcss.append(kmeans.inertia_)

        return k_values, wcss

    def silhouette_test(df, k_start, k_end):
        k_values = range(k_start, k_end)
        silhouette_scores = []

        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=10)
            kmeans.fit(df)
            labels = kmeans.labels_
            silhouette_avg = silhouette_score(df, labels)
            silhouette_scores.append(silhouette_avg)

        return k_values, silhouette_scores

    k_values, wcss = elbow_test(df, k_start, k_end)
    k_values_silhouette, silhouette_scores = silhouette_test(
        df, k_start, k_end)

    # Plot the elbow test results
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(k_values, wcss, marker='o', linestyle='-', color='b')
    plt.title('Elbow Method for Optimal K')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
    plt.grid()

    # Plot the silhouette test results
    plt.subplot(1, 2, 2)
    plt.bar(k_values_silhouette, silhouette_scores, color='skyblue')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score for Different K Values')
    plt.xticks(k_values_silhouette)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


# Call the combined function with the dataset and range of K values
clustering_evaluation(main_df)
