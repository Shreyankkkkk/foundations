# Source and attribution

These are my personal study notes based on the Khan Academy Statistics course.

- Course: Statistics
- Provider: Khan Academy
- Source: https://www.khanacademy.org/math/probability
- Copyright: © 2025 Khan Academy. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Khan Academy course materials.

# Two-Way Tables Introduction

## Lesson 1 : Representing Data with Venn Diagrams and Two-Way Tables

### Data with Multiple Categories

Sometimes observations can belong to **more than one category**.

For example, candies may:

- Have chocolate
- Have coconut
- Have **both**
- Have **neither**

Two common ways to represent this information are:

- **Venn diagrams**
- **Two-way tables**

---

### Venn Diagrams

A **Venn diagram** represents sets and their **overlaps**.

The rectangle represents the **universe** — the entire group being studied.

The circles represent the different **sets/categories**.

For example:

- Chocolate → one circle
- Coconut → another circle
- Overlap → chocolate **and** coconut
- Outside both circles → neither chocolate nor coconut

For 12 candies:

| Category | Number |
|---|---:|
| Chocolate only | 6 |
| Chocolate and coconut | 3 |
| Coconut only | 1 |
| Neither | 2 |

Check:

$$
6+3+1+2=12
$$

So all observations in the universe are accounted for.

### Important Parts

The **overlap** represents observations belonging to **both sets**.

$$
\boxed{\text{Chocolate and coconut}=3}
$$

Total chocolate:

$$
6+3=9
$$

Total coconut:

$$
1+3=4
$$

---

### Two-Way Tables

A **two-way table** organizes categorical data using **rows and columns**.

For the candy example:

| | Coconut | No Coconut | Total |
|---|---:|---:|---:|
| **Chocolate** | 3 | 6 | 9 |
| **No Chocolate** | 1 | 2 | 3 |
| **Total** | 4 | 8 | 12 |

Each cell represents a combination of two categories.

For example:

$$
\boxed{3=\text{Chocolate and coconut}}
$$

$$
\boxed{6=\text{Chocolate but no coconut}}
$$

$$
\boxed{1=\text{Coconut but no chocolate}}
$$

$$
\boxed{2=\text{Neither}}
$$

---

### Row and Column Totals

Totals can be found by adding across rows or columns.

Chocolate:

$$
3+6=9
$$

No chocolate:

$$
1+2=3
$$

Coconut:

$$
3+1=4
$$

No coconut:

$$
6+2=8
$$

Grand total:

$$
9+3=12
$$

or

$$
4+8=12
$$

### Key Takeaway

> **Venn diagrams and two-way tables are different ways of representing the same categorical data.**

- **Venn diagram** → emphasizes **sets and overlaps**
- **Two-way table** → organizes combinations into **rows and columns**
- **Overlap / intersection** → belongs to **both categories**
- **Outside all sets** → belongs to **neither category**
- Totals should account for **every observation**

$$
\boxed{
\text{Both methods represent the same information in different ways.}
}
$$

---

### Video

