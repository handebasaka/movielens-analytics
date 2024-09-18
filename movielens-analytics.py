# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read datasets (you need to provide the related file path where your files saved)
movies = pd.read_csv('./data/movies.csv')
ratings = pd.read_csv('./data/ratings_sample.csv')
tags = pd.read_csv('./data/tags.csv')

# Glance at movies data
print(movies.sample(5))

# Extract the year from title
# We can add a new column to store the original title column, before changing it
movies['title_original'] = movies['title']

# Function to extract the year and title
def extract_year(title):
    if title[-7:].startswith(' (') and title[-1] == ')':
        year = int(title[-5:-1])  # Extract the 4-digit year
        new_title = title[:-7]    # Remove the last 7 characters (the year and parentheses)
        return new_title, year
    return title, None  # If no valid year, return the original title and None for the year

# Apply the function and create two new columns 'title' and 'year'
movies[['title', 'year']] = movies['title_original'].apply(lambda x: pd.Series(extract_year(x)))

# Fill NaNs with 0 and change the data type to integer
movies['year'] = movies['year'].fillna(0).astype(int)

# Extract genres by using movies
movie_genre = movies.drop(columns= ['title', 'title_original', 'year'])
movie_genre['genres'] = movie_genre['genres'].str.split('|')
movie_genre = movie_genre.explode(column= 'genres')
print(movie_genre.sample(5))

# Glance at ratings data
print(ratings.sample(5))

# Convert timestamp to datetime
ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit= 's')

# Extract year info from date for the further analysis
ratings['year'] = ratings['timestamp'].dt.year

# Create new DataFrames movie_rating and movie_rating_yearly
# Calculate average rating and the total number of ratings for each movie, save them into a new DataFrame as movie_rating_temp
movie_rating_temp = pd.DataFrame(ratings.groupby(['movieId',])['rating'].agg(['mean', 'count'])).reset_index().rename(columns={"mean": "avg_rating", "count": "total_ratings"})
movie_rating_temp['avg_rating'] = movie_rating_temp['avg_rating'].round(1)

# Merge movies and the calculated movie_rating_temp dataset
movie_rating = movies.merge(movie_rating_temp, how= 'left', on= 'movieId').drop(columns= ['genres', 'title_original', 'year'])

# Fiil NaNs with zero for total_ratings
movie_rating['total_ratings'].fillna(0, inplace= True)
print(movie_rating.sample(5))

# Calculate average rating and the total number of ratings for each movie and rating year, save them into a new DataFrame as movie_rating_yearly
movie_rating_yearly_temp = pd.DataFrame(ratings.groupby(['movieId', 'year'])['rating'].agg(['mean', 'count'])).reset_index().rename(columns={"year": "rating_year", "mean": "avg_rating", "count": "total_ratings"})
movie_rating_yearly_temp['avg_rating'] = movie_rating_yearly_temp['avg_rating'].round(1)

# Merge movies and the calculated movie_rating_yearly_temp dataset
movie_rating_yearly = movies.merge(movie_rating_yearly_temp, how= 'left', on= 'movieId').drop(columns= ['genres', 'title_original', 'year'])

# Fiil NaNs with zero for total_ratings
movie_rating_yearly['total_ratings'].fillna(0, inplace= True)
print(movie_rating_yearly.sample(5))


# region Question-1

# Merge movie_genre and movie_rating
top_5_genres_temp = movie_genre.merge(movie_rating, how= 'left', on= 'movieId')

# Find the 5 top-rated genres 
top_5_genres = pd.DataFrame(top_5_genres_temp.groupby('genres')['avg_rating'].mean()).reset_index().sort_values('avg_rating', ascending= False).head(5)
print(top_5_genres)

# Merge movie_genre and movie_rating_yearly 
genre_rating_temp = movie_genre.merge(movie_rating_yearly, how= 'left', on= 'movieId')

# Calculate the average rating for each genre year by year
genre_rating = pd.DataFrame(genre_rating_temp.groupby(['genres', 'rating_year']).agg({'avg_rating' : 'mean', 'total_ratings' : 'sum'})).reset_index()
genre_rating['avg_rating'] = genre_rating['avg_rating'].round(1)

# Filter 5 top-rated genres
genre_rating_top_5 = genre_rating[genre_rating['genres'].isin(top_5_genres['genres'].tolist())]

# Visualize the average ratings of 5 top-rated genres over the year
# Set the theme and size of the plot
sns.set_theme(style= 'darkgrid', palette= 'Set2')
plt.figure(figsize=(10,8))

# Create the plot, change the title and legend
sns.lineplot(data= genre_rating_top_5, x= 'rating_year', y= 'avg_rating', hue= 'genres', linewidth= 2)
plt.title('Average Rating of 5 Top-Rated Genres Over the Years', fontsize= 18)
plt.legend(fontsize= 14, loc= 'upper right')

