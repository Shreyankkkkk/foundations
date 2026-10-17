# Source and attribution

These are my personal study notes based on the Khan Academy Statistics course.

- Course: Statistics
- Provider: Khan Academy
- Source: https://www.khanacademy.org/math/probability
- Copyright: © 2025 Khan Academy. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Khan Academy course materials.

# Frequency Tables & Dot Plots

## Lesson 1 : Frequency Tables & Dot Plots

### Learning Objectives

- Explain how frequency tables summarize data
- Interpret dot plots and identify mode and range
- Count values that satisfy conditions in a dataset

---

### Frequency Table

A **frequency table** shows how often each value occurs in a dataset.

| Age | Frequency |
| --: | --------: |
|   5 |         2 |
|   6 |         1 |
|   7 |         4 |
|   8 |         0 |
|   9 |         4 |
|  10 |         1 |
|  11 |         0 |
|  12 |         2 |

- **Frequency** = number of times a value occurs.
- Each row represents a value and how often it appears.

---

### Dot Plot

A **dot plot** represents the same information visually.

- Each dot represents **one observation**.
- The number of dots above a value = its frequency.
- Repeated values are stacked vertically.

---

### What you can read from them

#### Most frequent value (mode)

- The value with the highest frequency.
- In this example, **7 and 9** are tied with a frequency of 4.

#### Range

$$
\text{Range} = \text{Maximum} - \text{Minimum}
$$

Example:

$$
12 - 5 = 7
$$

#### Counting values meeting a condition

For "How many are older than 9?", count values **strictly greater than 9**.

- 10 → 1
- 12 → 2
- Total → **3**

Frequency tables, dot plots, and the original list all represent the **same dataset** in different forms.

---

### Key reminder

- **Frequency** → how often something occurs
- **Dot plot** → visual representation of frequencies
- **Mode** → most frequent value
- **Range** → maximum − minimum

---

### Video