[Venn diagrams and two-way tables](https://www.youtube.com/watch?v=l5MrtV7ZN88)

---

## Lesson 2 : Relative Frequencies in Two-Way Tables

### What is Relative Frequency?

A **relative frequency** tells us how common something is compared with the total.

The general formula is:

$$\boxed{\text{Relative frequency}=\dfrac{\text{frequency}}{\text{relevant total}}}$$

It can be written as a **decimal, fraction, or percentage**.

---

### Column Relative Frequency

For a **column relative frequency**, divide each value by the **total of its column**.

Suppose we have:

| | Accident | No Accident |
|---|---:|---:|
| SUV | 28 | 97 |
| Sports car | 35 | 104 |

For SUVs, the total is:

$$
28+97=125
$$

Therefore:

$$
\frac{28}{125}=0.224\approx\boxed{0.22}
$$

and

$$
\frac{97}{125}=0.776\approx\boxed{0.78}
$$

For sports cars, the total is:

$$
35+104=139
$$

Therefore:

$$
\frac{35}{139}\approx\boxed{0.25}
$$

and

$$
\frac{104}{139}\approx\boxed{0.75}
$$

---

### Relative Frequency Table

| | Accident | No Accident | Total |
|---|---:|---:|---:|
| **SUV** | 0.22 | 0.78 | 1 |
| **Sports car** | 0.25 | 0.75 | 1 |

The relative frequencies within each column/category add to approximately:

$$
\boxed{1}
$$

or:

$$\boxed{100\text{\%}}$$

---

### Interpretation

For SUVs:

$$
0.22=22\%
$$

So approximately **22% of SUVs had an accident**.

Similarly:

$$
0.78=78\%
$$

So approximately **78% of SUVs had no accident**.

For sports cars:

$$
0.25=25\%
$$

had an accident, while:

$$
0.75=75\%
$$

did not.

### Key Takeaway

> **Relative frequency compares a frequency to the relevant total.**

For a column relative frequency:

$$\boxed{\text{Column relative frequency}=\dfrac{\text{cell value}}{\text{column total}}}$$

Remember:

- **Frequency** → actual number of observations
- **Relative frequency** → proportion/percentage of the relevant total
- Values in a relative-frequency column should add to **1 (100%)**

---

### Video

[Relative frequencies in two-way tables](https://www.youtube.com/watch?v=_ETPMszULXc)

---

# Distribution in Two-Way Tables

## Lesson 1 : Marginal and Conditional Distributions

### Joint Distribution

A **two-way table** can show the **joint distribution** of two variables.

For example, we could study the relationship between:

- **Time studied**
- **Percent correct on a test**

Each cell shows the number of students belonging to a particular combination of the two variables.

For example:

$$
\boxed{20}
$$

could mean 20 students studied between 21–40 minutes and scored between 60–79%.

---

### Marginal Distribution

A **marginal distribution** focuses on **one variable at a time**, ignoring the other variable.

It is found using the **row or column totals (margins)** of a two-way table.

For example, to find the marginal distribution of **percent correct**, add the counts across each study-time category.

The marginal distribution can be expressed as:

- **Counts**
- **Percentages**

To convert a count into a percentage:

$$\boxed{\text{Percentage}=\dfrac{\text{count}}{\text{total}}\times100}$$

For example, if 40 out of 200 students scored between 80–100%:

$$
\frac{40}{200}=0.20=20\%
$$

So:

$$\boxed{20\text{\%}}$$

of students scored between 80–100%.

### Important Idea

When finding a marginal distribution, **you are no longer considering the other variable**.

For example:

> Marginal distribution of percent correct → distribution of scores for **all students**, regardless of study time.

---

### Conditional Distribution

A **conditional distribution** describes the distribution of **one variable given that something is true about another variable**.

The word **"given"** tells us the condition.

For example:

> Distribution of percent correct **given that students studied between 41 and 60 minutes**.

First, restrict the data to students who studied between 41 and 60 minutes.

Then examine how their test scores are distributed.

If there are 86 students who studied between 41–60 minutes and 16 of them scored 80–100%:

$$
\frac{16}{86}\times100\approx18.6\%
$$

So approximately:

$$\boxed{18.6\text{\%}}$$

of the students who studied 41–60 minutes scored between 80–100%.

Repeat this calculation for each score category to obtain the **conditional distribution**.

---

### Marginal vs Conditional Distribution

| Distribution | What it asks? | How to calculate |
|---|---|---|
| **Marginal** | What is the distribution of one variable overall? | Use row/column totals |
| **Conditional** | What is the distribution of one variable **given** a condition on the other? | Restrict to the condition, then calculate percentages |

### Key Takeaway

> **Marginal distribution = distribution of one variable by itself.**

> **Conditional distribution = distribution of one variable given a particular value/category of another variable.**

Think:

$$
\boxed{\text{Marginal}=\text{one variable overall}}
$$

$$
\boxed{\text{Conditional}=\text{one variable given another}}
$$

For conditional distributions, the percentages within the chosen condition should add to approximately:

$$\boxed{100\text{\%}}$$

---

### Video

[Marginal and conditional distributions](https://www.youtube.com/watch?v=Iw9fEYIpPMA)

---

## Lesson 2 : Comparing Distributions in Two-Way Tables

### Comparing Categories

A two-way table can be used to compare how different groups are distributed across another variable.

For example, we can compare:

- **Gender** → men vs women
- **Voting preference** → Obama, Romney, or Other

When using **column relative frequencies**, each column represents the distribution **within that group**.

---

### Example: 2012 Presidential Election

| Voting preference | Men | Women |
|---|---:|---:|
| Obama | 42% | 52% |
| Romney | 52% | 43% |
| Other | 6% | 5% |
| **Total** | **100%** | **100%** |

The percentages in each column add to:

$$\boxed{100\text{\%}}$$

because each column describes the entire distribution for that group.

---

### Comparing Men and Women

To determine whether men were more likely than women to vote for Romney, compare the percentages **within each group**.

Men:

$$\boxed{52\text{\%}}$$

Women:

$$\boxed{43\text{\%}}$$

Since:

$$
52\%>43\%
$$

male voters were **more likely to vote for Romney** than female voters.

This can also be interpreted as:

> Among male voters, there was a 52% chance of voting for Romney, compared with 43% among female voters.

---

### Key Takeaway

> **When comparing groups in a two-way table, compare the relative frequencies for the same outcome across the groups.**

For column relative frequencies:

$$
\boxed{\text{Each column describes the distribution within that group.}}
$$

To compare whether one group is more likely to have an outcome:

1. Find the percentage for that outcome in each group.
2. Compare the percentages.
3. The larger percentage means that outcome is more common in that group.

---

### Video

[Comparing distributions in two-way tables](https://www.youtube.com/watch?v=MarqSlyz-lU)

---