# Change labels and their settings
plt.xlabel('Year of Ratings', fontsize= 14)
plt.ylabel('Average of Ratings', fontsize= 14)
plt.xticks(fontsize= 12)
plt.yticks(fontsize= 12)

# Show the plot
plt.show();
# endregion

# region Question-2

# Visualize a histogram
# Set the theme and size of the plot
sns.set_theme(style= 'darkgrid', palette= 'Set2')
plt.figure(figsize=(15,12))

# Create the plot, change the title and legend
ax = sns.histplot(data= movie_rating, x= 'total_ratings', bins= 10)
plt.title('Distribution of Total Rating Numbers Among Movies', fontsize= 16)

# Change labels and their settings
plt.xlabel('Number of Total Ratings', fontsize= 14)
plt.ylabel('Number of Movies', fontsize= 14)
plt.xticks(fontsize= 14)
plt.yticks(fontsize= 14)

# Annotate the total number of movies for the y-axis (for more readability)
ax.bar_label(ax.containers[0], fontsize= 14, color= 'dimgray')

# Show the plot
plt.show();

# What are the films with more than 80.000 ratings?
print(movie_rating[movie_rating['total_ratings'] > 80000])
# endregion

# region Question-3

# Calculate the total number of tags for each movie
tags_temp = pd.DataFrame(tags.groupby('movieId')['tag'].count()).reset_index().rename(columns= {'tag': 'total_tags'})

# Merge movie_rating and the calculated tags dataset
movie_tag = movie_rating.merge(tags_temp, how= 'outer', on= 'movieId')

# Fill NaNs with zero for total_tags
movie_tag['total_tags'].fillna(0, inplace= True)
print(movie_tag.sample(5))

# Define the bins for avg_rating
bins = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
labels = ['0-0.5', '0.5-1.0', '1.0-1.5', '1.5-2.0', '2.0-2.5', '2.5-3.0', 
          '3.0-3.5', '3.5-4.0', '4.0-4.5', '4.5-5.0']

# Bin the avg_rating into categories
movie_tag['rating_bins'] = pd.cut(movie_tag['avg_rating'], bins=bins, labels=labels, include_lowest= False)

# Calculate the total number of tags by rating bins
movie_tag_bins = pd.DataFrame(movie_tag.groupby('rating_bins', observed= True)['total_tags'].sum()).reset_index()
print(movie_tag_bins)

# Visualize a bar plot
# Set the theme and size of plot
sns.set_theme(style= 'darkgrid', palette= 'Set2')
plt.figure(figsize=(10,8))

# Create the plot, change the title
ax = sns.barplot(data= movie_tag_bins, x= 'rating_bins', y= 'total_tags', width= 0.6, errorbar= None)
plt.title('Number of Tags Across Movies by Average Rating Ranges', fontsize= 16)

# Change labels and their settings
plt.xlabel('Average Rating', fontsize= 14)
plt.ylabel('Total Number of Tags', fontsize= 14)
plt.xticks(fontsize= 14)
plt.yticks(fontsize= 14)

# Annotate the total number of tags for the y-axis (for more readability)
ax.bar_label(ax.containers[0], fontsize= 12, color= 'dimgray')

# Show the plot
plt.show();
# endregion

# region Question-4

# Merge movies and movie_rating
movies_with_rating = movies.merge(movie_rating, how= 'left', on= 'movieId').drop(columns= ['genres', 'title_original', 'title_x', 'title_y']).rename(columns= {'year': 'movie_year'})

# Filter missing value for movie year (keep only not 0)
movies_with_rating_filtered = movies_with_rating[movies_with_rating['movie_year'] != 0]

# Visualize a line plot
# Set the theme and size of the plot
sns.set_theme(style= 'darkgrid', palette= 'Set2')
plt.figure(figsize=(10,8))

# Create the plot, change the title
sns.lineplot(data= movies_with_rating_filtered, x= 'movie_year', y= 'avg_rating', linewidth= 3, errorbar= None)
plt.title('Do More Recent Movies Get Higher Ratings?', fontsize= 16)

# Change labels and their settings
plt.xlabel('Year', fontsize= 14)
plt.ylabel('Average of Ratings', fontsize= 14)
plt.xticks(fontsize= 14)
plt.yticks(fontsize= 14)

# Add a solid vertical reference line at the year 2000
plt.axvline(x=2000, color='blue', linestyle='--', linewidth=2)  # You can change the style and color

# Show the plot
plt.show();
# endregion

# region Question-5

# Look at the top 10 movies with the highest number of ratings (total_ratings)
print(movies_with_rating.sort_values('total_ratings', ascending= False).head(10))

