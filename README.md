# Recommender System

This is a content based recommendation system implementation using k-means clustering algorithm

## The Dataset

This dataset (ml-latest-small) describes 5-star rating and free-text tagging activity from [MovieLens](http://movielens.org), a movie recommendation service. It contains 100836 ratings and 3683 tag applications across 9742 movies. These data were created by 610 users between March 29, 1996 and September 24, 2018. This dataset was generated on September 26, 2018.

Users were selected at random for inclusion. All selected users had rated at least 20 movies. No demographic information is included. Each user is represented by an id, and no other information is provided.

The data are contained in the files `links.csv`, `movies.csv`, `ratings.csv` and `tags.csv`. More details about the contents and use of all these files follows.

This is a _development_ dataset. As such, it may change over time and is not an appropriate dataset for shared research results. See available _benchmark_ datasets if that is your intent.

This and other GroupLens data sets are publicly available for download at <http://grouplens.org/datasets/>.

## Software, Tools and Libraries Required

1. [VS Code IDE](https://code.visualstudio.com/)
2. [Python 3.12.0](https://www.python.org/downloads/)
3. Libraries: `requests`, `zipfile`, `pandas`, `matplotlib`, `sklearn`, `Flask`

## Procedure

- **Data Ingestion:** Using the `requests` and `zipfile` library, we are able to download a zip format of the dataset, extract, and save into desired directory. `import_data.py` file contains the code to achieving that.

- **Data Preprocessing:** We used `pandas` library for data preprocessing. The whole pipeline provides methods to prepare, clean, and transform data for further analysis. That is contained in `pre_process.py` file.

- **Parameter Tuning:** Our choice of algorithm is K-Means Clustering. We need to choose an optimal K (Number of clusters) for the algorithm. We use WCSS score and Silhouette Statistics as our metric. We provided a visual for evaluation using `matplotlib`. This process is contained in `k_evaluation.py` file.

- **Clustering:** Using the `KMeans` function in the `Sklearn.Cluster` module we are able to create clusters of recommendations by similar movie traits and user interraction. The file `clustering.py` contains the algorithm.

- **Model Deployment:** We created a post method using flask and call on the function `recommender` which gives us movie recommendations based on the k-means clustering algorithm. We use `postman` vs code extension to test the endpoint.
