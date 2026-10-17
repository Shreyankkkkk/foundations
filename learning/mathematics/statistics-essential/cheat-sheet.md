# Statistics & Probability — Cheat Sheet

> Personal foundations notes (Mechatronics Engineering, self-study track toward quantitative finance).
> Based on in-class material (MATH141/142) + Khan Academy Statistics course, rewritten and reorganized in my own words as a reference, not a reproduction of course text.

---

## 1. Descriptive Statistics

### Mean

$$\bar{x} = \dfrac{\sum_{i=1}^{n}x_i}{n}$$

### Interquartile Range

$$IQR = Q_3 - Q_1$$

### Outlier Rule (1.5×IQR)

$$\text{Lower fence} = Q_1 - 1.5(IQR) \qquad \text{Upper fence} = Q_3 + 1.5(IQR)$$

Any point outside $[Q_1-1.5\,IQR,\ Q_3+1.5\,IQR]$ is flagged as an outlier.

---

## 2. Variability

### Population Variance / SD

$$\sigma^2 = \dfrac{\sum_{i=1}^{N}(x_i-\mu)^2}{N} \qquad \sigma = \sqrt{\sigma^2}$$

### Sample Variance

$$
s^2_{\text{biased (MLE)}} = \dfrac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n}
\qquad\qquad
s^2_{\text{unbiased}} = \dfrac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}
$$

- The $n-1$ version applies **Bessel's correction** — it corrects for the fact that $\bar x$ is estimated from the same data, which makes deviations from $\bar x$ systematically smaller than deviations from the true $\mu$.
- The $n-1$ version is **the standard used in practice** (this is what every stats package computes as "sample variance").

### Sample Standard Deviation — important subtlety

$$s = \sqrt{\dfrac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}$$

This is the conventional sample SD, but **note it is still a biased estimator of $\sigma$**, even though it uses the unbiased variance. This is because $\mathbb{E}[\sqrt{X}] \neq \sqrt{\mathbb{E}[X]}$ (square root is a concave function — Jensen's inequality). There is no simple closed-form correction that makes $s$ exactly unbiased for $\sigma$ in general; in practice this bias is small and usually ignored.

### Notation

| Symbol | Meaning |
|---|---|
| $x_i$ | $i$-th observation |
| $n$ | Sample size |
| $N$ | Population size |
| $\bar{x}$ | Sample mean |
| $\mu$ | Population mean |
| $s^2,\ s$ | Sample variance / SD |
| $\sigma^2,\ \sigma$ | Population variance / SD |
| $Q_1, Q_2, Q_3$ | Quartiles ($Q_2$ = median) |
| $IQR$ | Interquartile range |

---

## 3. Percentiles & Z-Scores

### Percentile Rank

$$\text{Percentile Rank}=\dfrac{\text{values below }x}{N}\times100$$

Use "at or below" instead of "below" if the problem specifies it — always check.

### Z-score

$$z=\dfrac{x-\mu}{\sigma}$$

- $z>0$: above the mean; $z<0$: below the mean; $z=0$: at the mean.
- Z-scores are **unitless**, which is exactly why they're used to compare values across different distributions:

$$z_1=\dfrac{x_1-\mu_1}{\sigma_1}, \qquad z_2=\dfrac{x_2-\mu_2}{\sigma_2}$$

---

## 4. Normal Distribution

### Empirical Rule (68–95–99.7)

| Distance from mean | Within | Each tail |
|---|---:|---:|
| $1\sigma$ | $68\%$ | $16\%$ |
| $2\sigma$ | $95\%$ | $2.5\%$ |
| $3\sigma$ | $99.7\%$ | $0.15\%$ |

### Normal Distribution Calculations

$$P(X<x)=P(Z<z) \qquad P(X>x)=1-P(Z<z)$$

$$P(a<X<b)=P(Z<z_b)-P(Z<z_a)$$

**Finding a value from a percentile:**

$$x=\mu+z\sigma$$

- Top $p\%$: solve for $z$ where $P(X<x)=1-p$, then $x=\mu+z\sigma$.
- Bottom $p\%$: solve for $z$ where $P(X<x)=p$, then $x=\mu+z\sigma$.

### Quick Decision Guide

| Question asks for... | Method |
|---|---|
| Below $x$ | $z$ → z-table |
| Above $x$ | $z$ → z-table → $1-\text{area}$ |
| Between $a,b$ | Two z-scores → subtract areas |
| Top $p\%$ | $1-p$ → find $z$ → find $x$ |
| Bottom $p\%$ | $p$ → find $z$ → find $x$ |

---

## 5. Bivariate Data, Regression & Residuals

### Scatterplots

Always describe: **Direction + Strength + Form + Outliers.**

### Regression Equation

$$\hat y=mx+b$$

- Slope: for every 1-unit increase in $x$, predicted $y$ changes by $m$ units.
- Intercept: when $x=0$, model predicts $y=b$ (only meaningful if $x=0$ is within/near the observed range).

### Interpolation vs Extrapolation

- **Interpolation** — estimating within the observed data range (generally safe).
- **Extrapolation** — estimating outside the observed range (assumes the trend continues; riskier).

### Residuals

$$\text{Residual}=y-\hat y \quad (\text{actual} - \text{predicted})$$

- Positive → point above the line; negative → below the line.
- **Least-squares regression** minimizes $\sum(y-\hat y)^2$ (squaring avoids positive/negative residuals cancelling, and penalizes large errors more).
- **Residual plot:** random scatter around 0 → linear model is appropriate; clear pattern/curve → linear model is probably wrong.

### Covariance

$$s_{XY}=\dfrac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar x)(y_i-\bar y)$$

