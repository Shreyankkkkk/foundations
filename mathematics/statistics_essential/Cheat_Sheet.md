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

| Distance from mean |     Within |  Each tail |
| ------------------ | ---------: | ---------: |
| \(1\sigma\)        |   \(68\%\) |   \(16\%\) |
| \(2\sigma\)        |   \(95\%\) |  \(2.5\%\) |
| \(3\sigma\)        | \(99.7\%\) | \(0.15\%\) |

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

| Question asks for...    | Method                              |
| ----------------------- | ----------------------------------- |
| Below \(x\)             | \(z\) → z-table                     |
| Above \(x\)             | \(z\) → z-table → \(1-\text{area}\) |
| Between \(a\) and \(b\) | Two z-scores → subtract areas       |
| Top \(p\%\)             | \(1-p\) → find \(z\) → find \(x\)   |
| Bottom \(p\%\)          | \(p\) → find \(z\) → find \(x\)     |

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

## Bivariate Data & Scatterplots

### Describing a Scatterplot

Always describe:

$$
\boxed{\text{Direction + Strength + Form + Outliers}}
$$

- **Positive** → \(x\uparrow,\ y\uparrow\)
- **Negative** → \(x\uparrow,\ y\downarrow\)
- **Strong** → points closely follow the pattern
- **Weak** → points are more scattered
- **Linear** → roughly follows a straight line
- **Non-linear** → follows a curve/non-straight pattern
- **Outlier** → point unusually far from the general pattern

---

## Line of Best Fit & Regression

### Line of Best Fit

A line of best fit represents the **overall linear trend** of a scatterplot.

$$
\boxed{
\text{Good line of best fit}
\rightarrow
\text{linear trend}
}
$$

Do **not** ignore data points just to make the line fit better.

---

### Regression Equation

$$
\boxed{\hat y=mx+b}
$$

- \(\hat y\) → predicted \(y\)
- \(m\) → slope
- \(b\) → \(y\)-intercept
- \(x\) → independent/explanatory variable
- \(y\) → dependent variable

---

### Slope Interpretation

$$
\boxed{
m=
\frac{\text{change in predicted }y}
{\text{change in }x}
}
$$

Interpret:

> For every \(1\)-unit increase in \(x\), predicted \(y\) changes by \(m\) units.

- \(m>0\) → predicted \(y\) increases
- \(m<0\) → predicted \(y\) decreases

---

### Y-Intercept

$$
\boxed{x=0\rightarrow\hat y=b}
$$

Interpret:

> When \(x=0\), the model predicts \(y=b\).

Check whether \(x=0\) is realistic and within the data's range.

---

## Interpolation vs Extrapolation

- **Interpolation** → estimate **within** the observed data range.
- **Extrapolation** → estimate **outside** the observed data range.

$$
\boxed{
\text{Within range}\rightarrow\text{Interpolation}
}
$$

$$
\boxed{
\text{Outside range}\rightarrow\text{Extrapolation}
}
$$

Extrapolation assumes the observed trend continues beyond the available data.

---

## Correlation

### Correlation Coefficient

$$
\boxed{-1\le r\le1}
$$

\(r\) measures the **direction and strength of a linear relationship**.

- \(r>0\) → positive linear relationship
- \(r<0\) → negative linear relationship
- \(r\approx0\) → little/no **linear** relationship
- \(|r|\) close to \(1\) → strong linear relationship
- \(|r|\) close to \(0\) → weak linear relationship

$$
\boxed{\text{Sign of }r\rightarrow\text{direction}}
$$

$$
\boxed{|r|\rightarrow\text{strength}}
$$

Examples:

$$
r=0.90\rightarrow\text{strong positive}
$$

$$
r=-0.80\rightarrow\text{strong negative}
$$

$$
r\approx0\rightarrow\text{little/no linear correlation}
$$

**Important:** \(r\) measures **linear** association. A strong curved relationship can still have \(r\approx0\).

---

## Correlation ≠ Causation

$$
\boxed{
\text{Correlation}\neq\text{Causation}
}
$$

Correlation only shows that variables are **associated**.

It does not prove:

