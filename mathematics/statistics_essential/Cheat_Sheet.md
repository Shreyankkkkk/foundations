# Statistics & Probability — Cheat Sheet

## Descriptive Statistics

### Mean

\[
\bar{x} = \frac{\sum\_{i=1}^{n}x_i}{n}
\]

### Interquartile Range

\[
IQR = Q_3 - Q_1
\]

### Outlier Rule

Lower:
\[
Q_1 - 1.5(IQR)
\]

Upper:
\[
Q_3 + 1.5(IQR)
\]

---

## Variability

### Population Variance

\[
\sigma^2 = \frac{\sum\_{i=1}^{N}(x_i-\mu)^2}{N}
\]

### Sample Variance

#### Biased

\[
s^2 = \frac{\sum\_{i=1}^{n}(x_i-\bar{x})^2}{n}
\]

#### Unbiased

\[
s^2 = \frac{\sum\_{i=1}^{n}(x_i-\bar{x})^2}{n-1}
\]

### Population Standard Deviation

\[
\sigma = \sqrt{\frac{\sum\_{i=1}^{N}(x_i-\mu)^2}{N}}
\]

### Sample Standard Deviation

#### Biased

\[
s = \sqrt{\frac{\sum\_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}
\]

_*to do the same for unbiased, finding a formula is not as easy as subtracting one from the denominator, therefore even the unbiased sample variance cannot give unbiased sample standard deviation*_

---

## Notation

| Symbol       | Meaning                       |
| ------------ | ----------------------------- |
| \(x_i\)      | \(i\)-th observation          |
| \(n\)        | Sample size                   |
| \(N\)        | Population size               |
| \(\bar{x}\)  | Sample mean                   |
| \(\mu\)      | Population mean               |
| \(s^2\)      | Sample variance               |
| \(\sigma^2\) | Population variance           |
| \(s\)        | Sample standard deviation     |
| \(\sigma\)   | Population standard deviation |
| \(Q_1\)      | First quartile                |
| \(Q_2\)      | Median                        |
| \(Q_3\)      | Third quartile                |
| \(IQR\)      | Interquartile range           |
| \(\sum\)     | Sum                           |