Don't confuse deviation-from-mean ($y_i-\bar y$) with a residual ($y_i-\hat y_i$) — covariance is built from the former.

- Covariance's sign tells direction; its **magnitude is not comparable across variables** because it carries the units of $X\times Y$.

### Correlation Coefficient

$$r=\dfrac{s_{XY}}{s_X s_Y}, \qquad -1\le r\le1$$

- Sign → direction, $|r|$ → strength of the **linear** relationship only. A strong curved (nonlinear) relationship can still give $r\approx 0$.
- $r$ is standardized (unitless), which is what makes it comparable across different datasets — covariance alone isn't.
- Calibration: $r=0.90\to$ strong positive, $r=-0.80\to$ strong negative, $r\approx0\to$ little/no linear correlation.
- A regression line should represent the **overall linear trend** — don't discard inconvenient points just to force a tighter fit; that's cherry-picking, not modeling.

### Covariance — sign logic

$$s_{XY}=\dfrac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar x)(y_i-\bar y)$$

Each term is a **joint deviation** $(x_i-\bar x)(y_i-\bar y)$:

$$(+)(+)=+\qquad(-)(-)=+\qquad(+)(-)=-\qquad(-)(+)=-$$

Positive product → that point moved in the *same* direction on both variables; negative product → *opposite* directions. Averaging these products (with the $n-1$ correction) gives the sign and rough tendency of the relationship — but not a standardized magnitude, which is why correlation exists:

$$\text{Deviation from mean} \to \text{Joint deviation} \to \text{Covariance} \to \text{Correlation}$$

| Concept | Tells you |
|---|---|
| SD | Spread of **one** variable |
| Covariance | How **two** variables vary together (unit-dependent) |
| Correlation | Standardized strength + direction of the **linear** relationship |

---

## 6. Study Design & Sampling

### Bias Types

| Bias | What happens |
|---|---|
| Voluntary response | People choose themselves to participate |
| Convenience | Chosen because easy to reach |
| Nonresponse | Selected people don't respond |
| Response bias | Answers are inaccurate/influenced |
| Undercoverage | Part of the population can't be selected |

### Sampling Methods

| Method | Idea |
|---|---|
| Simple random (SRS) | Every individual has equal chance |
| Stratified | Sample from **every** subgroup |
| Cluster | Randomly select **whole groups**, survey everyone in them |
| Systematic | Random start + every $k$-th individual |