# Look at the top 10 movies with the highest average ratings (avg_rating)
print(movies_with_rating.sort_values('avg_rating', ascending= False).head(10))

# Bin the avg_rating into categories
movies_with_rating['rating_bins'] = pd.cut(movies_with_rating['avg_rating'], bins=bins, labels=labels, include_lowest= False)

# Calculate the total number of ratings by rating bins
movie_rating_bins = pd.DataFrame(movies_with_rating.groupby('rating_bins', observed= True)['total_ratings'].sum()).reset_index()
print(movie_rating_bins)

# Visualize the relationship between the number of ratings and average ratings
# Set the theme and size of the plot
sns.set_theme(style= 'darkgrid', palette= 'Set2')
plt.figure(figsize=(10,8))

# Create the plot, change the title
ax = sns.barplot(data= movie_rating_bins, x= 'rating_bins', y= 'total_ratings', errorbar=None)
plt.title('Relationship Between Number of Ratings and Average Rating', fontsize= 16)

# Change labels and their settings
plt.xlabel('Average Rating', fontsize= 14)
plt.ylabel('Number of Ratings', fontsize= 14)
plt.xticks(fontsize= 14)
plt.yticks(fontsize= 14)

# Show numbers in plain format instead of scientific notation
plt.ticklabel_format(style='plain', axis='y')

# Show the plot
plt.show();

# Visualize the relationship between the number of ratings and average ratings
# Set the theme and size of the plot
sns.set_theme(style= 'darkgrid', palette= 'Set2')
plt.figure(figsize=(10,8))

# Create the plot, change the title
ax = sns.barplot(data= movie_rating_bins, x= 'rating_bins', y= 'total_ratings', errorbar=None)
plt.title('Relationship Between Number of Ratings and Average Rating', fontsize= 16)

# Change labels and their settings
plt.xlabel('Average Rating', fontsize= 14)
plt.ylabel('Number of Ratings', fontsize= 14)
plt.xticks(fontsize= 14)
plt.yticks(fontsize= 14)

# Show numbers in plain format instead of scientific notation
plt.ticklabel_format(style='plain', axis='y')

# Show too small and big values by log
plt.yscale('log')

# Show the plot
plt.show();
# endregion

# region Question-6

# Create a function to determine whether it is a single-genre movie or a multiple-genre movie
def is_multiple_genres(genres):
    if '|' in genres:
        return "multiple"
    else:
        return "single"

# Apply the function and create a new columns 'is_multiple_genres'
movies['is_multiple_genres'] = movies['genres'].apply(lambda x: pd.Series(is_multiple_genres(x)))
movies.sample(5)

# Drop movies have no genres listed
single_multiple_genres = movies[movies['genres'] != '(no genres listed)']

# Merge single_multiple_genres and movie_rating
single_multiple_genres = single_multiple_genres.merge(movie_rating, how= 'left', on= 'movieId').drop(columns= ['genres', 'title_original', 'year', 'title_y'])

# Calculate the average rating for single-genres movies and multiple-genres movies
is_multiple_genres = pd.DataFrame(single_multiple_genres.groupby('is_multiple_genres')['avg_rating'].mean().round(2))
is_multiple_genres

# Visualize 'is_multiple_genres' to show that there is almost no difference
# Create the plot, change the title
sns.barplot(data= is_multiple_genres, x= 'avg_rating', y= 'is_multiple_genres', width= 0.5)
plt.title('Average Ratings of Single vs. Multi-Genre Movies', fontsize= 12)

# Change labels and their settings
plt.xlabel('Average of Ratings', fontsize= 10)
plt.ylabel('')
plt.yticks(['multiple', 'single'], ['Multiple Genre', 'Single Genre'], fontsize= 10)

# Show the plot
plt.show();

# Bin the avg_rating into categories
single_multiple_genres['rating_bins'] = pd.cut(single_multiple_genres['avg_rating'], bins=bins, labels=labels, include_lowest= False)

# Visualize 'is_multiple_genres' to show that there is almost no difference
# Set the theme and size of the plot
sns.set_theme(style= 'darkgrid', palette= 'Set2')
plt.figure(figsize=(10,8))

# Create the plot, change the title and legend
sns.barplot(data= single_multiple_genres, x= 'rating_bins', y= 'avg_rating', hue= 'is_multiple_genres', width= 0.7, errorbar= None)
plt.title('Comparison of Average Ratings Between Single and Multi-Genre Movies', fontsize= 14)
plt.legend(fontsize= 12, loc= 'upper left')

# Change labels and their settings
plt.xlabel('Average Rating Groups', fontsize= 12)
plt.ylabel('Average Rating', fontsize= 12)
plt.xticks(fontsize= 12)
plt.yticks(fontsize= 12)

# Show the plot
plt.show();
# endregion