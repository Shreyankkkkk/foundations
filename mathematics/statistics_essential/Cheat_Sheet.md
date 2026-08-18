# Statistics & Probability — Cheat Sheet

## Descriptive Statistics

### Mean

$$
\bar{x} = \frac{\sum_{i=1}^{n}x_i}{n}
$$

### Interquartile Range

$$
IQR = Q_3 - Q_1
$$

### Outlier Rule

Lower:

$$
Q_1 - 1.5(IQR)
$$

Upper:

$$
Q_3 + 1.5(IQR)
$$

---

## Variability

### Population Variance

$$
\sigma^2 = \frac{\sum_{i=1}^{N}(x_i-\mu)^2}{N}
$$

### Sample Variance

#### Biased

$$
s^2 = \frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n}
$$

#### Unbiased

$$
s^2 = \frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}
$$

### Population Standard Deviation

$$
\sigma = \sqrt{\frac{\sum_{i=1}^{N}(x_i-\mu)^2}{N}}
$$

### Sample Standard Deviation

#### Biased

$$
s = \sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}
$$

_To do the same for unbiased, finding a formula is not as easy as subtracting one from the denominator; therefore even the unbiased sample variance cannot give an unbiased sample standard deviation._

---

## Notation

| Symbol     | Meaning                       |
| ---------- | ----------------------------- |
| $x_i$      | $i$-th observation            |
| $n$        | Sample size                   |
| $N$        | Population size               |
| $\bar{x}$  | Sample mean                   |
| $\mu$      | Population mean               |
| $s^2$      | Sample variance               |
| $\sigma^2$ | Population variance           |
| $s$        | Sample standard deviation     |
| $\sigma$   | Population standard deviation |
| $Q_1$      | First quartile                |
| $Q_2$      | Median                        |
| $Q_3$      | Third quartile                |
| $IQR$      | Interquartile range           |
| $\sum$     | Sum                           |

---

---

## Percentiles & Z-Scores

### Percentile Rank

Percentage of observations below a value:

$$
\boxed{
\text{Percentile Rank}
=
\frac{\#(\text{values below }x)}{N}\times100
}
$$

If the problem uses **at or below**:

$$
\boxed{
\text{Percentile Rank}
=
\frac{\#(\text{values at or below }x)}{N}\times100
}
$$

Always check whether the target value is included.

---

### Z-score

A Z-score tells how many standard deviations a value is above or below the mean.

$$
\boxed{
z=\frac{x-\mu}{\sigma}
}
$$

- \(z>0\) → above the mean
- \(z=0\) → at the mean
- \(z<0\) → below the mean
- Larger \(|z|\) → farther from the mean

Z-scores are **unitless**.

---

### Comparing Different Distributions

When comparing values from different distributions, compare their Z-scores rather than their raw scores.

$$
\boxed{
z_1=\frac{x_1-\mu_1}{\sigma_1}
}
$$

$$
\boxed{
z_2=\frac{x_2-\mu_2}{\sigma_2}
}
$$

The larger Z-score represents the higher relative position within its distribution.

---

## Normal Distribution

### Empirical Rule

For an approximately normal distribution:

$$
\boxed{68\%}
$$

within \(1\) SD of the mean.

$$
\boxed{95\%}
$$

within \(2\) SDs.

$$
\boxed{99.7\%}
$$

within \(3\) SDs.

Tail percentages:

| Distance from mean | Within | Each tail |
|---|---:|---:|
| \(1\sigma\) | \(68\%\) | \(16\%\) |
| \(2\sigma\) | \(95\%\) | \(2.5\%\) |
| \(3\sigma\) | \(99.7\%\) | \(0.15\%\) |

**Memory:**

$$
\boxed{68\%-95\%-99.7\%}
$$

---

## Normal Distribution Calculations

### Proportion Below

1. Calculate the Z-score:

$$
z=\frac{x-\mu}{\sigma}
$$

2. Look up \(z\) in the standard normal table.

$$
\boxed{P(X<x)=P(Z<z)}
$$

The z-table gives the cumulative area **to the left** of the Z-score.

---

### Proportion Above

$$
\boxed{
P(X>x)=1-P(Z<z)
}
$$

Steps:

1. Calculate \(z\).
2. Find the area below \(z\).
3. Subtract from \(1\).

$$
\boxed{\text{Above}=1-\text{Below}}
$$

---

### Proportion Between Two Values

For lower value \(a\) and upper value \(b\):

$$
\boxed{
P(a<X<b)=P(X<b)-P(X<a)
}
$$

Using Z-scores:

$$
\boxed{
P(a<X<b)
=
P(Z<z_b)-P(Z<z_a)
}
$$

Steps:

1. Find \(z_a\).
2. Find \(z_b\).
3. Look up both cumulative probabilities.
4. Subtract lower area from upper area.

$$
\boxed{\text{Between}=\text{Below upper}-\text{Below lower}}
$$

---

## Finding a Value from a Percentile

Once the desired percentile gives a Z-score, convert the Z-score to the original units:

$$
\boxed{
x=\mu+z\sigma
}
$$

### Top \(p\%\)

Convert the top percentage into the area **below** the cutoff:

$$
\boxed{
P(X<x)=1-p
}
$$

Then find \(z\) and use:

$$
\boxed{x=\mu+z\sigma}
$$

### Bottom \(p\%\)

The desired cumulative area is directly:

$$
\boxed{
P(X<x)=p
}
$$

Then find \(z\) and use:

$$
\boxed{x=\mu+z\sigma}
$$

---

## Quick Normal Distribution Decision Guide

| Question asks for... | Method |
|---|---|
| Below \(x\) | \(z\) → z-table |
| Above \(x\) | \(z\) → z-table → \(1-\text{area}\) |
| Between \(a\) and \(b\) | Two z-scores → subtract areas |
| Top \(p\%\) | \(1-p\) → find \(z\) → find \(x\) |
| Bottom \(p\%\) | \(p\) → find \(z\) → find \(x\) |

### Core Formulas

$$
\boxed{z=\frac{x-\mu}{\sigma}}
$$

$$
\boxed{x=\mu+z\sigma}
$$

$$
\boxed{\text{Above}=1-\text{Below}}
$$

$$
\boxed{\text{Between}=\text{Below upper}-\text{Below lower}}
$$