SRS is typically done **without replacement** — once an individual is selected, they can't be selected again.

### Quick Reverse-Lookup

| Question | Answer |
|---|---|
| People choose themselves? | Voluntary response |
| Chosen because easy to reach? | Convenience |
| Selected people don't respond? | Nonresponse |
| Answers inaccurate/influenced? | Response bias |
| Part of population can't be selected? | Undercoverage |
| Random individuals? | Simple random |
| Sample from every group? | Stratified |
| Random groups → everyone in them? | Cluster |
| Random start → every $k$-th? | Systematic |
| Group by characteristic → randomize within? | Block |
| Same person gets both conditions? | Matched pairs |
| Participants don't know treatment? | Blind |
| Participants + administrators don't know? | Double-blind |
| Random sampling gives you...? | Generalizability |
| Random assignment gives you...? | Causal evidence |
| $p<0.05$? | Statistically significant |

---

## 7. Experimental Design

- **Explanatory variable** → possible cause; **Response variable** → outcome measured.
- **Random sampling** → supports generalizability (who gets studied).
- **Random assignment** → supports causal claims (who gets which treatment).
- **Treatment group** → receives the treatment being tested; **control group** → comparison group that does not receive the active treatment.
- **Placebo** → controls for the placebo effect.
- **Blind** → participants don't know their treatment; **double-blind** → participants *and* administrators don't know.
- **Block design** → group by a known characteristic, then randomize *within* each block.
- **Matched pairs** → each subject receives both conditions (own comparison), reducing individual-difference noise.
- **Replication** → repeating the experiment increases confidence in the result.

---

## 8. Correlation, Causation & Confounding

$$\text{Correlation} \neq \text{Causation}$$

For an observed association between $A$ and $B$, three general explanations exist:

$$A \rightarrow B \qquad B \rightarrow A \qquad C \rightarrow A,\ C \rightarrow B$$

- $C$ is a **confounding (lurking) variable**: related to both $A$ and $B$, making the true causal effect hard to isolate. Self-selection is a common source of confounding.
- **Observational studies** → association only, not automatically causation.
- **Randomized experiments** (with random assignment) → much stronger evidence for causation, since confounders are balanced across groups on average.

---

## 9. Statistical Significance

Asks whether an observed result is unlikely to have occurred **by chance alone**.

- Common threshold: $p<0.05 \Rightarrow$ statistically significant.
- Estimated via simulation: repeatedly reshuffle/resample the data under the assumption of "no real effect," and count how often a result at least as extreme as the observed one occurs.

$$p \approx \dfrac{\text{simulated results at least as extreme}}{\text{total simulations}}$$

**What significance does *not* mean:**
- Does not mean the effect is large or practically important.
- Does not guarantee the result is true — it means the result would be unusual under the "no effect" assumption.
- Significance + random assignment together give the strongest case for a real, causal effect.

---

## 10. Probability Fundamentals

### Equally Likely Outcomes

$$P(\text{event})=\dfrac{\text{favorable outcomes}}{\text{total outcomes}}$$

All outcome probabilities in a sample space must sum to 1: $\sum P(\text{all outcomes}) = 1$.

### Addition Rule (Union)

$$P(A\cup B)=P(A)+P(B)-P(A\cap B)$$

The overlap $P(A\cap B)$ is subtracted because it's counted twice when $P(A)$ and $P(B)$ are added separately (visualize with a Venn diagram).

- **Mutually exclusive events** ($A\cap B = \varnothing$, i.e. they cannot both occur): $P(A\cap B)=0$, so the rule simplifies to

$$P(A\cup B)=P(A)+P(B)$$

### Independence

Two events are **independent** if knowing one occurred gives no information about the other:

$$P(A\cap B)=P(A)P(B) \iff P(A\mid B)=P(A) \iff P(B\mid A)=P(B)$$

**Multiple events** $E_1,\dots,E_n$ are (mutually) independent only if *every* subset satisfies the product rule — this is stronger than every pair being independent (pairwise independence does not imply mutual independence).