- \(A\) causes \(B\)
- \(B\) causes \(A\)
- a third variable does not cause both

Possible explanations:

$$
A\rightarrow B
$$

$$
B\rightarrow A
$$

$$
C\rightarrow A,\quad C\rightarrow B
$$

**Observational studies** can show association but do not automatically establish causation.

---

# Residuals

### Predicted vs Actual

$$
\boxed{y=\text{actual}}
$$

$$
\boxed{\hat y=\text{predicted}}
$$

### Residual

$$
\boxed{
\text{Residual}=y-\hat y
}
$$

**Actual − Predicted**

- Positive residual → actual point **above** regression line
- Negative residual → actual point **below** regression line
- Zero residual → point **on** regression line

$$
\boxed{
y>\hat y\rightarrow\text{positive residual}
}
$$

$$
\boxed{
y<\hat y\rightarrow\text{negative residual}
}
$$

Magnitude tells how far the prediction was off.

---

## Least-Squares Regression

The least-squares regression line minimizes the **sum of squared residuals**:

$$
\boxed{
\sum(y-\hat y)^2
}
$$

Squaring prevents positive and negative residuals from canceling.

$$
\boxed{
\text{Least squares}
\rightarrow
\min\sum(y-\hat y)^2
}
$$

---

## Residual Plots

A residual plot uses:

$$
\boxed{
(x,\text{residual})
}
$$

- Horizontal axis → \(x\)
- Vertical axis → residual
- Horizontal axis → residual \(=0\)

### Good Residual Plot

$$
\boxed{
\text{Random scatter around }0
\rightarrow
\text{linear model is appropriate}
}
$$

### Bad Residual Plot

$$
\boxed{
\text{Clear pattern/curve}
\rightarrow
\text{linear model may not be appropriate}
}
$$

**Memory:**

> Random residuals = good  
> Patterned residuals = problem

Large \(|\text{residual}|\) → actual value is far from prediction.

---

# Covariance

### Deviation from the Mean

For each observation:

$$
\boxed{x_i-\bar x}
$$

$$
\boxed{y_i-\bar y}
$$

**Do not confuse with residuals:**

$$
\boxed{y_i-\hat y_i=\text{residual}}
$$

$$
\boxed{y_i-\bar y=\text{deviation from mean}}
$$

---

### Joint Deviation

$$
\boxed{
(x_i-\bar x)(y_i-\bar y)
}
$$

Sign logic:

- \((+)(+)=+\)
- \((-)(-)=+\)
- \((+)(-)=-\)
- \((-)(+)=-\)

Therefore:

$$
\boxed{
\text{Positive product}\rightarrow\text{same direction}
}
$$

$$
\boxed{
\text{Negative product}\rightarrow\text{opposite directions}
}
$$

---

### Sample Covariance

$$
\boxed{
s_{XY}
=
\frac{1}{n-1}
\sum_{i=1}^{n}
(x_i-\bar x)(y_i-\bar y)
}
$$

- Positive covariance → variables tend to move together
- Negative covariance → variables tend to move oppositely
- Near \(0\) → little linear joint variation

Covariance depends on the units of the variables, so its magnitude is difficult to compare directly.

---

# Correlation from Covariance

### Sample Correlation

$$
\boxed{
r=
\frac{s_{XY}}{s_Xs_Y}
}
$$

Conceptually:

$$
\boxed{
\text{Correlation}
=
\frac{\text{Covariance}}
{\text{SD of }X\times\text{SD of }Y}
}
$$

Correlation is **unitless** and standardized:

$$
\boxed{-1\le r\le1}
$$

### Big Picture

$$
\boxed{
\text{Deviation from mean}
\rightarrow
\text{Joint deviation}
\rightarrow
\text{Covariance}
\rightarrow
\text{Correlation}
}
$$

---

## SD vs Covariance vs Correlation

| Concept                | What it tells you                                                  |
| ---------------------- | ------------------------------------------------------------------ |
| **Standard deviation** | Spread of **one** variable                                         |
| **Covariance**         | How **two** variables vary together                                |
| **Correlation**        | Standardized **strength + direction** of their linear relationship |

Key distinction:

