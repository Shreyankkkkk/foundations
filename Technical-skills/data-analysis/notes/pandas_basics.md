# Pandas

---

**Using Kaggle: Pandas course**

---

## Getting Started

To use pandas, you will typically start with the following:

```python
import pandas as pd
```

---

## Creating Data

There are two core objectis in pandas: the _DataFrame_ and the _Series_

---

### DataFrame

A DataFrame is a table.
It contains an array of individual entries, each of which has a certain value. Each entry corresponds to a row (or record) and a column.

---

#### DataFrames as integers

For example

```python
pd.DataFrame({"Yes":[50, 21], "No": [131, 2]})

#       Yes	No
#    0	50	131
#    1	21	2
```

---

#### DataFrames are not limited to integers

```python
pd.DataFrame({'Bob': ['I liked it.', 'It was awful.'], 'Sue': ['Pretty good.', 'Bland.']})
```

- pd.DataFrame() constructor to generate these DataFrame objects.

- pd.Datafram( Dictionary )

  Default values of rows is 0, 1, 2, 3..

---

#### To assign row labels

```python
pd.DataFrame( {"Bob" : ["I liked it.", "It was awful."],
"Sue" : ['Pretty Good', 'Bland.']},
index = ['Product A', 'Product B'])
```

**NOTE** currently pd.DataFrame takes 2 arguments, the dictionary of data and "index = {iterable}" which defines the name of the rows

---

### Series

A series, by contrast, is a sequence of data values. if a DataFrame is a table, a Series is a lit.

for example

```python
pd.Series( [1, 2, 3, 4, 5] )

# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: int64
```

A series is a single column of DataFrame.

---

### Assigning row labels

same as dataframe, use "index"

```python
pd.Series([30, 40, 50], index = ['2015 Sales', '2016 Sales', '2017 Sales'], name = "Product A")

# 2015 Sales    30
# 2016 Sales    35
# 2017 Sales    40
# Name: Product A, dtype: int64
```

name = {value} is to name the series of data

---


