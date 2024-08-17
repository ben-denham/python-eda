---
title: "Python EDA - Tutorial 3: Grouping and Presenting"
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

# Tutorial 3: Grouping and Presenting

In this tutorial you will:

* Visualise relationships between groups with Plotly
* Grouping and aggregating data with Pandas to compare subsets of your data
* Export the results of your analysis to share with others

:::::: {.speaker-notes}
Don't forget to run this first cell to import Pandas and Plotly, and to load
our DataFrame of listings in this notebook.
::::::

```code
%pip install pandas plotly nbformat

import pandas as pd
import plotly.express as px
# Ensure plots will be exported correctly by nbconvert
import plotly.io as pio
pio.renderers.default = 'notebook'

listings_df = pd.read_csv('https://ben-denham.github.io/python-eda/data/inside_airbnb_listings_nz_2023_09.csv')

listings_df
```

## Plotting groups

:::::: {.speaker-notes}
When exploring a dataset, we often want to compare different groups or
subsets of the data.

Plotly makes a lot of group comparisons easy if we have a *tidy*
DataFrame - with a **row for each data point** and a **column for each
attribute** - including *categorical* attributes we want to group by.

For example, we can specify a column to colour data points by.

**Note:** We can hide/show groups using the legend.
::::::

Colour each listing by its room type:

:::::: {.practice-input}
```code
px.scatter_mapbox(
    listings_df,
    lon='longitude',
    lat='latitude',
    zoom=3,
    height=500,
).update_layout(
    mapbox_style='open-street-map',
)
```
::::::

:::::: {.practice-output}
```code
px.scatter_mapbox(
    listings_df,
    lon='longitude',
    lat='latitude',
    zoom=3,
    height=500,
    color='room_type',
).update_layout(
    mapbox_style='open-street-map',
)
```
::::::

:::::: {.speaker-notes}
We can take this one step further and create a separate subplot for
the data points belonging to each group by specifying a categorical
column as a `facet_row` or `facet_col`.

In the plot below, note that we:

* Sort the data by the `accommodates` column, so that the facet plots
  are ordered by that value.
* Increase the height of the output to better view the large number of
  plots.
* Set `histnorm='percent'` so that groups with few data points still
  have a "full size" plot.
::::::

Plot the distribution of listing prices, with a separate subplot for
each number of people that a listing can accommodate:

```code
px.histogram(
    listings_df[listings_df['price_nzd'] < 500].sort_values(by='accommodates'),
    x='price_nzd',
    facet_row='accommodates',
    height=2000,
    histnorm='percent',
)
```

:::::: {.speaker-notes}
While not about strictly about groups, a `scatter_matrix` is a very
convenient shorthand to generate subplots for each combination of
numeric columns on the x and y axis:

* We limit the price data to focus on a more interesting subset.
* Some trends emerge, like the price floor for different values of
  `accommodates`.
::::::

Plot a scatter matrix of numeric columns:

```code
px.scatter_matrix(
    listings_df[listings_df['price_nzd'] < 500],
    dimensions=[
        'price_nzd',
        'accommodates',
        'review_scores_rating',
        'number_of_reviews',
    ],
    color='room_type',
    height=900,
    width=900,
)
```

### Plotting groups based on numeric columns

:::::: {.speaker-notes}
Not only can we colour points by categorical columns like `room_type`,
but we can also use numeric columns:
::::::

Colour each listing by its price (ignoring outliers):

:::::: {.practice-input}
```code
px.scatter_mapbox(
    listings_df[listings_df['price_nzd'] <= 500],
    lon='longitude',
    lat='latitude',
    zoom=3,
    height=500,
).update_layout(
    mapbox_style='open-street-map',
)
```
::::::

:::::: {.practice-output}
```code
px.scatter_mapbox(
    listings_df[listings_df['price_nzd'] <= 500],
    lon='longitude',
    lat='latitude',
    zoom=3,
    height=500,
    color='price_nzd',
).update_layout(
    mapbox_style='open-street-map',
)
```
::::::