[Frequency tables and dot plots - YouTube](https://www.youtube.com/watch?v=gdE46YSedvE)

---

# Histograms

## Lesson 2 : Histograms

### Learning Objectives

- Understand how histograms display grouped numerical data
- Interpret bin ranges and bar heights
- Use histograms to answer questions about distribution and spread

---

### What is a histogram?

A **histogram** displays numerical data by grouping values into **ranges (bins)** and using bars to show the frequency in each range.

- **Bins** = intervals or ranges of values
- **Height of bar** = frequency
- Useful for seeing **distribution, shape, and spread**
- Helpful when many values exist and a dot plot becomes cluttered
- Histogram bars **touch** because the ranges represent continuous intervals

> **Histogram = numerical data grouped into bins + frequency shown by bar height.**

---

### Video

[Histograms - YouTube](https://www.youtube.com/watch?v=gSEYtAjuZ-Y)

---

# Interpreting Histograms

## Lesson 3 : Interpreting Histograms

### Learning Objectives

- Read the frequency of each bin
- Add frequencies to find totals
- Compare intervals by subtracting frequencies
- Be careful about bin boundaries

---

### Key ideas

- Each bar represents a **range (bin)** of values
- The **height** of the bar gives the number of observations in that range
- To find the **total number of observations**, add all frequencies
- To find how many observations satisfy a condition, add relevant frequencies
- To compare two ranges, subtract their frequencies

---

### Example

If the histogram has frequencies:

- 30–59 → 5
- 60–89 → 8
- 90–119 → 4
- 120–149 → 3

Total:

$$
5 + 8 + 4 + 3 = 20
$$

So there are **20 pies**.

For **60 or more cherries**:

$$
8 + 4 + 3 = 15
$$

---

### Important

Pay attention to the **bin boundaries** when interpreting a histogram.

For example:

- "60 or more" includes 60
- "More than 60" does **not** include 60

---

### Video

[Interpreting histograms - YouTube](https://www.youtube.com/watch?v=c02vjunQsJM)

---

# Measures of Central Tendency

## Lesson 4 : Measures of Central Tendency

### Learning Objectives

- Define mean, median, and mode
- Understand how each measure describes a dataset
- Decide when each measure is most useful

---

### Overview

Measures of central tendency describe a **typical or central value** of a dataset.

---

### Mean

The arithmetic mean is the usual "average":

$$
\text{Mean} = \frac{\text{sum of all values}}{\text{number of values}}
$$

- Sensitive to **outliers**
- Useful when the data is reasonably balanced

---

### Median

The **middle value** after ordering the data from least to greatest.

- **Odd** number of values → middle value
- **Even** number of values → mean of the two middle values
- Less affected by outliers than the mean

---

### Mode

The value that occurs **most frequently**.

- A dataset can have **no mode**
- It can also have **multiple modes**

---

### Quick distinction

| Measure    | What it represents  |
| ---------- | ------------------- |
| **Mean**   | Arithmetic average  |
| **Median** | Middle value        |
| **Mode**   | Most frequent value |

> Mean, median, and mode are all measures of **central tendency**, but they describe the center in different ways.

---

### Video

[Measures of Central Tendency - Mean, Median, and Mode](https://www.youtube.com/watch?v=h8EYEJ32oQ8)

---

## 1. Descriptive Statistics

**Statistics** is the study of data.

### Descriptive statistics

Used to **summarize and describe a dataset** without listing every observation.

Examples:

- Mean
- Median
- Mode
- Range / IQR
- Variance / standard deviation
- Graphical summaries

### Inferential statistics

Uses sample data to **make conclusions or inferences about a larger population**.

> **Descriptive → describe the data**  
> **Inferential → infer beyond the data**

---

## 2. Central Tendency

A **measure of central tendency** attempts to represent the **typical, middle, or central** value of a dataset.

The three basic measures are:

1. **Mean**
2. **Median**
3. **Mode**

They describe the center in different ways and therefore have different uses.

---

## 3. Arithmetic Mean

The **arithmetic mean** is what we commonly call the "average."

$$
\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}
$$

where:

- $x_i$ = individual observations
- $n$ = number of observations
- $\sum x_i$ = sum of all observations

### Example

Dataset:

$$
4, 3, 1, 6, 1, 7
$$

$$
\bar{x} = \frac{4+3+1+6+1+7}{6}
$$

$$
= \frac{22}{6}
= \frac{11}{3}
\approx 3.67
$$

Therefore:

$$
\boxed{\bar{x} \approx 3.67}
$$

### Important intuition

The mean incorporates **every observation**.

Therefore, it is sensitive to **extreme values/outliers**.

Example:

$$
0,\;7,\;50,\;10{,}000,\;1{,}000{,}000
$$

The $1{,}000{,}000$ heavily influences the mean.

---

## 4. Median

The **median** is the middle value after sorting the dataset.

### Procedure

1. Sort the observations from smallest to largest.
2. Find the middle.

### Odd number of observations

There is one middle observation.

Example:

$$
0,\;7,\;50,\;10{,}000,\;1{,}000{,}000
$$

There are 5 observations.

$$
\boxed{\text{Median} = 50}
$$

### Even number of observations

There are two middle observations.

Take their arithmetic mean.

Example:

$$
1,\;1,\;3,\;4,\;6,\;7
$$

The two middle values are:

$$
3,\;4
$$

Therefore:

$$
\text{Median} = \frac{3+4}{2} = 3.5
$$

$$
\boxed{\text{Median} = 3.5}
$$

### Important intuition

The median is **less sensitive to extreme values** than the mean.

For example:

$$
1,\;2,\;3,\;4,\;5
$$

has median $3$.

Changing the last observation drastically:

$$
1,\;2,\;3,\;4,\;1{,}000{,}000
$$

still gives:

$$
\boxed{\text{Median} = 3}
$$

This makes the median useful for **skewed distributions or datasets containing extreme observations**.

---

## 5. Mode

The **mode** is the value that occurs **most frequently**.

Example:

$$
4,\;3,\;1,\;6,\;1,\;7
$$

The value $1$ occurs twice, while everything else occurs once.

$$
\boxed{\text{Mode} = 1}
$$

### Possible situations

A dataset can have:

- **One mode** → unimodal
- **Multiple modes** → e.g., bimodal
- **No mode** → if no value occurs more frequently than the others

Example:

$$
1,\;2,\;3,\;4,\;5
$$

No mode.

---

## 6. Mean vs Median vs Mode

| Measure    | What it represents  | Sensitive to outliers?                              |
| ---------- | ------------------- | --------------------------------------------------- |
| **Mean**   | Arithmetic average  | **Yes**                                             |
| **Median** | Middle observation  | **Much less**                                       |
| **Mode**   | Most frequent value | Generally not affected by the magnitude of outliers |

### Quick intuition

**Mean:**

> "What is the arithmetic average?"

**Median:**

> "What's in the middle?"

**Mode:**

> "What's most common?"

---

## 7. Choosing a Measure of Center

There isn't one universally "correct" measure of center.

The appropriate measure depends on the **distribution and purpose**.

### Mean

Useful when the distribution is reasonably symmetric and you want every observation to contribute.

### Median

Useful when data are skewed or contain extreme values.

### Mode

Useful when the **most common category/value** matters.

---

## Key Takeaway

> **Central tendency = a way of summarizing where the center or typical value of a dataset lies.**

$$
\boxed{\text{Mean = arithmetic average}}
$$

$$
\boxed{\text{Median = middle}}
$$

$$
\boxed{\text{Mode = most frequent}}
$$

---

# Median from a Histogram

## Lesson 5 : Median from a Histogram

### Learning Objectives

- Identify how to find the median using a histogram
- Use cumulative frequencies
- Locate the interval containing the median

---

- For an **odd** number of data points:
  - Order the data.
  - Median = middle data point.

- For an **even** number of data points:
  - Order the data.
  - Median = mean of the two middle data points.
  - For 50 data points → median lies between the **25th and 26th** data points.

### Finding the Median Interval

- Count the frequencies in each histogram interval from lowest to highest.
- Keep a cumulative count.
- For 50 observations:
  - First 23 observations are in the first three intervals.
  - The 24th–35th observations fall in the next interval.
  - Therefore, the 25th and 26th observations are in that interval.

**Answer: 7.5–8 hours.**

---

# Estimating Mean and Median in Data Displays

## Lesson 6 : Estimating Mean and Median in Data Displays

### Learning Objectives

- Estimate median from a data display
- Estimate mean by reasoning about balance and skew
- Distinguish symmetric and skewed distributions

---

- **Median:** middle data point
- For an **odd** number of data points → middle point
- For an **even** number → average of the two middle points

### Estimating the Median from a Histogram

- Count data points from either end
- The median is the middle observation
- Example: 31 data points → **16th data point**
- Example: 14 data points → average of the **7th and 8th** data points

### Estimating the Mean from a Histogram

- Think of the mean as the **balancing point** of the distribution
- **Left-skewed:** mean is generally **to the left of the median**
- **Right-skewed:** mean is generally **to the right of the median**
- **Roughly symmetric:** mean and median are generally **close together**
- **Perfectly symmetric:** mean and median can be in exactly the same place

### Examples

- 31 athletes:
  - Median → interval **B**
  - Left-skewed distribution → mean → interval **A**

- 14 coworkers:
  - Median → average of 7th and 8th → **B**
  - Symmetric distribution → mean → **B**

---

### Video

[Estimating Mean and Median - YouTube](https://www.youtube.com/watch?v=rb-T5ppxJk0)

---

# Interquartile Range (IQR)

## Lesson 7 : Interquartile Range (IQR)

### Learning Objectives

- Define quartiles and IQR
- Use the median of each half to find Q1 and Q3
- Interpret the middle 50% of the data

---

- **IQR** describes the **middle 50%** of the data
- First, order the data from **least to greatest**
- Find the **median of the lower half** → **Q1**
- Find the **median of the upper half** → **Q3**
- **IQR = Q3 − Q1**

---

### Example 1

Data:

4, 4, 4, 6, 7, 10, 11, 12, 14, 15

- Median = 10
- Lower half: 4, 4, 4, 6 → Q1 = (4 + 4) / 2 = 4
- Upper half: 11, 12, 14, 15 → Q3 = (12 + 14) / 2 = 13
- IQR = 13 − 4 = 9

---

### Example 2

Data:

7, 9, 9, 10, 10, 10, 11, 12, 12, 14

- Median = 10
- Lower half: 7, 9, 9, 10, 10 → Q1 = 9
- Upper half: 10, 11, 12, 12, 14 → Q3 = 12
- IQR = 12 − 9 = 3

---

### Video

[Interquartile Range - YouTube](https://www.youtube.com/watch?v=qLYYHWYr8xI)

---

# Box-and-Whisker Plots

## Lesson 8 : Box-and-Whisker Plots

### Learning Objectives

- Understand how box-and-whisker plots represent a dataset
- Order data to identify the minimum, maximum, median, and quartiles
- Construct a box-and-whisker plot
- Understand why the median is excluded when calculating quartiles

---

### What is a Box-and-Whisker Plot?

A **box-and-whisker plot** is a visual representation of a dataset that shows its:

- Minimum value
- First quartile (Q1)
- Median
- Third quartile (Q3)
- Maximum value

These five values are often called the **five-number summary**.

> **Box-and-whisker plot = minimum + Q1 + median + Q3 + maximum**

---

### Step 1: Order the Data

Before constructing a box-and-whisker plot, arrange the data from **least to greatest**.

Example:

$$
7,\;8,\;8,\;8,\;9,\;9,\;9,\;9,\;10,\;11,\;13
$$

Ordering the data makes it possible to identify the median and quartiles.

---

### Step 2: Find the Minimum and Maximum

The smallest and largest values determine the ends of the plot.

For the example:

- **Minimum = 7**
- **Maximum = 13**

The **whiskers** extend to these values.

---

### Step 3: Find the Median

The **median** is the middle value of the entire ordered dataset.

There are 11 values:

$$
7,\;8,\;8,\;8,\;9,\;\boxed{9},\;9,\;9,\;10,\;11,\;13
$$

There are five values on each side of the middle value.

Therefore:

$$
\boxed{\text{Median} = 9}
$$

If a dataset has an **even number of values**, the median is the mean of the two middle values.

---

### Step 4: Find the First Quartile (Q1)

To find **Q1**, look at the lower half of the dataset.

**Exclude the median** when calculating the quartiles.

The lower half is:

$$
7,\;8,\;8,\;8,\;9
$$

The middle value is:

$$
\boxed{8}
$$

Therefore:

$$
\boxed{Q_1 = 8}
$$

---

### Step 5: Find the Third Quartile (Q3)

Now look at the upper half of the dataset, again **excluding the median**.

The upper half is:

$$
9,\;9,\;10,\;11,\;13
$$

The middle value is:

$$
\boxed{10}
$$

Therefore:

$$
\boxed{Q_3 = 10}
$$

---

### The Five-Number Summary

For this dataset:

| Statistic   | Value |
| ----------- | ----: |
| **Minimum** |     7 |
| **Q1**      |     8 |
| **Median**  |     9 |
| **Q3**      |    10 |
| **Maximum** |    13 |

These five values define the box-and-whisker plot.

---

### Parts of the Box-and-Whisker Plot

- **Left whisker** → minimum
- **Left side of the box** → Q1
- **Line inside the box** → median
- **Right side of the box** → Q3
- **Right whisker** → maximum

For the example:

$$
\boxed{7}\;-\;\boxed{8\;\;|\;\;9\;\;|\;\;10}\;-\;\boxed{13}
$$

The **box** represents the middle portion of the dataset, while the **whiskers** extend toward the minimum and maximum values.

---

### Important: Exclude the Median

When calculating Q1 and Q3, **exclude the median**.

For an odd number of observations:

1. Find the median of the entire dataset.
2. Remove/exclude that median.
3. Find the median of the lower half → Q1.
4. Find the median of the upper half → Q3.

> **Do not include the overall median when calculating Q1 and Q3 when the problem specifically says to exclude it.**

---

### Quick Procedure

To construct a box-and-whisker plot:

1. **Sort** the data from least to greatest.
2. Find the **minimum**.
3. Find the **median**.
4. Exclude the median.
5. Find **Q1** from the lower half.
6. Find **Q3** from the upper half.
7. Find the **maximum**.
8. Plot the five values on a number line.
9. Draw the box from Q1 to Q3 and the median inside the box.
10. Draw whiskers from the box to the minimum and maximum.

---

### Key Takeaways

- A **box-and-whisker plot** summarizes a dataset using five important values.
- Always **order the data** before finding the median and quartiles.
- The **median** is the middle value of the entire dataset.
- **Q1** is the median of the lower half.
- **Q3** is the median of the upper half.
- When instructed to exclude the median, **do not include it in either half** when calculating Q1 and Q3.
- The **whiskers** extend to the minimum and maximum.
- The **box** extends from Q1 to Q3.
- The line inside the box represents the median.

---

### Video

[Box-and-whisker plots - YouTube](https://www.youtube.com/watch?v=m6xURMj2ztk)

---

## Lesson 9 : Box-and-Whisker Plots with an Even Number of Data Points

### Learning Objectives

- Order data from least to greatest
- Identify the minimum and maximum values
- Find the median when there is an even number of observations
- Find Q1 and Q3 by finding the medians of the lower and upper halves
- Construct a box-and-whisker plot
- Understand why the median is excluded when calculating quartiles

---

### What is a Box-and-Whisker Plot?

A **box-and-whisker plot** is a visual representation of a dataset that shows its:

- Minimum value
- First quartile (**Q1**)
- Median
- Third quartile (**Q3**)
- Maximum value

These five values form the **five-number summary**.

> **Box-and-whisker plot = minimum + Q1 + median + Q3 + maximum**

The plot helps visualize both the **range** of the data and the location of its **center and middle 50%**.

---

### Step 1: Order the Data

The first step is to arrange all values from **least to greatest**.

Example:

$$
1,\;2,\;2,\;3,\;3,\;4,\;5,\;6,\;7,\;8,\;8,\;10
$$

Ordering the data makes it easier to identify the median and quartiles.

---

### Step 2: Find the Minimum and Maximum

The smallest and largest values determine the ends of the box-and-whisker plot.

For the example:

- **Minimum = 1**
- **Maximum = 10**

These values form the ends of the **whiskers**.

The whiskers therefore represent the overall **range** of the dataset.

$$
\text{Range} = \text{Maximum} - \text{Minimum}
$$

$$
10 - 1 = 9
$$

---

### Step 3: Find the Median

There are **14 observations**, so there is no single middle value.

For an even number of observations, the median is the **mean of the two middle values**.

The two middle values are:

$$
4,\;5
$$

Therefore:

$$
\text{Median} = \frac{4+5}{2}
$$

$$
\boxed{\text{Median} = 4.5}
$$

The median is located **between the two middle observations**.

> **Odd number of observations → one middle value**
>
> **Even number of observations → mean of the two middle values**

---

### Step 4: Find Q1

To find the first quartile (**Q1**), use the lower half of the ordered dataset.

The median is **4.5**, which is not itself one of the observations, so the lower half contains the first seven values:

$$
1,\;2,\;2,\;3,\;3,\;4,\;?
$$

The lower half has seven observations, and its middle value is:

$$
\boxed{2}
$$

Therefore:

$$
\boxed{Q_1 = 2}
$$

Q1 forms the **left boundary of the box**.

---

### Step 5: Find Q3

Now find the median of the upper half of the dataset.

The upper half contains seven observations, beginning with 5 and ending with 10.

Its middle value is:

$$
\boxed{7}
$$

Therefore:

$$
\boxed{Q_3 = 7}
$$

Q3 forms the **right boundary of the box**.

---

### Five-Number Summary

For the example:

| Statistic   | Value |
| ----------- | ----: |
| **Minimum** |     1 |
| **Q1**      |     2 |
| **Median**  |   4.5 |
| **Q3**      |     7 |
| **Maximum** |    10 |

These five values define the box-and-whisker plot.

---

### Parts of the Box-and-Whisker Plot

- **Minimum** → end of the left whisker
- **Q1** → left edge of the box
- **Median** → line inside the box
- **Q3** → right edge of the box
- **Maximum** → end of the right whisker

Conceptually:

$$
1\quad\text{—}\quad[\,2\quad|\quad4.5\quad|\quad7\,]\quad\text{—}\quad10
$$

The **box** represents approximately the middle 50% of the data.

The **whiskers** extend from the box toward the minimum and maximum.

---

### Excluding the Median

When calculating quartiles, the median of the entire dataset is **excluded**.

For an even number of observations, the median is usually between two observations rather than being an actual observation.

In this example:

$$
\text{Median} = 4.5
$$

Since 4.5 is not one of the original data values, the observations naturally split into two groups:

- **Lower half** → used to find Q1
- **Upper half** → used to find Q3

For an odd number of observations, the overall median is an actual data point, so if the instructions say to exclude it, leave that value out of both halves when calculating Q1 and Q3.

---

### Quick Procedure

To construct a box-and-whisker plot:

1. **Sort** the data from least to greatest.
2. Identify the **minimum**.
3. Identify the **maximum**.
4. Find the **median**.
5. Divide the data into a lower and upper half.
6. Find the median of the lower half → **Q1**.
7. Find the median of the upper half → **Q3**.
8. Plot the five-number summary.
9. Draw the **box** from Q1 to Q3.
10. Draw the **median line** inside the box.
11. Draw the **whiskers** from the box to the minimum and maximum.

---

### Key Takeaways

- A **box-and-whisker plot** shows the distribution of a dataset using five important values.
- Always **order the data** from least to greatest first.
- The **minimum and maximum** determine the ends of the whiskers.
- For an **even** number of observations, the median is the mean of the two middle values.
- **Q1** is the median of the lower half.
- **Q3** is the median of the upper half.
- The overall median is **excluded when calculating quartiles** when the problem specifies this.
- The **box** represents approximately the middle 50% of the data.
- The **whiskers** show the spread from the quartiles toward the minimum and maximum.

---

### Video

[Box-and-whisker plots - YouTube](https://www.youtube.com/watch?v=oajrmwCALmc)

---

## Lesson 10 : Interpreting Box-and-Whisker Plots

### Learning Objectives

- Identify the minimum and maximum values from a box-and-whisker plot
- Calculate the range of a dataset
- Identify the median from a box-and-whisker plot
- Understand how quartiles divide data into four groups
- Interpret what the box and whiskers tell us about a dataset

---

### What Does a Box-and-Whisker Plot Show?

A **box-and-whisker plot** is a visual representation of the spread of a dataset.

It shows:

- The **minimum** value
- The **first quartile (Q1)**
- The **median (Q2)**
- The **third quartile (Q3)**
- The **maximum** value

These five values form the **five-number summary**.

> **Box-and-whisker plots show both the spread and center of a dataset.**

---

### The Whiskers

The **whiskers** extend from the box toward the minimum and maximum values.

- The left whisker ends at the **minimum**
- The right whisker ends at the **maximum**

Therefore, the whiskers show the full range of the data.

### Example

Suppose a box-and-whisker plot shows:

- Minimum = 8 years
- Maximum = 50 years

The data range is:

$$
\text{Range} = \text{Maximum} - \text{Minimum}
$$

$$
= 50 - 8
$$

$$
\boxed{\text{Range} = 42\text{ years}}
$$

This means the tree ages range from **8 years to 50 years**, including both endpoints.

---

### The Median

The line inside the box represents the **median**.

The median divides the ordered dataset into two halves:

- Approximately **50% of the observations** are below the median.
- Approximately **50% of the observations** are above the median.

### Example

If the median tree age is:

$$
\boxed{21\text{ years}}
$$

then approximately half of the surveyed trees are younger than 21 years and approximately half are older than 21 years.

> **The median is the central value of an ordered dataset.**

---

### Quartiles

The box-and-whisker plot divides the data into **four groups**, called **quartiles**.

Each quartile represents approximately **25% of the observations**.

The four quartiles are:

1. **First quartile (Q1)**
2. **Second quartile (Q2)**
3. **Third quartile (Q3)**
4. **Fourth quartile**

The median is also called the **second quartile (Q2)**.

---

### Understanding the Four Quartiles

Suppose a box-and-whisker plot has:

- Minimum = 8
- Q1 = 14
- Median = 21
- Q3 = 33
- Maximum = 50

The data is divided approximately as follows:

| Section             | Range | Approximate proportion |
| ------------------- | ----- | ---------------------: |
| **First quartile**  | 8–14  |                    25% |
| **Second quartile** | 14–21 |                    25% |
| **Third quartile**  | 21–33 |                    25% |
| **Fourth quartile** | 33–50 |                    25% |

The exact number of observations in each section can vary slightly depending on the dataset and how quartiles are calculated.

---

### Reading the Five-Number Summary

A box-and-whisker plot can be read from left to right:

$$
\text{Minimum}
\rightarrow
Q_1
\rightarrow
\text{Median}
\rightarrow
Q_3
\rightarrow
\text{Maximum}
$$

For the example:

$$
8
\rightarrow
14
\rightarrow
21
\rightarrow
33
\rightarrow
50
$$

Therefore:

- **Minimum = 8**
- **Q1 = 14**
- **Median = 21**
- **Q3 = 33**
- **Maximum = 50**

---

### Range vs. Interquartile Range

The **range** measures the spread of the entire dataset:

$$
\boxed{\text{Range} = \text{Maximum} - \text{Minimum}}
$$

The **interquartile range (IQR)** measures the spread of the middle 50%:

$$
\boxed{\text{IQR} = Q_3 - Q_1}
$$

For the example:

$$
\text{Range} = 50 - 8 = 42
$$

and:

$$
\text{IQR} = 33 - 14 = 19
$$

So:

$$
\boxed{\text{Range} = 42}
$$

$$
\boxed{\text{IQR} = 19}
$$

---

### Interpreting the Position of the Median

The position of the median inside the box can give information about the distribution.

For example, if the median is closer to Q1 than Q3, the data may be more spread out in the upper portion.

Similarly, the lengths of the whiskers can show that the data extends farther in one direction.

In the tree-age example:

- Minimum = 8
- Q1 = 14
- Median = 21
- Q3 = 33
- Maximum = 50

The median is closer to Q1 than Q3, and the right whisker is longer than the left whisker.

This suggests that the data has more spread toward the **higher ages**.

> The box-and-whisker plot allows you to see the distribution and spread of the data without displaying every individual observation.

---

### Quick Procedure for Reading a Box-and-Whisker Plot

When given a box-and-whisker plot:

1. Find the **minimum** at the end of the left whisker.
2. Find **Q1** at the left edge of the box.
3. Find the **median** at the line inside the box.
4. Find **Q3** at the right edge of the box.
5. Find the **maximum** at the end of the right whisker.
6. Calculate the **range** if needed:

$$
\text{Range} = \text{Maximum} - \text{Minimum}
$$

7. Calculate the **IQR** if needed:

$$
\text{IQR} = Q_3 - Q_1
$$

---

### Key Takeaways

- A **box-and-whisker plot** shows the spread and center of a dataset.
- The **whiskers** extend to the minimum and maximum values.
- The line inside the box represents the **median**.
- **Q1** is the first quartile.
- **Q2** is the median.
- **Q3** is the third quartile.
- The data is divided into approximately **four groups of 25%**.
- The **range** describes the spread of the entire dataset:

$$
\boxed{\text{Range} = \text{Maximum} - \text{Minimum}}
$$

- The **IQR** describes the spread of the middle 50%:

$$
\boxed{\text{IQR} = Q_3 - Q_1}
$$

- The five-number summary is:

$$
\boxed{\text{Minimum},\;Q_1,\;\text{Median},\;Q_3,\;\text{Maximum}}
$$

---

### Video

[Box-and-whisker plots - YouTube](https://www.youtube.com/watch?v=b2C9I8HuCe4)

---

## Lesson 11 : Interpreting Box-and-Whisker Plots

### Learning Objectives

- Determine whether a statement is definitely true
- Determine whether a statement is definitely false
- Recognize when there is not enough information to decide
- Understand what a box-and-whisker plot can and cannot tell us

---

### Interpreting Statements from a Box-and-Whisker Plot

A box-and-whisker plot gives information about the **minimum, quartiles, median, and maximum**, but it does not show every individual data value.

When interpreting a statement, ask:

1. Is it **definitely true**?
2. Is it **definitely false**?
3. Or is there **not enough information**?

Sometimes multiple different datasets can produce the same box-and-whisker plot.

---

### Example Box Plot

Suppose a box-and-whisker plot shows:

- Minimum = 7
- Q1 = 10
- Median = 13
- Q3 = 15
- Maximum = 16

These values tell us about the distribution, but they do not tell us every individual student's age.

---

### 1. Using the Maximum

Suppose the maximum age is 16.

Statement:

> All of the students are less than 17 years old.

Since the largest possible age is 16:

$$
16 < 17
$$

Therefore, this statement is:

$$
\boxed{\text{Definitely true}}
$$

---

### 2. Using Q1 to Interpret Percentages

Suppose:

$$
Q1=10
$$

Q1 marks the boundary between the first and second quartiles.

Approximately 25% of the observations are in each quartile.

Therefore, approximately 75% of the observations are at or above Q1.

So:

> At least 75% of the students are 10 years old or older.

is:

$$
\boxed{\text{Definitely true}}
$$

There could even be some observations in the first quartile that are exactly 10.

---

### 3. The Exact Number of Observations Is Unknown

A box-and-whisker plot does **not** tell us exactly how many students are at the party.

Different datasets can produce the same box plot.

For example, with:

$$
Q1=10,\qquad \text{Median}=13,\qquad Q3=15
$$

some values between the quartiles could vary while keeping the same quartiles.

This means we must be careful about making statements about the **exact number of students** at a particular age.

---

### 4. Minimum and Maximum Do Not Give Exact Counts

Suppose:

$$
\text{Minimum}=7
$$

This tells us that at least one observation is 7.

However, it does **not** tell us whether there is exactly one 7-year-old.

There could be:

- one 7-year-old
- multiple 7-year-olds

Both can be consistent with the same box plot.

Therefore:

> There is only one seven-year-old.

is:

$$
\boxed{\text{Not enough information}}
$$

The same reasoning applies to the maximum.

If:

$$
\text{Maximum}=16
$$

we cannot tell whether there is exactly one 16-year-old or multiple 16-year-olds.

Therefore:

> There is only one 16-year-old.

is also:

$$
\boxed{\text{Not enough information}}
$$

---

### 5. Different Datasets Can Have the Same Box Plot

A box plot can remain unchanged even when individual observations change.

For example, values between Q1 and the median could vary while still producing:

$$
Q1=10
$$

and:

$$
\text{Median}=13
$$

Similarly, values between the median and Q3 could vary while still producing:

$$
\text{Median}=13
$$

and:

$$
Q3=15
$$

This is why a box plot does not provide enough information to determine every individual value.

---

### 6. "Exactly Half Are Older Than 13"

Suppose the median is:

$$
13
$$

It might seem that exactly half of the students must be older than 13.

However, the box plot does not necessarily tell us this.

Some observations could be exactly 13, and the number of observations can vary.

For example, one possible dataset could have:

$$
\frac{3}{7}
$$

of the students older than 13.

Another possible dataset could have exactly:

$$
\frac{1}{2}
$$

of the students older than 13.

Both situations can be consistent with the same box-and-whisker plot.

Therefore:

> Exactly half the students are older than 13.

is:

$$
\boxed{\text{Not enough information}}
$$

---

### Key Takeaway

When interpreting a box-and-whisker plot:

- Use the **minimum and maximum** to determine limits on the data.
- Use **quartiles** to reason about approximately 25%, 50%, and 75% of the observations.
- Do not assume the plot tells you the **exact number of observations**.
- The minimum does not tell you there is exactly one minimum value.
- The maximum does not tell you there is exactly one maximum value.
- Different datasets can produce the **same box-and-whisker plot**.
- If a statement could be true or false depending on the individual data values, the correct answer is:

$$
\boxed{\text{Not enough information}}
$$

> When interpreting statistics, it is important to distinguish between what the data **actually tells us** and what we are merely assuming.

### Video

[Interpreting Box Plots - Youtube](https://www.youtube.com/watch?v=oBREri10ZHk)

---

## Lesson 12 : Identifying Outliers Using the IQR

### Learning Objectives

- Use the **interquartile range (IQR)** to identify potential outliers
- Calculate the lower and upper outlier cutoffs
- Understand why the **1.5 × IQR rule** is used
- Represent outliers in a box-and-whisker plot

---

### What is an Outlier?

An **outlier** is a value that is unusually far from the rest of the data.

Sometimes outliers can be identified visually from a distribution.

For example, if most values are clustered around 13–19, values such as:

$$
1,\;1,\;6
$$

may look unusually low.

However, visual judgment is subjective.

To use a more consistent numerical rule, statisticians often use the **1.5 × IQR rule**.

---

### The 1.5 × IQR Rule

A value is considered an outlier if it is:

$$
\boxed{\text{less than } Q_1-1.5(\text{IQR})}
$$

or:

$$
\boxed{\text{greater than } Q_3+1.5(\text{IQR})}
$$

These values define the **lower and upper outlier cutoffs**.

> The 1.5 × IQR rule is a convention used by statisticians. It is not a universal law or mathematical rule of nature.

---

### Example Dataset

Consider the 15 observations:

$$
1,\;1,\;6,\;13,\;13,\;14,\;14,\;14,\;15,\;15,\;16,\;18,\;18,\;18,\;19
$$

The data are already arranged from least to greatest.

There are:

$$
15
$$

observations.

---

### Step 1: Find the Median

For 15 observations, the median is the **8th observation**.

There are 7 observations on each side.

The 8th observation is:

$$
\boxed{14}
$$

Therefore:

$$
\boxed{\text{Median}=Q_2=14}
$$

---

### Step 2: Find Q1

The lower half contains the first 7 observations:

$$
1,\;1,\;6,\;13,\;13,\;14,\;14
$$

The middle value is the 4th observation:

$$
\boxed{Q_1=13}
$$

---

### Step 3: Find Q3

The upper half contains the last 7 observations:

$$
15,\;15,\;16,\;18,\;18,\;18,\;19
$$

The middle value is the 4th observation:

$$
\boxed{Q_3=18}
$$

---

### Step 4: Find the IQR

The interquartile range is:

$$
\text{IQR}=Q_3-Q_1
$$

Therefore:

$$
\text{IQR}=18-13
$$

$$
\boxed{\text{IQR}=5}
$$

---

### Step 5: Find the Lower Outlier Cutoff

The lower cutoff is:

$$
Q_1-1.5(\text{IQR})
$$

Substitute the values:

$$
13-1.5(5)
$$

$$
=13-7.5
$$

$$
\boxed{5.5}
$$

Therefore, any value **less than 5.5** is an outlier.

In this dataset:

$$
1,\;1
$$

are below 5.5.

So the two 1s are outliers.

The value 6 is **not** an outlier because:

$$
6>5.5
$$

---

### Step 6: Find the Upper Outlier Cutoff

The upper cutoff is:

$$
Q_3+1.5(\text{IQR})
$$

Substitute the values:

$$
18+1.5(5)
$$

$$
=18+7.5
$$

$$
\boxed{25.5}
$$

Therefore, any value **greater than 25.5** is an outlier.

There are no observations greater than 25.5.

So there are **no upper-side outliers**.

---

### Final Outlier Rule for This Dataset

The two cutoffs are:

$$
\boxed{5.5}
$$

and:

$$
\boxed{25.5}
$$

Therefore:

- Values **less than 5.5** → outliers
- Values **greater than 25.5** → outliers
- Values between 5.5 and 25.5 → not outliers

For this dataset:

$$
\boxed{\text{Outliers}=1,\;1}
$$

---

### Why Use 1.5 × IQR?

The 1.5 × IQR rule provides a **numerical definition** for identifying unusually distant observations.

Instead of saying:

> "This value looks like an outlier."

we can use:

$$
Q_1-1.5(\text{IQR})
$$

and:

$$
Q_3+1.5(\text{IQR})
$$

to determine objective cutoff points.

The value **1.5** is a convention. Other choices could theoretically be used, but 1.5 is the commonly accepted rule for identifying outliers with the IQR method.

---

### Outliers and Box-and-Whisker Plots

Outliers can affect how a box-and-whisker plot is drawn.

For the dataset:

$$
1,\;1,\;6,\;13,\;13,\;14,\;14,\;14,\;15,\;15,\;16,\;18,\;18,\;18,\;19
$$

we have:

| Statistic   | Value |
| ----------- | ----: |
| **Minimum** |     1 |
| **Q1**      |    13 |
| **Median**  |    14 |
| **Q3**      |    18 |
| **Maximum** |    19 |

The box is determined by:

$$
Q_1=13
$$

to:

$$
Q_3=18
$$

with the median at:

$$
14
$$

---

### Box Plot Including Outliers

If we include every observation when drawing the whiskers, the whiskers extend from:

$$
1\quad\text{to}\quad19
$$

This includes the two values of 1, even though they are identified as outliers by the 1.5 × IQR rule.

---

### Box Plot Showing Outliers Separately

Alternatively, we can make the outliers visually distinct.

Since 1 is an outlier and 6 is not, the lower whisker can extend only to:

$$
6
$$

The upper whisker extends to:

$$
19
$$

The two values of 1 are then shown separately as outlier points.

Conceptually:

$$
1,\;1
\quad\cdots\quad
6
\;-\;
[13\;|\;14\;|\;18]
\;-\;
19
$$

This makes it clear that the two 1s are outliers.

---

### Important Distinction

There are two ideas to keep separate:

#### Full-data range

If all observations are included:

$$
\text{Range}=19-1=18
$$

#### Whiskers when outliers are displayed separately

If the outliers are excluded from the whisker endpoints, the lower whisker ends at the smallest **non-outlier**, which is:

$$
6
$$

The outliers are plotted separately.

> In a modified box plot, whiskers generally extend to the most extreme **non-outlier** values, while outliers are shown separately.

---

### Quick Procedure for Finding Outliers

Given a dataset:

1. **Order** the data from least to greatest.
2. Find **Q1**.
3. Find **Q3**.
4. Calculate the IQR:

$$
\text{IQR}=Q_3-Q_1
$$

5. Calculate the lower cutoff:

$$
Q_1-1.5(\text{IQR})
$$

6. Calculate the upper cutoff:

$$
Q_3+1.5(\text{IQR})
$$

7. Values below the lower cutoff are **outliers**.
8. Values above the upper cutoff are **outliers**.

---

### Key Takeaways

- The **IQR** can be used to identify potential outliers.
- The commonly used rule is:

$$
\boxed{\text{Lower cutoff}=Q_1-1.5(\text{IQR})}
$$

$$
\boxed{\text{Upper cutoff}=Q_3+1.5(\text{IQR})}
$$

- Values below the lower cutoff are outliers.
- Values above the upper cutoff are outliers.
- The **1.5 × IQR rule is a statistical convention**, not an absolute law.
- Outliers can be shown separately on a modified box-and-whisker plot.
- A box plot can therefore communicate both the main distribution and unusually distant observations.

#### Example Summary

For:

$$
1,\;1,\;6,\;13,\;13,\;14,\;14,\;14,\;15,\;15,\;16,\;18,\;18,\;18,\;19
$$

we have:

$$
Q_1=13,\qquad Q_3=18
$$

$$
\text{IQR}=5
$$

Lower cutoff:

$$
13-1.5(5)=5.5
$$

Upper cutoff:

$$
18+1.5(5)=25.5
$$

Therefore:

$$
\boxed{\text{Outliers}=1,\;1}
$$

### Video

[Judging Outliers - Youtube](https://www.youtube.com/watch?v=FRlTh5HQORA)

---
