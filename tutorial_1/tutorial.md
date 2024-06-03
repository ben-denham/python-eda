---
title: "Python EDA - Tutorial 1: Loading and Visualising"
jupyter:
  nbformat: 4
  nbformat_minor: 4
  kernelspec:
     display_name: Python
     language: python
     name: python3
  language_info:
     codemirror_mode:
       name: python
       version: 3
     file_extension: ".py"
     mimetype: "text/x-python"
     name: "python"
     nbconvert_exporter: "python"
     pygments_lexer: "ipython3"
     version: "3.8"
---

# Tutorial 1: Loading and Visualising

In this tutorial you will:

1. Learn how to run Python code in Jupyter notebooks
2. Load the CSV of Airbnb listings into a Pandas DataFrame
3. Use Pandas methods to calculate summary statistics of listing attributes
4. Use Plotly to produce simple plots to visualise the listings

## Jupyter Notebooks

:::::: {.speaker-notes}
* **Jupyter notebooks** are a very popular platform for Python coding,
  particularly for data analysis and visualisation.
* We are running Jupyter notebooks in **Google Colab** so that you
  don't need to install Python or Jupyter on your own computer.
  * Note: Because your notebooks will run on Google's servers, you
    shouldn't upload any company data or code you are not authorised
    to use outside of company-approved systems.
* Jupyter notebooks can also be run on your own desktop or server with
  a piece of software called **JupyterLab**.
::::::

> Note: Your notebooks in Google Colab will be saved to your Google
> Drive account, you can find previous notebooks from the `File ->
> Open notebook` menu.

In the empty *cell* below, type `1 + 1` and then **press the `Enter`
key *while holding* the `Shift` key** to run the code (there may be
short delay while the notebook session starts up):

:::::: {.practice}
```code
1 + 1
```
::::::

:::::: {.speaker-notes}
You should see the result of `2` - **the value of the final expression
in the cell will be displayed after the cell.**

**You can edit and re-run cells;** update your previous cell to
instead calculate `2 + 2`, then re-run it.
::::::

However, **we need to be careful of the order we run cells**. Try to
run the following cell:

```code
days_in_year / 7
```

:::::: {.speaker-notes}
You should see a `NameError` because we have attempted to use the
variable `days_in_year` before it has been defined.
::::::

Run the following cell to define `days_in_year`, then re-run the cell
above:

```code
days_in_year = 365.2425
```

:::::: {.speaker-notes}
When working in notebooks, it is a good idea to regularly select
`Runtime > Restart session and run all` from the menu to ensure our
code executes as we expect when run in order.
::::::


## Loading data with Pandas

:::::: {.speaker-notes}
We can use the `pandas` library to work with tabular data in Python,
like CSVs, SQL tables, and spreadsheets.

* Pandas is based on a lower-level maths library called `numpy`
* Pandas DataFrames are similar to R's DataFrames
::::::

Running the following cell will ensure we have Pandas installed
(however, it is pre-installed in Google Colab):

```code
%pip install pandas
```

Import the Pandas library:

:::::: {.practice}
```code
import pandas as pd
```
::::::

:::::: {.speaker-notes}
Importing Pandas as the alias `pd` is conventional, and saves us from
typing out `pandas` everytime we want to use it.
::::::

Now, let's load our CSV of Airbnb listings:

```code
listings_df = pd.read_csv('https://ben-denham.github.io/python-eda/data/inside_airbnb_listings_nz_2023_09.csv')
```

:::::: {.speaker-notes}
* `df` is a *conventional* variable suffix for a DataFrame.
* Pandas has many different `read_*` functions for reading from
  different types of files (e.g. `read_excel()`, `read_sql()`,
  `read_parquet()`).
::::::

Display the contents of the DataFrame:

:::::: {.practice}
```code
listings_df
```
::::::

:::::: {.speaker_notes}
Only a few rows from the top and bottom of the DataFrame are shown
::::::

Sort the DataFrame by the listing's current rating:

:::::: {.practice}
```code
listings_df.sort_values('review_scores_rating')
```
::::::

:::::: {.speaker_notes}
**This doesn't change the original DataFrame**, it produced a new
DataFrame that is sorted

Notice that the ratings sorted "last" are `NaN` (aka `null` or `None`
or "missing"). **By default `sort_values()` puts all `NaN` values at
the end, regardless of sort order.**

Indeed, these listings have a `number_of_reviews` equal to `0`. We'll need to
consider how to handle these rating-less listings later.
::::::

Select a subset of columns from a DataFrame:

:::::: {.practice}
```code
listings_df[['latitude', 'longitude']]
```
::::::

Now extract the `name` column on its own:

:::::: {.practice}
```code
listings_df['name']
```
::::::


## Summary Statistics

:::::: {.speaker-notes}
A simple and effective way to start exploring our data is to compute
*summary statistics*, which is really easy to do with Pandas.
::::::

