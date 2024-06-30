---
title: "Python EDA - Tutorial 2: Transforming and Filtering"
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

# Tutorial 2: Transforming and Filtering

:::::: {.speaker-notes}
When we get some data to analyse, it almost always requires a bit of
preparation or *cleaning* before we can work productively with it.

We're now going to look at the tools Pandas gives us for:

* Transforming data - allowing us to calculate new columns and fix
  incorrect values and formats
* Filtering data - to discard data we aren't interested in analysing
::::::

In this tutorial you will:

* Learn about Pandas' core types and column data types
* Transform columns to clean your data and compute new columns
* Use Boolean conditions on columns to filter DataFrame rows

:::::: {.speaker-notes}
We'll run this first cell to import Pandas and Plotly, and to load
our DataFrame of listings in this notebook.
::::::

```code
%pip install pandas plotly nbformat

import pandas as pd
import plotly.express as px

listings_df = pd.read_csv('https://ben-denham.github.io/python-eda/data/inside_airbnb_listings_nz_2023_09.csv')

listings_df
```

## Data Types in Pandas

What is the *type* of a table of data?

```code
type(listings_df)
```

What is the *type* of an individual column?

```code
type(listings_df['room_type'])
```

:::::: {.speaker-notes}
* A tabular *DataFrame* is made up of many column *Series*.
* Pandas provides many functions, methods, and operations for working
  with both DataFrames and Series
* A particular function or method **may work for both a DataFrame or a
  Series**, but the *behaviour* of that function or method can be
  quite different for each type
* It is therefore very important to **always be aware of whether we're
  dealing with a DataFrame or a Series**

::::::

Check the data type of each column in the DataFrame:

:::::: {.practice}
```code
listings_df.info()
```
::::::

:::::: {.speaker-notes}
Notice that:

* Even though the CSV provided no data type information, numeric types
  have been automatically inferred by Pandas
* Non-numeric types like strings are listed as `object` (we only
  have strings here)
* **Types aren’t always what we want** - the `last_review` column
  should be a `datetime`
::::::


## Transforming Data

We can convert a column with datetime-like strings to have a datetime
data type:

:::::: {.practice-input}
```code
listings_df['last_review']
```
::::::

:::::: {.practice-output}
```code
pd.to_datetime(listings_df['last_review'])
```
::::::

:::::: {.speaker-notes}
We can replace a column by assigning a new Series to it, just like
we would with a Python variable.
::::::

Replace the `last_review` column with a new Series with a datetime
data type:

:::::: {.practice}
```code
listings_df['last_review'] = pd.to_datetime(listings_df['last_review'])
```
::::::

Check that the `last_review` column now has the correct data type:

```code
listings_df.info()
```

### Maths with columns

:::::: {.speaker-notes}
Applying standard Python maths operators on a Series performs the
operation on each value in the Series and returns a new Series.
::::::

Convert listing prices to Australian dollars:

:::::: {.practice-input}
```code
nzd_to_aud = 0.93

listings_df['price_nzd']
```
::::::

:::::: {.practice-output}
```code
nzd_to_aud = 0.93

listings_df['price_nzd'] * nzd_to_aud
```
::::::

:::::: {.speaker-notes}
Performing maths with two Series applies the operation *element-wise* to
each pair of values from the two Series.

Also note that we can add new columns to the end of our DataFrame by
assigning to a column that doesn't already exist in the DataFrame.
::::::

Add a `price_per_person` column to `listings_df`:

:::::: {.practice-input}
```code
listings_df['price_per_person'] =

listings_df
```
::::::

:::::: {.practice-output}
```code
listings_df['price_per_person'] = listings_df['price_nzd'] / listings_df['accommodates']

listings_df
```
::::::

### Applying Functions to DataFrames

:::::: {.speaker-notes}
While Pandas provides many more functions for transforming DataFrames
and Series, it is still often convenient to express a transformation
as plain-old-Python code applied to a single value or row.

We can do this by writing our transformation as a regular Python
function and then *applying* it to a Series or DataFrame.

For example, the function below can transform a single listing's ID
into a URL for the listing:
::::::

The following function transforms a listing ID into a URL:

