## MovieLens Insight Explorer: Analyzing Trends, Ratings, and Genres

A scatterplot effectively displays the correlation between life expectancy and fertility rates across different countries over the years. In the notebook below, by animating the scatterplot, we will dynamically show how these key indicators of development and population have evolved between 1960 to 2023, revealing trends that static visualizations might miss.

**Dataset:** movielens is a non-commercial, personalized movie recommendation service and provides movies, ratings and tags data publicly. We will download the data from [here](https://grouplens.org/datasets/movielens/) and take the up-to-date datasets from 'MovieLens 32M'. This dataset describes 5-star rating and free-text tagging activity containing 32000204 ratings and 2000072 tag applications across 87585 movies. These data were created by 200948 users between 09.01.1995 and 12.10.2023. This dataset was generated on October 13, 2023.

***Note:*** *Since the original `ratings.csv` is too large, I used a sample version of it (with the first 20 rows) in the Python file. You can download the original files from the source I mentioned above or you can see the results coming from original data in the Jupyter Notebook.*

To get started analysis via Python, we will need some packages below:

- `pandas:` It is a data analysis and manipulation library that provides data structures and tools.
- `matplotlib.pyplot:` It is a plotting library for creating visualizations in Python.
- `seaborn:` It provides a high-level interface for drawing attractive and informative statistical graphics.



## Goals
- The goal of this project is to answer below questions to understand the trend between ratings, genres and tags.

**Questions**
1. What are the top-rated genres over the years? Analyze movies by their genres and calculate the average rating for each genre year by year.

2. What is the distribution of total number of ratings among movies? Analyze the distribution of the total number of ratings per movie.

3. Do movies with more number of tags have higher or lower average ratings? Analyze the relationship between the number of tags a movie receives and its average rating.

4. Do more recent movies get higher ratings? Compare the ratings of older movies (pre-2000) with more recent ones (post-2000). Are newer movies rated higher, or is there a trend that older films are more cherished?

5. Do movies with more number of ratings have higher or lower average ratings? Analyze the relationship between the number of ratings a movie receives and its average rating. Do more popular movies tend to get higher ratings?

6. Are highly-rated movies more likely to belong to multiple genres? Analyze if movies that are categorized under multiple genres (e.g., Comedy-Drama) tend to receive higher ratings compared to single-genre films.

*You will get graphs to answer these questions in the Python file but you can also find the answers and comments in the Jupyter Notebook.*

## Tools and Technologies Used
`Python`

`Pandas` for data manipulation 

`Matplotlib` and `Seaborn` for data visualization

## How to Run
clone:
```sh
git clone https://github.com/handebasaka/movielens-analytics
```
open the solution file:
```bash
cd movielens-analytics
```
run python script:
```bash
python3 movielens-analytics.py
```