Get summary statistics for all numeric columns of the listings:

:::::: {.practice}
```code
listings_df.describe()
```
::::::

:::::: {.speaker-notes}
`.describe()` gives us:

* The count of non-NaN values
* The mean and standard deviation (i.e. how far values spread from the mean)
* Min/max values
* The 25%, 50%, and 75% quantiles

### Mean vs Median

The mean (what most would call the "average") is the sum of all prices
divided by the number of listings.

The 50% quantile is also known as the median, and is the "middle"
value that is above the bottom 50% of values and below the top 50%.

The median price is quite a bit lower than the mean, suggesting there
is a smaller number of higher prices that are dragging the mean
higher.

Let's look at the maximum price.
::::::

Get the maximum price of any listing:

:::::: {.practice}
```code
listings_df['price_nzd'].max()
```
::::::

:::::: {.speaker-notes}
The maximum price looks suspiciously large,
this will warrant further investigation!

For categorical values, we can get an initial picture by
counting the frequency of each distinct value:
::::::

Count the frequency of each room type (values are listed by descending
frequency):

:::::: {.practice}
```code
listings_df['room_type'].value_counts()
```
::::::


## Plotting with Plotly

:::::: {.speaker-notes}
While useful, summary statistics only tell us part of the story. For
example, we are left with questions about what the difference between
the mean and median really means.

With the power of Python, there's nothing stopping us from
plotting our data to give us a clearer picture.
::::::

Running the following cell will ensure we have Plotly installed
(however, it is pre-installed in Google Colab):

```code
%pip install plotly
```

Import Plotly Express:

:::::: {.practice}
```code
import plotly.express as px
```
::::::

Create a scatter plot of listing latitude and longitude values:

:::::: {.practice}
```code
px.scatter(listings_df, x='longitude', y='latitude')
```
::::::

:::::: {.speaker-notes}
See how easy it is to plot our data.

Plotly Express makes such plots easy when we have *tidy data* - that is:

* Each row is an *observation* or *data point* to plot
* Each column is an *attribute* or *feature* describing some aspect of an observation
* Each cell contains only a single value
::::::

Plot the *distribution* of listing prices:

:::::: {.speaker-notes}
A histogram can show us the *distribution* or *shape* of the values in a column.

Each bar is showing us the frequency of values that fall into a certain range (or *bin*).
::::::

:::::: {.practice}
```code
px.histogram(listings_df, x='price_nzd')
```
::::::

:::::: {.speaker-notes}
This histogram helps us understand the difference between mean and median prices.

There are some very extreme prices in this dataset, almost certainly
anomalies. **We will want to filter these out later.**

> Side note: The impact of extreme values on the mean is also the
> reason you'll see economists talk about median house prices.

This example highlights the importance of visualising our data and not
just relying on summary statistics.
::::::


# Practice Exercises

## 1. Dataset Statistics

Using the methods we've looked at so far, answer the following
questions:

### 1a. Which "parent region" has the least listings?

:::::: {.hint}
Use the `.value_counts` method.
::::::

:::::: {.practice}
```code
listings_df.value_counts('region_parent_name')
```
::::::

### 2a. Which listing was last reviewed the longest time ago?

:::::: {.hint}
Use the `.sort_values` method.
::::::

:::::: {.practice}
```code
# Get the first `last_review` date.
listings_df.sort_values('last_review')
```
::::::

### 3a. What would you consider to be a "typical" minimum number of nights for a listing?

:::::: {.hint}
Look at the `mean`, median (`50%`), and `max` for `minimum_nights`.
::::::

:::::: {.practice}
```code
listings_df.describe()
```

The mean `minimum_nights` is slightly higher than the median, which
seems to be due to an abnormally high maximum value. We could further
confirm this by plotting a histogram.

Therefore, the median of `2` is a better choice for a "typical" minimum
number of nights.
::::::

## 2. Plotting Practice

Investigating relationships between variables is an incredibly
important part of exploratory data analysis.

Construct a scatter plot that shows the relationship between the
listing's price and its number of reviews (you may need to zoom in on
the plot).

:::::: {.hint}
Call `px.scatter` with `x` and `y` set to the columns for price and number of reviews.
::::::

:::::: {.practice}
```code
px.scatter(listings_df, x='price_nzd', y='number_of_reviews')
```
::::::

What does this scatter plot tell you about listings that are very
expensive (say, greater than $1,000 per night)?

:::::: {.practice}
These more expensive listings tend not to have more than about 100 reviews.

This might be important to consider if we plan to use review
scores to predict the price of an expensive listing.
::::::

## 3. Extra for Experts

Try out some other plot types from: https://plotly.com/python/plotly-express/

For example, try making a 3D scatter plot between 3 columns:
https://plotly.com/python/3d-scatter-plots/