```code
def id_to_url(id):
    numeric_id = id.removeprefix('l')
    return f'https://www.airbnb.co.nz/rooms/{numeric_id}'

id_to_url('l11909616')
```

:::::: {.speaker-notes}
Calling `.apply(id_to_url)` on a single column Series calls the
function with each value in the Series and uses the returned
values to construct a new Series.
::::::

Produce a series of listing URLs:

:::::: {.practice}
```code
listings_df['id'].apply(id_to_url)
```
::::::

:::::: {.speaker-notes}
We can also use `.apply()` with `axis='columns'` on an entire
DataFrame to pass an entire row at a time to the function.

The output will still be a single Series of the returned values.

The `row` passed into the function will be a Series representing a
single row in the DataFrame.

We can access the row's value for each column in the same way we
access columns in a DataFrame.
::::::

The following function produces a description from a listing row:

```code
def listing_to_description(row):
    room_type = row['room_type']
    host_name = row['host_name']
    return f'{room_type} by {host_name}'
```

Produce a Series of listing descriptions:

:::::: {.practice}
```code
listings_df.apply(listing_to_description, axis='columns')
```
::::::

:::::: {.speaker-notes}
One important point to know about `.apply()` is that **Pandas built-in
operations will often be much faster** than running plain-old-Python on
each row.

However, this often won't make much of a difference until you're
dealing with hundreds of thousands or millions of rows. And remember,
when exploring the data it's **most important for you to be able to
quickly translate your ideas into working code!**
::::::


## Filtering Rows

:::::: {.speaker-notes}
The first step to filtering the rows in a DataFrame is to specify
the conditions we want to filter by.

Using a comparison operator on a Series performs the comparison to
each value in the Series and returns a new Series full of Boolean
values.

A Boolean Series like this is commonly called a *mask*
::::::

Construct a *Boolean Series* that is `True` for listings in
`'Wellington City'`:

:::::: {.practice-input}
```code
wellington_mask =
```
::::::

:::::: {.practice-output}
```code
wellington_mask = listings_df['region_parent_name'] == 'Wellington City'
```
::::::

:::::: {.speaker-notes}
We can use the mask to return a new DataFrame that is filtered to contain
only the rows where the mask is `True`:
::::::

Use the `wellington_mask` to get a DataFrame of listings in Wellington:

:::::: {.practice}
```code
listings_df[wellington_mask]
```
::::::

:::::: {.speaker-notes}
* To view the unmatched rows, we'll want to *invert* the mask
  * `False` becomes `True` and `True` becomes `False`
* We can't just use Python's `not` operator, instead we have to use
  the tilde operator
  * Aside: This is because the behaviour of Python's Boolean operators
    can't be overridden by Pandas
::::::

Use the `wellington_mask` to get a DataFrame of listings NOT in Wellington:

:::::: {.practice}
```code
listings_df[~wellington_mask]
```
::::::

:::::: {.practice}
Note: Similar to `null` values in SQL, conditions on `NaN` values
always evaluate to `False`.
::::::

### Combining Filters

:::::: {.speaker-notes}
Using Boolean operators to combine masks is a powerful way to build up
complex filtering conditions.

Just like how we have to use tilde instead of `not` for inversion, we
need to use `&` instead of `and` and `|` instead of `or`.
::::::

Construct a *Boolean Series* that is `True` for listings that cost
less than $100 per night:

```code
cheap_mask = listings_df['price_nzd'] <= 100

cheap_mask
```

Find cheap listings in Wellington:

:::::: {.practice}
```code
listings_df[wellington_mask | cheap_mask]
```
::::::

Find listings that are either cheap OR in Wellington:

:::::: {.practice}
```code
listings_df[wellington_mask & cheap_mask]
```
::::::


:::::: {.speaker-notes}
The tools for transforming and filtering data we've used here are the
kind of code you'll spend much of your time writing when analysing
data with Pandas.

The next set of exercises will give you an opportunity to start
applying these tools to clean up and analyse the data.
::::::


# Practice Exercises

## 1. Analysing listing ratings

### 1a. Plotting the ratings

Guests may review a listing on a scale of 0 to 5 stars, and the mean
of those reviews is recorded as the *rating* of the listing.

We'd like to get an idea of the distribution of the typical ratings of
listings, so your first task is to plot a histogram of the
`review_scores_rating` column:

