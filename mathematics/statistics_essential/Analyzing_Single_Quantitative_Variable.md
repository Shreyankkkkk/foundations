# Source and attribution

These are my personal study notes based on the Khan Academy Statistics course.

- Course: Statistics
- Provider: Khan Academy
- Source: https://www.khanacademy.org/math/probability
- Copyright: © 2025 Khan Academy. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Khan Academy course materials.

# Standard Deviation

## Lesson 1 : Sample Variance

### Learning Objectives

- Distinguish between a **population** and a **sample**
- Understand the difference between **population variance** and **sample variance**
- Understand why sample variance uses **\(n-1\)** instead of \(n\)

---

### Population vs Sample

A **population** is the entire group we want to study.

A **sample** is a smaller group taken from that population.

For example:

- Population → everyone in a country
- Sample → 6 people surveyed from that population

The population has a true **population mean** and **population variance**, but these are often impractical or impossible to calculate directly.

Instead, we use statistics calculated from a sample to **estimate** population parameters.

| Population                        | Sample                   |
| --------------------------------- | ------------------------ |
| Population mean: \(\mu\)          | Sample mean: \(\bar{x}\) |
| Population variance: \(\sigma^2\) | Sample variance: \(s^2\) |
| Parameter                         | Statistic                |

---

### Example

Suppose a sample contains 6 people's daily TV watching:

$$
1.5,\;2.5,\;4,\;2,\;1,\;1
$$

The sample mean is:

$$
\bar{x}=\frac{1.5+2.5+4+2+1+1}{6}
$$

$$
\boxed{\bar{x}=2}
$$

This sample mean is a **statistic** used to estimate the unknown population mean.

---

### Population Variance

If we had the **entire population**, population variance would be calculated as:

$$
\boxed{
\sigma^2=
\frac{\sum_{i=1}^{N}(x_i-\mu)^2}{N}
}
$$

The process is:

1. Find the difference between each value and the population mean.
2. Square each difference.
3. Add the squared differences.
4. Divide by the number of observations \(N\).

---

### Why Can't We Directly Use Population Variance?

When working with a sample, we usually **do not know the population mean \(\mu\)**.

Instead, we calculate the sample mean:

$$
\bar{x}
$$

and use it to estimate the population mean.

For the example:

$$
\bar{x}=2
$$

The sum of squared deviations from the sample mean is:

$$
(1.5-2)^2+(2.5-2)^2+(4-2)^2+(2-2)^2+(1-2)^2+(1-2)^2
$$

$$
=0.25+0.25+4+0+1+1
$$

$$
=6.5
$$

---

### Dividing by \(n\)

If we divide by the sample size:

$$
\frac{6.5}{6}\approx1.08
$$

This is a possible calculation of variance, but it **systematically tends to underestimate the population variance** when used to estimate it from a sample.

---

### Sample Variance

The standard definition of **sample variance** uses \(n-1\) in the denominator:

$$
\boxed{
s^2=
\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}
}
$$

For the example:

$$
s^2=\frac{6.5}{6-1}
$$

$$
=\frac{6.5}{5}
$$

$$
\boxed{s^2=1.3}
$$

Using \(n-1\) gives a better estimate of the population variance.

---

### Why \(n-1\)?

Using the sample mean \(\bar{x}\) makes the data appear slightly less spread out than it truly is in the population.

Therefore, dividing by \(n\) tends to **underestimate** the population variance.

Using:

$$
\boxed{n-1}
$$

corrects for this systematic underestimation.

This is called **Bessel's correction**.

> \(n-1\) is not used because \(n\) is mathematically wrong.  
> It is used because we are estimating an unknown population variance from a sample.

---

### Mathematical Notation

Sample variance:

$$
\boxed{
s^2=
\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}
}
$$

where:

- \(x_i\) = individual sample observation
- \(\bar{x}\) = sample mean
- \(n\) = sample size
- \(s^2\) = sample variance

For population variance:

$$
\boxed{
\sigma^2=
\frac{\sum_{i=1}^{N}(x_i-\mu)^2}{N}
}
$$

where:

- \(x_i\) = individual population observation
- \(\mu\) = population mean
- \(N\) = population size
- \(\sigma^2\) = population variance

---

### Quick Distinction