:::::: {.speaker-notes}
Sometimes we'd like to treat a numeric column like a categorical
column in our visualisation.

We can do this by using `pd.qcut()` to create a categorical column by
dividing a numeric column into *bins*.

* Using `pd.qcut()` makes each bin **has the same number of data
  points**, while `pd.cut()` makes each bin **cover an equal-length
  interval of the numeric column**.
* We need to convert each "bin" value to a string in order to display
  it with Plotly.

::::::

Plot the distribution of review counts for different tiers of pricing:

:::::: {.practice-input}
```code
listings_df['price_bin'] =

px.box(
    # Ensure lower price bins are shown first.
    listings_df.sort_values(by='price_nzd'),
    x='price_bin',
    y='number_of_reviews',
)
```
::::::

:::::: {.practice-output}
```code
listings_df['price_bin'] = pd.qcut(listings_df['price_nzd'], q=10).astype(str)

px.box(
    # Ensure lower price bins are shown first.
    listings_df.sort_values(by='price_nzd'),
    x='price_bin',
    y='number_of_reviews',
)
```
::::::

## Grouping and aggregating data with Pandas

:::::: {.speaker-notes}
We can use Pandas' `groupby()` to split up a DataFrame according to
a categorical attribute.

If you're familiar with SQL, you'll see similarities to the `GROUP BY`
clause.

* We can loop over the "groups", getting the attribute value and a
  DataFrame of rows having that attribute value
* `.shape` returns the number of rows and number of columns as a pair
  (tuple)
::::::

Print the number of listings for each type of room:

:::::: {.practice-input}
```code
room_type_groups =

for room_type, room_type_group_df in room_type_groups:
    print('Room type:', room_type)
    print(room_type_group_df.shape[0])
```
::::::

:::::: {.practice-output}
```code
room_type_groups = listings_df.groupby('room_type')

for room_type, room_type_group_df in room_type_groups:
    print('Room type:', room_type)
    print(room_type_group_df.shape[0])
```
::::::

:::::: {.speaker-notes}
`groupby()` can also be used to produce a DataFrame of aggregate
statistics for each group. In the following, see how we:

* Specify the columns from which to create a group for each
  combinations of values (`['accommodates', 'room_type']`)
* Use indexing to select a list of columns to calculate the statistic
  for (`['price_nzd', 'review_scores_rating']`)
* Choose one or more statistics to calculate: `agg(['mean', 'std'])`
::::::

```code
indexed_stats_df = (
    listings_df
    .groupby(['accommodates', 'room_type'])
    [['price_nzd', 'review_scores_rating']]
    .agg(['mean', 'std'])
)

indexed_stats_df
```

* Calling `.agg()` with a list of statistics also converts the columns
  into a *multi-level index*
  * We can flatten them with a list comprehension
  * This issue does not occur when passing a single statistic name to
    `.agg()` instead of a list, or when performing aggregation against
    a single numeric column instead of a list.
* `.groupby()` converts the group columns into an *index*
  * We can convert them back into regular columns with
    `.reset_index()`

```code
stats_df = indexed_stats_df.copy()
stats_df.columns = ['_'.join(col) for col in stats_df.columns]
stats_df = stats_df.reset_index()

stats_df
```

:::::: {.speaker-notes}
`.groupby()` is a very powerful tool for reshaping data into the right
*tidy* format that will support the plot you want.
::::::

Such DataFrames produced with `groupby()` can be very useful for
producing plots of statistics, like bar charts:

```code
px.bar(
    stats_df.sort_values(by='accommodates'),
    x='accommodates',
    y='price_nzd_mean',
    color='room_type',
    barmode='group',
    title='Mean Price',
)
```

## Sharing results with others

:::::: {.speaker-notes}
We can easily generate a CSV of our cleaned up and aggregated DataFrame:
::::::

Export our group statistics to a CSV file:

```code
stats_df.to_csv('stats_df.csv', index=False)
```

Open the file browser from the left sidebar, right-click on the
`stats_df.csv`, and click `Download`.