**Gambler's fallacy:** the false belief that past independent outcomes (e.g. a coin landing heads 5 times running) change the probability of the next outcome. They don't — each independent trial keeps its own fixed probability.

### Conditional Probability

$$P(B\mid A)=\dfrac{P(A\cap B)}{P(A)}$$

Read "$\mid$" as **"given that."**

### General Multiplication Rule

$$P(A\cap B)=P(A)\,P(B\mid A)$$

For more than two events:

$$P(E_1\cap E_2\cap\cdots\cap E_n)=P(E_1)\,P(E_2\mid E_1)\,P(E_3\mid E_1\cap E_2)\cdots P(E_n\mid E_1\cap\cdots\cap E_{n-1})$$

**Independent case** (conditioning drops out): $P(B\mid A)=P(B) \Rightarrow P(A\cap B)=P(A)P(B)$.

**Dependent case** (typically arises from sampling *without replacement*, since removing an item changes the composition of what's left): $P(B\mid A)\neq P(B)$.

| | With replacement | Without replacement |
|---|---|---|
| Typical result | Independent | Usually dependent |

**Testing independence with data:** compute $P(B)$ and $P(B\mid A)$ from observed frequencies. If they differ meaningfully, the events are (empirically) dependent. Frequencies computed this way are *experimental* probabilities, estimating the underlying *theoretical* ones.

### Law of Total Probability

Splitting event $E$ into cases based on whether $F$ occurred ($E = (E\cap F)\cup(E\cap F^c)$, mutually exclusive):

$$P(E)=P(E\mid F)P(F)+P(E\mid F^c)P(F^c)$$

More generally, for mutually exclusive $F_1,\dots,F_n$ whose union is the entire sample space:

$$P(E)=\sum_{i=1}^{n}P(E\mid F_i)P(F_i)$$

### Bayes' Theorem

$$P(F\mid E)=\dfrac{P(E\mid F)P(F)}{P(E)}=\dfrac{P(E\mid F)P(F)}{P(E\mid F)P(F)+P(E\mid F^c)P(F^c)}$$

General form over a partition $F_1,\dots,F_n$:

$$P(F_j\mid E)=\dfrac{P(E\mid F_j)P(F_j)}{\sum_{i=1}^{n}P(E\mid F_i)P(F_i)}$$

**Interpretation:**

$$\text{Posterior} \propto \text{Likelihood} \times \text{Prior}, \qquad P(F)\ (\text{prior}) \ \longrightarrow\ P(F\mid E)\ (\text{posterior})$$

Note in general $P(E\mid F)\neq P(F\mid E)$ — Bayes' theorem is exactly the bridge between the two directions of conditioning.

**Odds form:**

$$\text{Odds of } H = \dfrac{P(H)}{P(H^c)} \qquad\qquad \dfrac{P(H\mid E)}{P(H^c\mid E)}=\dfrac{P(H)}{P(H^c)}\cdot\dfrac{P(E\mid H)}{P(E\mid H^c)}$$

i.e. **Posterior odds = Prior odds × Evidence (likelihood) ratio.**

**Worked pattern — screening test example** (base-rate/prevalence effect): if a condition is rare, even a test with a low false-positive rate can produce more false positives than true positives among all *positive* results. This is why $P(\text{condition}\mid \text{positive test})$ can be far below the test's raw sensitivity — always weight by prevalence, not just by the test's error rates:

$$P(\text{condition}\mid\text{positive})=\dfrac{\text{true positives}}{\text{true positives}+\text{false positives}}$$

### Logical chain (how these results connect)

$$\text{Conditional probability} \to \text{Multiplication rule} \to \text{Law of total probability} \to \text{Bayes' theorem}$$

and independence is exactly the special case where conditioning changes nothing: $P(E\mid F)=P(E)$.

---

## 11. Combinatorics

### Factorial

$$n! = n(n-1)(n-2)\cdots 2\cdot 1, \qquad 0! = 1 \ (\text{by definition, so that } P(n,n)=n!/0!=n! \text{ stays consistent})$$

### Permutations (order matters)

Choosing/arranging $r$ items from $n$, **without repetition**:

$$P(n,r)=\dfrac{n!}{(n-r)!} = n(n-1)(n-2)\cdots(n-r+1)$$

- With repetition allowed (e.g. $r$-letter strings from an $n$-letter alphabet): $n^r$.
- Decision rule: *can the same item be reused?* Yes → same base each slot ($n^r$). No → shrinking base each slot ($P(n,r)$).

### Combinations (order doesn't matter)

$$\binom{n}{k}=\dfrac{n!}{k!(n-k)!} = \dfrac{P(n,k)}{k!}$$

Every group of $k$ chosen items can be internally arranged in $k!$ ways, all of which count as the *same* combination — hence dividing the permutation count by $k!$.

| | Permutation | Combination |
|---|---|---|
| Order matters? | Yes | No |
| Formula | $\dfrac{n!}{(n-r)!}$ | $\dfrac{n!}{k!(n-k)!}$ |
| Typical cue | distinct roles/positions (president/VP/secretary, arranging a code) | a group/hand/selection (committee, lottery numbers, card hand) |

### Probability via Counting

$$P(\text{event})=\dfrac{\text{favorable outcomes}}{\text{total outcomes}}$$

**Exactly $k$ successes among $n$ independent binary trials** (e.g. coin flips): choose which $k$ of the $n$ trial-positions are successes — order of the *positions chosen* doesn't matter, so use a combination:

$$P(\text{exactly }k\text{ successes})=\dfrac{\binom{n}{k}}{2^n} \quad (\text{fair binary trial case; general case uses the binomial distribution})$$

**One specific favorable combination out of all equally likely combinations** (lottery, dealt hand, correctly guessing an unordered group):

$$P(\text{specific outcome})=\dfrac{1}{\binom{n}{k}}$$

**One specific favorable permutation out of all equally likely assignments** (assigning distinct roles):

$$P(\text{specific assignment})=\dfrac{1}{P(n,r)}$$

**Probability a particular item is included in a random selection of $k$ from $n$:**

$$P(\text{item included})=\dfrac{\binom{n-1}{k-1}}{\binom{n}{k}}=\dfrac{k}{n}$$

**Combining multiple simultaneous conditions** (e.g. exactly 2 aces *and* exactly 2 kings from a deck in a 4-card draw): multiply the favorable combination counts for each condition, divide by the total combinations:

$$P=\dfrac{\binom{n_1}{k_1}\binom{n_2}{k_2}}{\binom{N}{k_1+k_2}}$$

---

## 12. Simulation, Experimental vs Theoretical Probability

### Theoretical vs Experimental

- **Theoretical probability** — predicted by the model (e.g. $P(\text{Heads})=0.5$ for a fair coin).
- **Experimental probability** — observed proportion from actual trials: $P(\text{event})\approx \dfrac{\text{occurrences}}{\text{trials}}$.

### Law of Large Numbers

As the number of independent trials increases, experimental probability tends to converge toward the theoretical probability. This does **not** mean short-run streaks/runs (e.g. 10 heads in a row) can't happen, or that outcomes must "balance out" — it means their effect on the *overall proportion* shrinks as $n$ grows, because each additional trial carries proportionally less weight.

### Simulation as a Tool

A simulation imitates a random process (e.g. using random digit tables or a computer RNG) to estimate probabilities or expected values without exhaustively enumerating outcomes or running the real experiment. Reliability of the estimate improves with more trials — this is the same Law of Large Numbers idea applied to estimating an average or a probability.

Simulation is also the practical method used in **§9 (Statistical Significance)** to estimate how extreme an observed result is relative to pure chance, by resampling/reshuffling under a null (no-effect) assumption.

---

## 13. Random Variables & Probability Distributions

### Random Variable

A **random variable** assigns a numerical value to the outcome of a random experiment. It's **discrete** if it takes only countable/separate values (e.g. $0,1,2,3$) — never values like $0.5$ or $\pi$.

### Validity of a Discrete Probability Distribution

$$P(X)\geq 0 \text{ for every value of } X \qquad\qquad \sum P(X) = 1$$

Both conditions are required — a set of "reasonable-looking" probabilities that sum to $0.8$ or $1.2$ is **not** a valid distribution.

### Constructing a Distribution from a Sample Space

List the equally likely outcomes → group them by the value of the random variable → divide each group's count by the total:

$$P(X=x)=\dfrac{\text{outcomes producing }x}{\text{total equally likely outcomes}}$$

When a value of $X$ can arise from independent trials in multiple distinct ways (e.g. "exactly one success in two independent tries" = success-then-fail **or** fail-then-success):

$$\text{Multiply probabilities within a scenario, add probabilities across different scenarios}$$

### Missing Probability & Cumulative Events

$$P(X=x_{\text{missing}}) = 1 - \sum(\text{known probabilities})$$

$$P(X\geq k) = \sum_{x\geq k}P(X=x) = 1-P(X<k)$$

The complement form is usually faster than summing directly.

### Empirical vs Theoretical Distributions

- **Theoretical** — derived from a model or counting argument.
- **Empirical** — estimated from observed data:

$$P(X=x)\approx\dfrac{\text{observations with }X=x}{\text{total observations}}$$

More observed data → more reliable estimate (same Law of Large Numbers idea from §12, applied to a whole distribution rather than a single probability).

### Fair Decisions

A probability-based procedure is **fair** only if every outcome/person has an **equal** probability of being selected. Count the favorable outcomes for each party directly and compare — a procedure can look random while still being unfair if the counts aren't equal.

---

## 14. Expected Value

### Definition

$$\mu = E(X) = \sum x\,P(X=x)$$

The probability-weighted average of all possible outcomes — **not** the most likely single outcome, and it can land on a non-integer value even when every individual outcome of $X$ is an integer.

### Interpretation

$E(X)$ describes the **long-run average over many repetitions**, not a guaranteed or even attainable result on any single trial.

### Expected Payoff / Net Gain

Always separate return from net gain:

$$\text{Net gain} = \text{Return (payout)} - \text{Cost} \qquad\qquad E(\text{net gain}) = \sum(\text{net gain})\times P(\text{outcome})$$

A large possible loss can still coexist with a **positive** expected value if that loss is sufficiently unlikely (insurance/protection-plan case) — and a small-looking negative expected value per unit scales linearly with volume (e.g. $-\$0.55$ per lottery ticket $\to -\$5{,}500$ over 10,000 tickets).

---

## Master Formula Reference

$$z=\dfrac{x-\mu}{\sigma} \qquad x=\mu+z\sigma$$

$$P(A\cup B)=P(A)+P(B)-P(A\cap B)$$

$$P(A\cap B)=P(A)P(B\mid A) \qquad \text{[independent]}\ \ P(A\cap B)=P(A)P(B)$$

$$P(B\mid A)=\dfrac{P(A\cap B)}{P(A)}$$

$$P(F\mid E)=\dfrac{P(E\mid F)P(F)}{\sum_i P(E\mid F_i)P(F_i)} \quad \text{(Bayes)}$$

$$P(n,r)=\dfrac{n!}{(n-r)!} \qquad \binom{n}{k}=\dfrac{n!}{k!(n-k)!}$$

$$r=\dfrac{s_{XY}}{s_Xs_Y} \qquad \text{Residual}=y-\hat y \qquad \text{Least squares} \to \min\sum(y-\hat y)^2$$

$$\text{Random sampling}\to\text{Generalizability} \qquad \text{Random assignment}\to\text{Causation}$$

$$p<0.05 \to \text{statistically significant} \qquad \text{Law of Large Numbers}\to\text{experimental}\to\text{theoretical}$$

$$E(X)=\sum xP(X=x) \qquad \text{Net gain}=\text{Return}-\text{Cost}$$

---

*Source note: originally derived from personal coursework and Khan Academy's Statistics course (khanacademy.org/math/probability), rewritten as independent study notes for my own reference — not official course material.*