:::::: {.practice}
```code
px.histogram(listings_df, x='review_scores_rating')
```
::::::

### 1b. Thinking about distribution spikes

In your histogram, you should see that the smooth-ish shape of the
distribution is broken up by a series of spikes, especially around the
exact ratings of 0, 1, 2, 3, and 4. Why do you think that may be?

:::::: {.hint}
Listings with a small number of reviews are more likely to have a
rating that is either an exact number of stars or a simple ratio. For
example, a listing with a single review must have a rating that is
equal to the exact number of stars of its only review!

When considering summary statistics (like an average rating) it is
important to consider how many data points have made up that
statistic.
::::::

### 1c. Plotting filtered data

Let's seen what the distribution looks like if we ignore listings with
few reviews.

Plot a histogram of listings that have more than 100 reviews:

:::::: {.practice}
```code
px.histogram(listings_df[listings_df['number_of_reviews'] > 100], x='review_scores_rating')
```
::::::

Does plotting only listings with a large number of reviews reveal any
other insights about the data?

:::::: {.hint}
No listing with more than 100 reviews has a rating less than 4.0 stars.
::::::

## 2. Transforming and Filtering Practice

Combine the techniques we've learned in the last two tutorials to
answer these questions:

### 2a. What is the lowest cost booking I could make?

Note: Each listing has a minimum number of nights that you must book
for (recorded in the `minimum_nights` column).

:::::: {.practice}
```code
base_prices = listings_df['price_nzd'] * listings_df['minimum_nights']
base_prices.min()
```
::::::

:::::: {.hint}
You may find it helpful to multiply two columns and use `.min()` as
part of your answer.
::::::

### 2b. Which parent region has more affordable listings on average, Auckland or Wellington City?

:::::: {.practice}
```code
auckland_listings_df = listings_df[listings_df['region_parent_name'] == 'Auckland']
print(auckland_listings_df['price_nzd'].mean())

wellington_listings_df = listings_df[listings_df['region_parent_name'] == 'Wellington City']
print(wellington_listings_df['price_nzd'].mean())
```
::::::

:::::: {.hint}
You may find it helpful to use filters and `.mean()` as part of your
answer.
::::::

**Extra:** The term "affordable" is subject to interpretation here -
is a listing more affordable if it can accommodate more people for the
same price? Does your answer change depending on your interpretation
of affordable?

## 3. Extra for Experts - Data Cleaning

Pandas DataFrames and Series have many other methods that apply useful
transformations. You can find references for them at these links:

* https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
* https://pandas.pydata.org/pandas-docs/stable/reference/series.html

Try using some of them to perform the data cleaning tasks below.

### 3a. Filter out listings that are missing a rating

Use the
[`.isna()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.isna.html)
Series method to find listings that are missing a rating (i.e. the
rating is `NaN`).

:::::: {.practice}
```code
reviewed_listings_df = listings_df[~(listings_df['review_scores_rating'].isna())]

reviewed_listings_df
```
::::::

### 3b. Add a `filled_rating` column to `listings_df` that fills in missing ratings with the mean rating

Use the
[`.fillna()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.fillna.html)
Series method to replace missing values in a Series with a given value.

:::::: {.practice}
```code
rating_mean = listings_df['review_scores_rating'].mean()
listings_df['filled_rating'] = listings_df['review_scores_rating'].fillna(rating_mean)
```
::::::

> Filling in missing values with an average value can *sometimes* be a
> useful technique for applying machine learning models that cannot
> work when some data values are missing.

### 3c. Convert formatted price strings to numeric values

The original Inside Airbnb dataset provides each price as a formatted
string starting with a `$` and containing commas. The original
formatted values are retained in the `formatted_price` column.

Your task is to transform the `formatted_price` column into a numeric
`float` data type, just like the `price_nzd` column.

You may like to use the `.apply()` used in the tutorial, or try using
the
[`.str.replace()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.replace.html)
and
[`.astype()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.astype.html)
Series methods.

:::::: {.practice}
```code
(
    listings_df['formatted_price']
    .str.replace('$', '', regex=False)
    .str.replace(',', '', regex=False)
    .astype(float)
)
```
::::::