### Sharing the notebook

:::::: {.speaker-notes}
We can also export our Jupyter notebook as a shareable HTML file.

* HTML is the **format used by web pages**, so we can **open the file
  in a web browser**.
* The key benefit of exporting as HTML is that the **plots will remain
  interactive**.
* Be careful of previews in SharePoint etc. that disable JavaScript.

::::::

To export this notebook as an HTML file:

1. Select `File -> Download -> Download .ipynb`
2. Open the file browser from the left sidebar, and upload the file
   you downloaded.
3. Run the following cell to execute the shell command to convert the
   uploaded `.ipynb` file to a `.html` file:
4. Right-click on the generated `python_eda_tutorial_3.html` file in
   the file browser and click `Download`.
5. Open the downloaded file in any web browser.

```code
!jupyter nbconvert --to html python_eda_tutorial_3.ipynb
```

:::::: {.speaker-notes}
Jupyter notebooks are a convenient tool for making repeatable reports.

1. When you have new data, just re-run the notebook with new input
   files.
2. Use Text cells to tell a story about the data - use Markdown for
   text formatting.
3. Advanced users can see exactly what code ran to produce the plot -
   allowing them to scrutinise your assumptions in interpreting and
   cleaning the data.
::::::

:::::: {.cell .markdown}
#### Markdown Demo

Text/Markdown cells let us provide **explanations** for our analyses
with *rich-text* formatting.

* This
* is
* a bullet list

1. This
2. is
3. a numbered list

```
{
    "format": "JSON",
    "title": "Code block demonstration"
}
```

$$
a^2 + b^2 = c^2
$$