$$
\boxed{
\text{SD}\rightarrow\text{one variable}
}
$$

$$
\boxed{
\text{Covariance}\rightarrow\text{two variables moving together}
}
$$

$$
\boxed{
r\rightarrow\text{linear strength + direction}
}
$$

# Study Design & Sampling

## Bias in Surveys

| Bias | What happens? | Memory |
|---|---|---|
| **Voluntary response** | People choose themselves to participate | **Choose themselves** |
| **Convenience** | People chosen because they are easy to reach | **Easy to reach** |
| **Nonresponse** | Selected people do not respond | **Selected → don't answer** |
| **Response bias** | People give inaccurate/influenced answers | **Problem with answers** |
| **Undercoverage** | Part of the population cannot be selected | **Who's missing?** |

### Quick Identification

$$
\boxed{\text{People choose themselves}\rightarrow\text{Voluntary response}}
$$

$$
\boxed{\text{Easy to reach}\rightarrow\text{Convenience}}
$$

$$
\boxed{\text{Selected but don't answer}\rightarrow\text{Nonresponse}}
$$

$$
\boxed{\text{Inaccurate/influenced answers}\rightarrow\text{Response bias}}
$$

$$
\boxed{\text{Part of population cannot be selected}\rightarrow\text{Undercoverage}}
$$

**Key distinction:**

$$
\boxed{\text{Who gets selected?}\rightarrow\text{Sampling problem}}
$$

$$
\boxed{\text{Who responds?}\rightarrow\text{Nonresponse}}
$$

$$
\boxed{\text{What answers are given?}\rightarrow\text{Response bias}}
$$

---

## Sampling Methods

### Simple Random Sample (SRS)

Randomly select individuals from the entire population.

$$
\boxed{\text{Number everyone}\rightarrow\text{randomize}\rightarrow\text{select}}
$$

Every population member has an equal chance of selection.

**Without replacement:** an individual cannot be selected twice.

---

### Stratified Sample

Divide population into **strata** based on an important characteristic, then randomly sample **from every group**.

$$
\boxed{\text{Groups}\rightarrow\text{sample from EACH group}}
$$

**Memory:** **Stratified = some from every group**

---

### Cluster Sample

Divide population into **clusters**, randomly select clusters, then survey **everyone in selected clusters**.

$$
\boxed{\text{Randomly select groups}\rightarrow\text{survey everyone}}
$$

**Memory:** **Cluster = whole groups**

---

### Systematic Random Sample

Choose a **random starting point**, then select every \(k\)th individual.

$$
\boxed{\text{Random start}+\text{fixed interval}}
$$

Example:

\[
37,\ 137,\ 237,\ 337,\ldots
\]

Watch for population patterns that match the sampling interval.

---

### Sampling Method Comparison

| Method | Main idea |
|---|---|
| **Simple random** | Random individuals |
| **Stratified** | Some from **every** group |
| **Cluster** | **Whole** randomly selected groups |
| **Systematic** | Random start + every \(k\)th |
| **Voluntary** | People choose themselves |
| **Convenience** | Easiest people to reach |

---

# Experimental Design

## Variables

**Explanatory variable:**

$$
\boxed{\text{Variable that may explain/cause a change}}
$$

**Response variable:**

$$
\boxed{\text{Outcome being measured}}
$$

**Memory:** Explanatory → Response

---

## Random Sampling vs Random Assignment

### Random Sampling

$$
\boxed{\text{WHO gets studied?}}
$$

Helps with:

$$
\boxed{\text{Generalizability}}
$$

### Random Assignment

$$
\boxed{\text{WHO gets WHICH treatment?}}
$$

Helps with:

$$
\boxed{\text{Causation}}
$$

### Highest-Yield Rule

$$
\boxed{\text{Random sampling}\rightarrow\text{generalize}}
$$

$$
\boxed{\text{Random assignment}\rightarrow\text{causation}}
$$

---

## Treatment & Control

**Treatment group:** receives the treatment being tested.

**Control group:** comparison group that does not receive the active treatment.

---

## Placebo

A treatment with no active ingredient that resembles the real treatment.

$$
\boxed{\text{Placebo}\rightarrow\text{controls for placebo effect}}
$$

---

## Blinding

**Blind:**

$$
\boxed{\text{Participants don't know their treatment}}
$$

**Double-blind:**

$$
\boxed{\text{Participants + experiment administrators don't know}}
$$

Reduces psychological/researcher bias.

---

## Block Design

Group participants according to an important characteristic, then randomly assign **within each block**.

$$
\boxed{\text{Block by characteristic}\rightarrow\text{randomize within blocks}}
$$

**Memory:** **Block = group similar people, then randomize**

---

## Matched Pairs Design

Each participant receives **both conditions**; each person acts as their own comparison.

$$
\boxed{\text{Same person}\rightarrow\text{both conditions}}
$$

Reduces effects of individual differences.

**Memory:** **Matched pairs = same person, both treatments**

---

## Replication

Repeat an experiment with different participants/settings.

$$
\boxed{\text{Replication}\rightarrow\text{greater confidence in results}}
$$

---

# Correlation & Causation

$$
\boxed{\text{Correlation}\neq\text{Causation}}
$$

Correlation shows **association**, not necessarily cause.

Possible explanations:

$$
A\rightarrow B
$$

$$
B\rightarrow A
$$

$$
C\rightarrow A,\qquad C\rightarrow B
$$

where \(C\) may be a **confounding/lurking variable**.

**Observational study:**

$$
\boxed{\text{Association}\quad\text{(not automatically causation)}}
$$

**Randomized experiment:**

$$
\boxed{\text{Random assignment}\rightarrow\text{stronger causal evidence}}
$$

---

# Confounding Variables

A **confounding variable** is an outside variable related to both the explanatory and response variables, making the causal effect difficult to isolate.

$$
\boxed{
C\rightarrow A,\qquad C\rightarrow B
}
$$

Self-selection can create confounding:

$$
\boxed{\text{Self-selection}\rightarrow\text{possible confounding}}
$$

Without random assignment:

$$
\boxed{\text{Association}\not\Rightarrow\text{Causation}}
$$

---

# Statistical Significance

Statistical significance asks whether an observed result is unlikely to have occurred by chance alone.

$$
\boxed{\text{Rare by chance}\rightarrow\text{statistically significant}}
$$

### Simulation

$$
\boxed{
p\approx
\frac{\#\text{ simulations at least as extreme}}
{\#\text{ total simulations}}
}
$$

### Common Significance Level

$$
\boxed{p<0.05\rightarrow\text{statistically significant}}
$$

$$
\boxed{p\geq0.05\rightarrow\text{not statistically significant}}
$$

**Statistical significance does NOT necessarily mean:**

- effect is large
- effect is practically important
- result is guaranteed true

It means the observed result would be **unusual if there were no real effect**.

---

# Study Design Quick Decision Guide

| Question | Answer |
|---|---|
| People choose themselves? | **Voluntary response** |
| People chosen because easy to reach? | **Convenience** |
| Selected people don't respond? | **Nonresponse** |
| Answers inaccurate/influenced? | **Response bias** |
| Part of population can't be selected? | **Undercoverage** |
| Random individuals? | **Simple random** |
| Sample from every group? | **Stratified** |
| Random groups → everyone in them? | **Cluster** |
| Random start → every \(k\)th? | **Systematic** |
| Group by characteristic → randomize? | **Block** |
| Same person gets both conditions? | **Matched pairs** |
| Participants don't know treatment? | **Blind** |
| Participants + administrators don't know? | **Double-blind** |
| Random sampling? | **Generalizability** |
| Random assignment? | **Causation** |
| \(p<0.05\)? | **Statistically significant** |

### Master Memory

$$
\boxed{\text{Sampling}=\text{WHO is studied?}}
$$

$$
\boxed{\text{Assignment}=\text{WHO gets WHICH treatment?}}
$$

$$
\boxed{\text{Sampling}\rightarrow\text{Generalizability}}
$$

$$
\boxed{\text{Random assignment}\rightarrow\text{Causation}}
$$

$$
\boxed{\text{Correlation}\neq\text{Causation}}
$$

$$
\boxed{\text{Rare by chance}\rightarrow\text{Significant}}
$$