|             | Population Variance            | Sample Variance                            |
| ----------- | ------------------------------ | ------------------------------------------ |
| Mean used   | \(\mu\)                        | \(\bar{x}\)                                |
| Denominator | \(N\)                          | \(n-1\)                                    |
| Symbol      | \(\sigma^2\)                   | \(s^2\)                                    |
| Purpose     | Describe the entire population | Estimate population variance from a sample |

#### Key Takeaway

> **Population variance divides by \(N\). Sample variance divides by \(n-1\) because the sample variance is being used to estimate the population variance.**

For the sample:

$$
1.5,\;2.5,\;4,\;2,\;1,\;1
$$

$$
\boxed{\bar{x}=2}
$$

$$
\boxed{s^2=1.3}
$$

### Video

[Sample variance](https://www.youtube.com/watch?v=iHXdzfF7UEs)

---

## Lesson 2 : Sample Standard Deviation and Bias

### Sample standard deviation

The **sample standard deviation** is defined as the square root of the unbiased sample variance:

$$
\boxed{s=\sqrt{s^2}}
$$

Since

$$
s^2=\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1},
$$

we get

$$
\boxed{s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}}
$$

#### Example

For the sample

$$
4,\ 3,\ 5,\ 7,\ 2,\ 9,\ 11,\ 7
$$

the sample mean is

$$
\bar{x}=6
$$

The sum of squared deviations is

$$
4+9+1+1+16+9+25+1=66
$$

Therefore the unbiased sample variance is

$$
s^2=\frac{66}{8-1}=\frac{66}{7}\approx9.43
$$

and the sample standard deviation is

$$
s=\sqrt{\frac{66}{7}}\approx3.07
$$

### Bias of sample standard deviation

Although \(s^2\) is an **unbiased estimator** of the population variance \(\sigma^2\),

$$
E[s^2]=\sigma^2,
$$

the sample standard deviation

$$
s=\sqrt{s^2}
$$

is **not generally an unbiased estimator** of the population standard deviation \(\sigma\).

The reason is that the square-root function is **nonlinear**:

$$
E[\sqrt{s^2}] \neq \sqrt{E[s^2]}
$$

in general.

So:

- \(s^2\) → unbiased estimator of \(\sigma^2\)
- \(s\) → biased estimator of \(\sigma\), despite being the standard estimator normally used

An exactly unbiased estimator for \(\sigma\) would require a correction that depends on the **underlying population distribution**, so there is no single simple \(n-1\)-style correction that works universally.

#### Key distinction

$$
\boxed{\text{Sample variance }s^2\text{ is unbiased for }\sigma^2}
$$

$$
\boxed{\text{Sample standard deviation }s\text{ is generally biased for }\sigma}
$$

The standard definition of \(s\) is still widely used because it is simple and useful, and it is based directly on the unbiased sample variance.

---

### Video