A [link](https://www.markdownguide.org/cheat-sheet/) to a Markdown
guide.
::::::

# Practice Exercises

## 1. Bringing it all together

Use everything you've learned to answer a critical question for our
analysis: **Do more expensive listings typically have higher
ratings?**

There are different ways you could approach this analysis, but
consider the following points:

1. How do you want to judge how "expensive" a listing is? E.g. Should
   it be based on price, or price-per-person?
2. Given what we learned about ratings in the previous tutorial, do
   you want to exclude listings with few reviews?
3. Visualising the relationship between expensiveness and rating will
   be important, but what kind of visualisation will be easiest to
   interpret? Perhaps a scatter plot? Or maybe convert one of the
   columns into a categorical column with `pd.cut()` or `pd.qcut()`
   and then use a box plot? Or `groupby()` the categorical column to
   produce a table of summary statistics per group?
4. Add a Text/Markdown cell to explain what you can observe from your
   visualisation(s).

```code
```

<details>
<summary>Hint: code for calculating price-per-person</summary>

```python
listings_df['price_nzd_per_person'] = listings_df['price_nzd'] / listings_df['accommodates']
```

</details>

:::::: {.speaker-notes}
```python
listings_df['price_nzd_per_person'] = listings_df['price_nzd'] / listings_df['accommodates']
```
::::::


<details>
<summary>Hint: code for creating a categorical column from a numeric column</summary>

```python
listings_df['price_nzd_per_person_bin'] = pd.qcut(listings_df['price_nzd_per_person'], q=10).astype(str)

# If you bin the rating instead, you may need to drop duplicate bins.
listings_df['rating_bin'] = pd.qcut(listings_df['review_scores_rating'], q=10, duplicates='drop').astype(str)
```

</details>

:::::: {.speaker-notes}
```python
listings_df['price_nzd_per_person_bin'] = pd.qcut(listings_df['price_nzd_per_person'], q=10).astype(str)

# If you bin the rating instead, you may need to drop duplicate bins.
listings_df['rating_bin'] = pd.qcut(listings_df['review_scores_rating'], q=10, duplicates='drop').astype(str)
```
::::::


<details>
<summary>Hint: code for excluding listings with few reviews</summary>

```python
reviewed_listings_df = listings_df[listings_df['number_of_reviews'] > 100]
```

</details>

:::::: {.speaker-notes}
```python
reviewed_listings_df = listings_df[listings_df['number_of_reviews'] > 100]
```
::::::


<details>
<summary>Full example answer</summary>

```python
listings_df['price_nzd_per_person'] = listings_df['price_nzd'] / listings_df['accommodates']

listings_df['price_nzd_per_person_bin'] = pd.qcut(listings_df['price_nzd_per_person'], q=10).astype(str)

reviewed_listings_df = listings_df[listings_df['number_of_reviews'] > 100]

px.box(
    # Ensure lower price bins are shown first.
    reviewed_listings_df.sort_values(by='price_nzd_per_person'),
    x='price_nzd_per_person_bin',
    y='review_scores_rating',
)
```

</details>

:::::: {.speaker-notes}
```python
listings_df['price_nzd_per_person'] = listings_df['price_nzd'] / listings_df['accommodates']

listings_df['price_nzd_per_person_bin'] = pd.qcut(listings_df['price_nzd_per_person'], q=10).astype(str)

reviewed_listings_df = listings_df[listings_df['number_of_reviews'] > 100]

px.box(
    # Ensure lower price bins are shown first.
    reviewed_listings_df.sort_values(by='price_nzd_per_person'),
    x='price_nzd_per_person_bin',
    y='review_scores_rating',
)
```
::::::

## 2. Extra for Experts - Aggregation Practice

In the exercises below, be wary of indexes, column names, multi-index
columns in the DataFrames produced by `.groupby()`.

### 2a. Which parent region has the highest average listing price?

Extra: Does the answer change depending on whether you use a mean or
median for the average? what does that indicate?

:::::: {.hint}
Hint: Use a `groupby()` and `agg()` with an appropriate average
statistic like `'mean'` or `'median'`. Then sort the result by `price_nzd`.
::::::

:::::: {.practice}
```code
region_price_stats_df = (
    listings_df
    .groupby('region_parent_name')
    [['price_nzd']]
    .agg(['median', 'mean'])
)
region_price_stats_df.columns = ['_'.join(col) for col in region_price_stats_df.columns]
region_price_stats_df.sort_values(by='price_nzd_median')
```
::::::

### 2b. Do "home" listings cost more? Are they better reviewed? Do they accommodate more people?

Any listing with "home" in it's name should be considered a "home" listing.

:::::: {.hint}
Use `.str.lower()` and `.str.contains()` on the `name` column to
create a Boolean column that indicates which listings have names with
the keyword "home", then use appropriate `groupby()`s and/or plots.
::::::

:::::: {.practice}
```code
listings_df['is_home'] = listings_df['name'].str.lower().str.contains('home')
(
    listings_df
    .groupby('is_home')
    [['price_nzd', 'review_scores_rating', 'accommodates']]
    .agg(['mean', 'median'])
)
```
::::::

### 2c. Of hosts with at least 10 reviewed listings, who has the highest average rating?

:::::: {.hint}
Use a `groupby('host_name')` on `review_scores_rating` with
`.agg(['count', 'mean'])` to get both the count and mean of the
ratings. Then filter hosts based on the count of listings.
::::::

:::::: {.practice}
```code
host_stats_df = (
    listings_df
    .groupby('host_name')
    ['review_scores_rating']
    .agg(['count', 'mean'])
)
(
    host_stats_df
    [host_stats_df['count'] >= 10]
    .sort_values(by='mean')
)
```
::::::

### 2d. Use a bar chart to show how many listings of each room type there are in each parent region.

:::::: {.hint}
Use a `groupby()` and `agg()` with the `'size'` statistic (which
counts the number of rows in the group, as opposed to `'count'` which
counts the number of non-`NaN` values in a column).
::::::

:::::: {.practice}
```code
region_room_counts_df = (
    listings_df
    .groupby(['region_parent_name', 'room_type'])
    .agg('size')
    .reset_index()
)
px.bar(
    region_room_counts_df.sort_values(by=0, ascending=False),
    x='region_parent_name',
    y=0,
    color='room_type',
    barmode='group',
)
```
::::::
