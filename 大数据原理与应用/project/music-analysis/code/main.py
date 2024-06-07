from pyspark.sql import SparkSession
import json

def write_json(data, file_path):
    """Helper function to write data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f)

def genre_analysis(spark, df):
    """Perform various genre analyses and save the results to JSON files."""
    # Count of albums per genre that are greater than 2000
    genre_count = df.groupBy('genre').count()
    popular_genres = genre_count.filter('count > 2000').limit(10).collect()
    write_json([row.asDict() for row in popular_genres], 'static/data/genre.json')

    # Total sales per genre
    genre_sales = df.groupBy('genre').sum('num_of_sales').collect()
    write_json([row.asDict() for row in genre_sales], 'static/data/genre-sales.json')

    # Annual number of tracks and albums published
    year_data = df.groupBy('year_of_pub').agg({'num_of_tracks': 'sum', 'year_of_pub': 'count'}).orderBy('year_of_pub')
    year_result = year_data.collect()
    write_json([row.asDict() for row in year_result], 'static/data/year-tracks-and-sales.json')

    # Top 5 genres by album count
    top_genres = genre_count.orderBy('count', ascending=False).limit(5)
    top_genre_list = [row['genre'] for row in top_genres.collect()]

    # Sales per year for the top 5 genres
    genre_year_sales = df.filter(df['genre'].isin(top_genre_list)).groupBy('genre', 'year_of_pub').sum('num_of_sales').orderBy('genre', 'year_of_pub')
    genre_year_sales_result = genre_year_sales.collect()
    write_json([row.asDict() for row in genre_year_sales_result], 'static/data/genre-year-sales.json')

    # Average critic scores for the top genres
    genre_critic_scores = df.filter(df['genre'].isin(top_genre_list)).groupBy('genre').avg('rolling_stone_critic', 'mtv_critic', 'music_maniac_critic')
    genre_critic_scores_result = genre_critic_scores.collect()
    write_json([row.asDict() for row in genre_critic_scores_result], 'static/data/genre-critic.json')

if __name__ == "__main__":
    spark = SparkSession.builder.appName('Music Data Analysis').getOrCreate()
    df = spark.read.csv("albums.csv", header=True)  # Assume CSV has headers
    genre_analysis(spark, df)
    spark.stop()  # Properly stop the Spark session