[Sample standard deviation and bias](https://www.youtube.com/watch?v=DNAnQBhGpRw)

---

## Lesson 3 : Mean and standard deviation versus median and IQR

### Choosing measures of center and spread

The appropriate measures depend on the shape of the data and the presence of outliers.

| Data                                       | Center     | Spread                 |
| ------------------------------------------ | ---------- | ---------------------- |
| Roughly symmetric, no significant outliers | **Mean**   | **Standard deviation** |
| Skewed or has significant outliers         | **Median** | **IQR**                |

#### Why?

The **mean** and **standard deviation** are sensitive to outliers.

A very large or small value can pull the mean toward itself and increase the standard deviation significantly.

The **median** and **IQR** are much more robust because they depend on the ordering of the data rather than the magnitude of extreme values.

For example, if one salary is changed from \$250,000 to \$250 million:

- The **mean** changes drastically.
- The **median** remains unchanged.
- The **standard deviation** changes drastically.
- The **IQR** remains unchanged.

#### Example

For the salaries

$$
35,\ 50,\ 50,\ 50,\ 56,\ 60,\ 60,\ 75,\ 250
$$

(in thousands):

$$
\text{Mean}\approx76.2
$$

$$
\text{Median}=56
$$

The \$250k salary is an extreme outlier, pulling the mean far above most of the data. The median is therefore a better measure of the typical salary.

The quartiles are:

$$
Q_1=50,\qquad Q_3=67.5
$$

so

$$
IQR=Q_3-Q_1=67.5-50=17.5
$$

The IQR remains unaffected by how extremely large the \$250k salary becomes.

### Key takeaway

$$
\boxed{\text{Symmetric data without major outliers}
\rightarrow \text{Mean + SD}}
$$

$$
\boxed{\text{Skewed data or significant outliers}
\rightarrow \text{Median + IQR}}
$$

This is why **median salary** and **median home price** are commonly reported: these quantities can be strongly skewed by a small number of unusually large values.

---

### Video

[Mean and standard deviation versus median and IQR](https://www.youtube.com/watch?v=qNKOi08NxHs)

---

# Percentiles and Z scores

## Lesson 1 : Calculating Percentile

### What is a Percentile?

A **percentile** describes the percentage of data values that fall below or at/below a particular value.

For a given data point \(x\), there are two common ways to calculate its percentile rank:

1. **Percentage of data below \(x\)**
2. **Percentage of data at or below \(x\)**

The choice matters when the value \(x\) actually appears in the dataset.

---

### Example

Suppose a dot plot contains the daily driving times of **14 school bus drivers**.

We want to find the percentile rank of a driver who drives:

$$
x=6\text{ hours/day}
$$

There are:

$$
7
$$

drivers with driving times **below 6 hours**.

Therefore:

$$
\frac{7}{14}\times100=50\%
$$

So, using the **below** definition:

$$
\boxed{6\text{ hours is at the 50th percentile}}
$$

---

### Including the Data Point

If we instead count the observations that are **at or below 6 hours**, we include the driver(s) at exactly 6 hours.

There are:

$$
8
$$

drivers at or below 6 hours.

Therefore:

$$
\frac{8}{14}\times100
\approx57.1\%
$$

The transcript approximates this as roughly the **56th percentile** based on the intended count/rounding in the question.

The important idea is that **different percentile-rank conventions can give slightly different answers**, especially when the target value occurs in the dataset.

---

### General Calculation

If \(N\) is the total number of observations:

#### Using values below \(x\)

$$\boxed{\text{Percentile rank}=\dfrac{\text{values below }x}{N}\times100}$$

#### Using values at or below \(x\)

$$\boxed{\text{Percentile rank}=\dfrac{\text{values below }x}{N}\times100}$$

Always pay attention to whether the question says **below** or **at or below**.

---

### Important Interpretation

If a value is at approximately the **50th percentile**, roughly half of the observations are below it.

For example:

$$
\boxed{x\text{ at the 50th percentile}}
$$

means approximately **50% of the data is below \(x\)**.

A higher percentile means the value is relatively higher compared with the rest of the dataset.

For example:

- 25th percentile → about 25% of observations are below the value
- 50th percentile → about 50% are below
- 90th percentile → about 90% are below

---

### Percentile vs Percentile Rank

The terms are closely related but can be used slightly differently depending on the textbook or convention.

- **Percentile** → a position in a distribution expressed as a percentage.
- **Percentile rank** → the percentage of observations at or below (or sometimes below) a particular value.

When solving a problem, **follow the definition being used by the question**.

---

### Key Takeaway

> **Percentile rank tells us what percentage of the data lies below or at/below a particular value.**

For \(x\):

$$\boxed{\text{Percentile rank}=\frac{\text{number of observations below }x}{N}\times100}$$

or, depending on the convention,

$$\boxed{\text{Percentile rank}=\frac{\text{number of observations at or below }x}{N}\times100}$$

**Always check whether the target value itself should be included.**

---

### Video

[Calculating percentile](http://youtube.com/watch?v=Ngyt8Q5tWkU)

---

## Lesson 2 : Z-score Introduction

### What is a Z-score?

A **Z-score** is a standardized score that tells us how many **standard deviations** a data point is above or below the mean.

In other words, it measures the position of a data point relative to the mean while expressing that distance in units of standard deviation.

The general formula is:

$$
\boxed{
z=\frac{x-\mu}{\sigma}
}
$$

where:

- \(x\) = data point
- \(\mu\) = population mean
- \(\sigma\) = population standard deviation
- \(z\) = Z-score

---

### Interpreting the Z-score

The sign tells us which side of the mean the observation is on:

- \(z>0\) → data point is **above the mean**
- \(z=0\) → data point is **exactly at the mean**
- \(z<0\) → data point is **below the mean**

The magnitude tells us how far away the data point is in standard deviation units.

For example:

$$
z=1
$$

means the observation is **1 standard deviation above the mean**.

$$
z=-2
$$

means the observation is **2 standard deviations below the mean**.

$$
z=0.5
$$

means the observation is **half a standard deviation above the mean**.

---

### Why Divide by the Standard Deviation?

First calculate:

$$
x-\mu
$$

This gives the distance between the data point and the mean in the **original units**.

However, the raw distance alone does not tell us how large that difference is relative to the overall variability of the data.

Dividing by the standard deviation converts the distance into **standard deviation units**:

$$
\boxed{
z=\frac{\text{distance from mean}}{\text{standard deviation}}
}
$$

This allows us to compare how far observations are from their respective means even when the datasets have different units or amounts of variation.

---

### Example: Winged Turtles

Suppose the entire population consists of 7 winged turtles with lengths (in cm):

$$
2,\ 2,\ 3,\ 2,\ 5,\ 1,\ 6
$$

The population mean is:

$$
\mu=\frac{2+2+3+2+5+1+6}{7}
$$

$$
\boxed{\mu=3}
$$

The population standard deviation is approximately:

$$
\boxed{\sigma=1.69}
$$

We can now calculate the Z-score for each observation.

---

### Example: A 2 cm Turtle

For:

$$
x=2
$$

the Z-score is:

$$
z=\frac{x-\mu}{\sigma}
$$

$$
z=\frac{2-3}{1.69}
$$

$$
z=\frac{-1}{1.69}
$$

$$
\boxed{z\approx-0.59}
$$

#### Interpretation

The 2 cm turtle is approximately:

$$
\boxed{0.59\text{ standard deviations below the mean}}
$$

Because the Z-score is negative, the turtle's length is below the population mean.

The other 2 cm turtle has the **same Z-score** because it has the same value.

---

### Example: A 6 cm Turtle

For:

$$
x=6
$$

we get:

$$
z=\frac{6-3}{1.69}
$$

$$
z=\frac{3}{1.69}
$$

$$
\boxed{z\approx1.77}
$$

#### Interpretation

The 6 cm turtle is approximately:

$$
\boxed{1.77\text{ standard deviations above the mean}}
$$

So it is more than one but less than two standard deviations above the mean.

---

### Standardized Score

A Z-score is an example of a **standardized score**.

Standardization transforms an observation from its original scale into a common scale based on:

- the mean
- the standard deviation

The resulting Z-score tells us the observation's position relative to the mean in standard deviation units.

This is useful because the raw value alone does not necessarily tell us whether an observation is unusual.

For example, a value of \(100\) could be extremely large in one dataset but completely ordinary in another. The Z-score accounts for the dataset's mean and variability.

---

### Z-score as a Measure of Unusualness

One major reason Z-scores are useful is that they help us judge how **usual or unusual** a data point is within its distribution.

Generally:

$$
|z|\text{ small}
\quad\Rightarrow\quad
\text{closer to the mean}
$$

and

$$
|z|\text{ large}
\quad\Rightarrow\quad
\text{farther from the mean}
$$

For example:

|  Z-score | Interpretation            |
| -------: | ------------------------- |
|    \(0\) | Exactly at the mean       |
|  \(0.5\) | \(0.5\) SD above the mean |
|   \(-1\) | \(1\) SD below the mean   |
|    \(2\) | \(2\) SD above the mean   |
| \(-2.5\) | \(2.5\) SD below the mean |

The larger the absolute value \(|z|\), the farther the observation is from the mean.

Later, this becomes particularly important when studying **normal distributions, percentiles, probability, and statistical inference**.

---

### Important Formula

For a population:

$$
\boxed{
z=\frac{x-\mu}{\sigma}
}
$$

Think of the formula as:

$$\boxed{\text{Z-score}=\frac{\text{observed value}-\text{mean}}{\text{standard deviation}}}$$

A useful mental model is:

> **Subtract the mean to find how far away you are; divide by the standard deviation to find how many standard deviations away you are.**

---

### Z-score and Units

Suppose \(x\) and \(\mu\) are measured in centimeters.

Then:

$$
x-\mu
$$

is also measured in centimeters.

The standard deviation \(\sigma\) is measured in centimeters as well, so:

$$
\frac{x-\mu}{\sigma}
$$

has no units.

Therefore, a Z-score is **dimensionless**.

This is one reason standardized scores are useful for comparing observations measured on different scales.

---

### Key Takeaway

> **A Z-score tells you how many standard deviations a data point is above or below the mean.**

$$
\boxed{
z=\frac{x-\mu}{\sigma}
}
$$

Remember:

- Positive \(z\) → above the mean
- Negative \(z\) → below the mean
- \(z=0\) → exactly at the mean
- Larger \(|z|\) → farther from the mean
- Z-scores are **standardized and unitless**

The central idea is simple:

$$
\boxed{
\text{Data point}
\rightarrow
\text{distance from mean}
\rightarrow
\text{divide by SD}
\rightarrow
\text{Z-score}
}
$$

---

### Video

[Z-score introduction](https://www.youtube.com/watch?v=5S-Zfa-vOXs)

---

## Lesson 3 : Comparing with Z-scores

### Why Use Z-scores to Compare Distributions?

Raw scores cannot always be compared directly when they come from **different distributions**.

Two exams, measurements, or datasets may have:

- Different means
- Different standard deviations
- Different scales

A score of \(80\) on one exam does not necessarily represent the same performance as a score of \(80\) on another exam.

Instead, we can compare the **Z-scores** of the observations.

A Z-score tells us how many standard deviations a data point is from its distribution's mean.

$$
\boxed{
z=\frac{x-\mu}{\sigma}
}
$$

---

### Example: LSAT vs MCAT

Suppose Juwan takes both the LSAT and MCAT.

#### LSAT

Mean:

$$
\mu=151
$$

Standard deviation:

$$
\sigma=10
$$

Juwan's score:

$$
x=172
$$

His Z-score is:

$$
z=\frac{172-151}{10}
$$

$$
z=\frac{21}{10}
$$

$$
\boxed{z=2.1}
$$

Therefore, Juwan scored **2.1 standard deviations above the LSAT mean**.

---

#### MCAT

Mean:

$$
\mu=25.1
$$

Standard deviation:

$$
\sigma=6.4
$$

Juwan's score:

$$
x=37
$$

His Z-score is:

$$
z=\frac{37-25.1}{6.4}
$$

$$
z=\frac{11.9}{6.4}
$$

$$
\boxed{z\approx1.86}
$$

Therefore, Juwan scored approximately **1.86 standard deviations above the MCAT mean**.

---

### Comparing the Results

We now have:

| Exam | Juwan's score |  Z-score |
| ---- | ------------: | -------: |
| LSAT |       \(172\) | \(2.10\) |
| MCAT |        \(37\) | \(1.86\) |

Although the raw scores cannot meaningfully be compared directly, their Z-scores can.

Since:

$$
2.10\gt 1.86
$$

Juwan performed **slightly better relative to the other test takers on the LSAT**.

The difference is relatively small, so his performances could reasonably be described as comparable.

---

### The General Method

When comparing a person's performance across different distributions:

#### Step 1: Calculate each Z-score

$$
z_1=\frac{x_1-\mu_1}{\sigma_1}
$$

$$
z_2=\frac{x_2-\mu_2}{\sigma_2}
$$

#### Step 2: Compare the Z-scores

The larger Z-score represents the observation that is **farther above its distribution's mean**.

For observations below their respective means, a more negative Z-score indicates a lower relative position.

---

### Why This Works

The raw difference from the mean:

$$
x-\mu
$$

tells us how far the observation is from the mean in the original units.

But this distance alone is not enough for comparisons between distributions.

Dividing by the standard deviation:

$$
\frac{x-\mu}{\sigma}
$$

expresses the distance in **standard deviation units**.

Therefore, Z-scores put observations from different distributions onto a common standardized scale.

This allows us to make statements such as:

> "This score is 2 standard deviations above its mean."

rather than relying on the original scoring scale.

---

### Important Assumption

The comparison is especially useful when the distributions are **roughly normal** or when the standardized scores are being interpreted within distributions where this comparison makes sense.

For normally distributed data, Z-scores can later be connected to **percentiles and probabilities**, which makes them particularly useful in statistical analysis.

---

### Z-score as Relative Performance

A useful way to think about a Z-score is:

$$
\boxed{
\text{Z-score}=\text{relative position within a distribution}
}
$$

For example:

$$
z=2
$$

means:

> The observation is 2 standard deviations above the mean of its distribution.

This does **not** mean the original score is "2" or that it is twice as good as the mean.

It means its position relative to the distribution is two standard deviations above average.

---

### Comparing Absolute vs Relative Performance

There are two different questions:

**Absolute performance:**

> What score did the person get?

**Relative performance:**

> How does that score compare with everyone else taking the same exam?

Z-scores are useful for answering the second question.

This distinction becomes important whenever different measurements have different scales or levels of variability.

---

### Key Takeaway

> **When comparing observations from different distributions, compare their Z-scores rather than their raw values.**

$$
\boxed{
z=\frac{x-\mu}{\sigma}
}
$$

A larger Z-score means the observation is farther above its distribution's mean in standard deviation units.

For Juwan:

$$
z_{\text{LSAT}}=2.10
$$

$$
z_{\text{MCAT}}\approx1.86
$$

Therefore:

$$
\boxed{\text{Juwan performed slightly better relative to others on the LSAT.}}
$$

The core idea:

$$
\boxed{
\text{Raw score}
\rightarrow
\text{standardize}
\rightarrow
\text{Z-score}
\rightarrow
\text{compare relative position}
}
$$

---

### Video

[Comparing with z-scores](https://www.youtube.com/watch?v=_rtQGAX5wsQ)

---

# Normal Distribution and Emperical Formula

## Lesson 1 : Sense of Normal Distribution

- A **normal distribution** is approximately **bell-shaped and symmetric**, with most values concentrated around the mean.
- Real-world data may be **approximately normal**, but usually won't be perfectly normal.
- The shape of a distribution depends on the type of data and the factors affecting it.

### Shapes to Recognize

- **Normal:** roughly symmetric with one central peak.
- **Right-skewed (positively skewed):** long tail to the **right**.
  - Usually **mean > median**
- **Left-skewed (negatively skewed):** long tail to the **left**.
  - Usually **mean < median**
- **Bimodal:** two distinct peaks.
- **Trimodal:** three distinct peaks.

### Main Takeaway

Before applying the properties of a normal distribution, look at the **shape of the data** and determine whether it is reasonably close to **bell-shaped and symmetric**.

### Video

[Introduction to Normal Distribution](https://www.youtube.com/watch?v=79duxPXpyKQ)

---

## Lesson 2 : Experical Formula

The **empirical rule** applies to data that follows a **normal distribution**.

- **68%** of data falls within **1 standard deviation** of the mean.
- **95%** falls within **2 standard deviations**.
- **99.7%** falls within **3 standard deviations**.

### Useful percentages for the tails

Because a normal distribution is **symmetric**:

- Within 1 SD: **68%** → outside = 32% → **16% in each tail**
- Within 2 SD: **95%** → outside = 5% → **2.5% in each tail**
- Within 3 SD: **99.7%** → outside = 0.3% → **0.15% in each tail**

### Quick way to use it

If given a value, first determine **how many standard deviations it is from the mean**, then use the empirical rule.

Example:

- A value **1 SD below the mean** → everything below it = **16%**
- A value **2 SD from the mean** → between −2 SD and +2 SD = **95%**
- A value **more than 3 SD above the mean** → **0.15%**

**Memory:**  
**1 → 68% | 2 → 95% | 3 → 99.7%**

### Video

[Experical Rule](https://www.youtube.com/watch?v=OhRr26AfFBU)

---

# Normal Distribution Calculation

## Lesson 1: Standard Normal Table for Proportions Below

### Core idea

To find the proportion of a normally distributed variable that is **below a given value**:

1. Calculate the **z-score**.
2. Look up the z-score in the **standard normal (z) table**.
3. The table gives the proportion **below** that z-score.

### Formula

$$
z = \frac{x-\mu}{\sigma}
$$

Where:

- \(x\) = the given value
- \(\mu\) = mean
- \(\sigma\) = standard deviation
- \(z\) = number of standard deviations the value is from the mean

### Example

Student heights are normally distributed with:

$$
\mu = 150\text{ cm}
$$

$$
\sigma = 20\text{ cm}
$$

Darnell's height is:

$$
x = 161.4\text{ cm}
$$

Calculate the z-score:

$$
z = \frac{161.4-150}{20}
$$

$$
z = \frac{11.4}{20}=0.57
$$

So Darnell is **0.57 standard deviations above the mean**.

### Using the z-table

Look up:

$$
z=0.57
$$

The standard normal table gives:

$$
P(Z\lt 0.57)=0.7157
$$

Therefore:

$$
\boxed{0.7157\%}
$$

or:

$$
\boxed{71.57\%}
$$

So approximately **71.57% of students have a height below Darnell's**.

### Key takeaway

> **Given value → calculate z-score → look up z-score → get proportion below**

### Important

- Positive \(z\) → value is **above** the mean.
- Negative \(z\) → value is **below** the mean.
- \(z=0\) → value is exactly at the mean.
- For this type of z-table, the value gives the **area/proportion to the left (below)** the z-score.

### Video

[Table Proportion Below](https://www.youtube.com/watch?v=Fo4kitkFB3I)

---

## Lesson 2 : Standard Normal Table for Proportion Above

### Core idea

To find the proportion of a normal distribution that is **above a given value**:

1. Calculate the **z-score**.
2. Use the standard normal (z) table to find the proportion **below** that z-score.
3. Subtract that value from \(1\).

### Formula

$$
z=\frac{x-\mu}{\sigma}
$$

Then:

$$
\boxed{P(X\gt x)=1-P(Z\lt z)}
$$

This works because the **total area under the normal curve is 1**.

### Example

Exam scores are normally distributed with:

$$
\mu=40
$$

$$
\sigma=3
$$

Ludwig's score is:

$$
x=47.5
$$

Calculate the z-score:

$$
z=\frac{47.5-40}{3}
$$

$$
z=\frac{7.5}{3}=2.5
$$

So Ludwig scored **2.5 standard deviations above the mean**.

### Using the z-table

Look up:

$$
z=2.50
$$

The z-table gives the proportion **below** this value:

$$
P(Z\lt 2.50)=0.9938
$$

But the question asks for the proportion **above** Ludwig's score.

Therefore:

$$
P(Z\gt 2.50)=1-0.9938
$$

$$
\boxed{P(Z\gt 2.50)=0.0062}
$$

So:

$$
\boxed{0.0062}
$$

or:

$$
\boxed{0.62\%}
$$

of exam scores are higher than Ludwig's.

### Key takeaway

> **For a proportion above a value, calculate the z-score, use the z-table for the area below, then subtract from 1.**

$$
\boxed{
\text{Above}
=
1-\text{Below}
}
$$

Remember:

- Positive \(z\) → above the mean
- Negative \(z\) → below the mean
- Standard z-tables give the **proportion below**
- For the proportion above:

$$
\boxed{1-\text{z-table value}}
$$

### Video

[Standard normal table for proportion above](https://www.youtube.com/watch?v=i9FzFfv1rQg)

---

## Lesson 3 : Standard Normal Table for Proportion Between Values

### Core idea

To find the proportion of a normal distribution that is **between two values**:

1. Calculate the **z-score** for the upper value.
2. Use the z-table to find the proportion **below** the upper value.
3. Calculate the **z-score** for the lower value.
4. Use the z-table to find the proportion **below** the lower value.
5. Subtract the two proportions.

### Formula

$$
\boxed{
P(a\lt X\lt b)=P(X\lt b)-P(X\lt a)
}
$$

Using z-scores:

$$
\boxed{
P(a\lt X\lt b)=P(Z\lt z_b)-P(Z\lt z_a)
}
$$

### Example

Laptop prices are normally distributed with:

$$
\mu=750
$$

$$
\sigma=60
$$

Find the proportion of prices between:

$$
\$624\text{ and }\$768
$$

#### Upper value: \$768

$$
z=\frac{768-750}{60}
$$

$$
\boxed{z=0.30}
$$

From the z-table:

$$
P(Z\lt 0.30)=0.6179
$$

#### Lower value: \$624

$$
z=\frac{624-750}{60}
$$

$$
\boxed{z=-2.10}
$$

From the z-table:

$$
P(Z\lt -2.10)=0.0179
$$

#### Find the area between

$$
0.6179-0.0179=0.6000
$$

Therefore:

$$
\boxed{0.6000}
$$

or:

$$
\boxed{60\%}
$$

of laptop prices are between \$624 and \$768.

### Key takeaway

> **For the proportion between two values, find the area below each value and subtract the smaller area from the larger area.**

$$\boxed{\text{Between}=\text{Below upper value}-\text{Below lower value}}$$

### Video

[Standard normal table for proportion between values](https://www.youtube.com/watch?v=uwhV0TAPmWc)

---

## Lesson 4 : Finding Z-score for a Percentile

### Core idea

Sometimes we are given a **percentile** and need to find the corresponding **z-score**.

Then, if the distribution has a known mean and standard deviation, we can use that z-score to find the actual value.

### Example

Resting pulse rates are approximately normally distributed with:

$$
\mu=80
$$

$$
\sigma=9
$$

The school wants to screen students in the **top 30%**.

Since the top 30% is above the cutoff, the area **below** the cutoff must be:

$$
100\%-30\%=70\%
$$

So we need the z-score whose cumulative area is approximately:

$$
0.70
$$

### Finding the Z-score

From the z-table:

$$
P(Z\lt 0.53)=0.7019
$$

while \(z=0.52\) is below the 70% threshold.

Therefore:

$$
\boxed{z\approx0.53}
$$

### Convert the Z-score to the Actual Value

A z-score of \(0.53\) means the cutoff is \(0.53\) standard deviations above the mean.

Use:

$$
x=\mu+z\sigma
$$

$$
x=80+(0.53)(9)
$$

$$
x=80+4.77
$$

$$
x=84.77
$$

Rounded to the nearest whole number:

$$
\boxed{85\text{ beats per minute}}
$$

So a resting pulse rate of approximately **85 bpm or higher** places a student in the top 30%.

### Key takeaway

> **To find a value from a percentile: find the corresponding z-score first, then convert the z-score back to the original units.**

$$
\boxed{x=\mu+z\sigma}
$$

For a **top \(p\%\)** cutoff:

$$
\boxed{\text{Area below cutoff}=1-p}
$$

### Video

[Finding z-score for a percentile](https://www.youtube.com/watch?v=S5_5KyCVjrU)

---

## Lesson 5 : Threshold for Low Percentile

### Core idea

A **lower percentile cutoff** tells us the largest value that is still within a certain percentage of the distribution.

For example, the **bottom 10%** corresponds to the **10th percentile**.

To find the cutoff:

1. Find the z-score corresponding to the desired percentile.
2. Convert that z-score into the original units using the mean and standard deviation.

### Example

Average drive-through wait times are approximately normally distributed with:

$$
\mu=185\text{ seconds}
$$

$$
\sigma=11\text{ seconds}
$$

Amelia only uses restaurants whose average wait time is in the **bottom 10%**.

We need the maximum wait time that is still in the bottom 10%.

### Finding the Z-score

The bottom 10% means:

$$
P(Z\lt z)=0.10
$$

From the z-table, the appropriate cutoff is approximately:

$$
\boxed{z=-1.29}
$$

The negative sign makes sense because the 10th percentile is **below the mean**.

### Convert to the Actual Value

Use:

$$
x=\mu+z\sigma
$$

$$
x=185+(-1.29)(11)
$$

$$
x=185-14.19
$$

$$
x=170.81
$$

So the cutoff is approximately:

$$
\boxed{171\text{ seconds}}
$$

If the goal is to ensure the wait time stays within the bottom 10%, **170 seconds** can be used as a conservative cutoff.

### Key takeaway

> **For a lower percentile, find the z-score whose area below it equals the desired percentile, then convert it back to the original units.**

$$
\boxed{x=\mu+z\sigma}
$$

For the bottom \(p\%\):

$$
\boxed{P(Z\lt z)=p}
$$

The z-score will generally be **negative** for percentiles below 50%.

### Video

[Threshold for low percentile](https://www.youtube.com/watch?v=umYWWMfxUCI)

---