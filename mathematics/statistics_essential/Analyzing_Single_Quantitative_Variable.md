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

# Comparing Distributions
