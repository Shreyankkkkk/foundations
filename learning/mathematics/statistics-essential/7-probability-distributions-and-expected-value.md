# Source and attribution

These are my personal study notes based on the Khan Academy Statistics course.

- Course: Statistics
- Provider: Khan Academy
- Source: https://www.khanacademy.org/math/probability
- Copyright: © 2025 Khan Academy. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Khan Academy course materials.

# Probability distributions introduction

## Lesson 1 : Constructing a probability distribution for random variable

### Random Variable

A **random variable** is a variable whose value depends on the outcome of a random experiment.

Example:

> Let $X$ = number of heads obtained when flipping a fair coin 3 times.

Possible values of $X$:

$$
\boxed{X=0,1,2,3}
$$

---

### All Possible Outcomes

Three coin flips have:

$$
2^3=8
$$

equally likely outcomes:

$$
HHH,\ HHT,\ HTH,\ HTT,\ THH,\ THT,\ TTH,\ TTT
$$

Now group these outcomes by the number of heads.

| $X$ | Number of heads | Probability |
|---:|---:|---:|
| 0 | 0 heads | $\dfrac18$ |
| 1 | 1 head | $\dfrac38$ |
| 2 | 2 heads | $\dfrac38$ |
| 3 | 3 heads | $\dfrac18$ |

The probabilities add to 1:

$$
\dfrac18+\dfrac38+\dfrac38+\dfrac18=1
$$

---

### Probability Distribution

A **probability distribution** shows the probabilities associated with the possible values of a random variable.

For $X$:

$$
\boxed{P(X=0)=\dfrac18,\quadP(X=1)=\dfrac38,\quadP(X=2)=\dfrac38,\quadP(X=3)=\dfrac18}
$$

We can visualize the distribution with a bar graph:

- $X=0$ → height $\dfrac18$
- $X=1$ → height $\dfrac38$
- $X=2$ → height $\dfrac38$
- $X=3$ → height $\dfrac18$

---

### Discrete Probability Distribution

This is a **discrete probability distribution** because $X$ can only take specific, separate values:

$$
\boxed{0,\ 1,\ 2,\ 3}
$$

It cannot take values such as:

$$
0.5,\quad \pi,\quad 1.7
$$

> **Discrete = separate/countable possible values.**

---

### Key Takeaways

> A **random variable** assigns a numerical value to a random outcome.

> A **probability distribution** tells us the probability of each possible value.

> For 3 fair coin flips, the number of heads can only be $0,1,2,$ or $3$.

$$
\boxed{\text{All probabilities in a distribution add to }1}
$$

### Memory Trick

> **Random variable = what we measure.**

> **Probability distribution = how likely each value is.**

> **Discrete = separate possible values.**

### Video

[Probability distribution example: number of heads after 3 coin flips](https://www.youtube.com/watch?v=cqK3uRoPtk0)

---

## Lesson 2 : Valid Discrete Probability Distribution Examples

### Valid Probability Distribution

A **discrete probability distribution** is valid when:

1. Every probability is **non-negative**:

$$
\boxed{P(X)\geq0}
$$

2. All probabilities add up to exactly **1** (100%):

$$
\boxed{\sum P(X)=1}
$$

A probability distribution cannot have a total greater than 1 or less than 1.

---

### Example: Free Throws

Suppose the probabilities are:

| Outcome | Probability |
|---|---:|
| Miss both | $0.2$ |
| Make exactly one | $0.5$ |
| Make both | $0.1$ |

All probabilities are positive, but:

$$
0.2+0.5+0.1=0.8
$$

Since:

$$
0.8\neq1
$$

this is **not a valid probability distribution**.

> The probabilities must account for **all possible outcomes**.

---

### Constructing a Probability Distribution

Suppose a sample contains:

- 97 chickens
- 47 cows
- 77 humans

Total:

$$
97+47+77=221
$$

Since every creature is equally likely to be selected:

$$
P(\text{chicken})=\dfrac{97}{221}
$$

$$
P(\text{cow})=\dfrac{47}{221}
$$

$$
P(\text{human})=\dfrac{77}{221}
$$

Check:

$$
\dfrac{97}{221}+\dfrac{47}{221}+\dfrac{77}{221}=\dfrac{221}{221}=1
$$

Therefore, this **is a valid probability distribution**.

---

### Key Takeaways

> Every probability must be **non-negative**.

$$
\boxed{P(X)\geq0}
$$

> All probabilities must add to exactly **1**.

$$
\boxed{\sum P(X)=1}
$$

> If outcomes are equally likely, probability can be found by:

$$
\boxed{P(\text{type})=\dfrac{\text{number of that type}}{\text{total number}}}
$$

### Memory Trick

> **Valid distribution = no negative probabilities + total = 1.**

### Video

[Valid discrete probability distribution examples](https://www.youtube.com/watch?v=uXtxKxYl1Iw)

---

## Lesson 3 : Probability with Discrete Random Variable Example

### Discrete Random Variable

Let $X$ = number of baseball card packs Hugo buys.

He can buy at most **4 packs**, so:

$$
\boxed{X=1,2,3,4}
$$

The probability distribution is:

| $X$ | $P(X)$ |
|---:|---:|
| 1 | $0.2$ |
| 2 | $0.16$ |
| 3 | $0.128$ |
| 4 | $?$ |

---

### Finding a Missing Probability

All probabilities in a valid distribution must add to 1.

Therefore:

$$
P(X=4)=1-0.2-0.16-0.128
$$

$$
\boxed{P(X=4)=0.512}
$$

The relatively large probability makes sense because Hugo **must stop after 4 packs**, even if he hasn't found the card.

---

### Finding $P(X\geq2)$

The event $X\geq2$ means Hugo buys:

$$
2,\ 3,\text{ or }4\text{ packs}
$$

Therefore:

$$
P(X\geq2)=P(X=2)+P(X=3)+P(X=4)
$$

$$
=0.16+0.128+0.512
$$

$$
\boxed{P(X\geq2)=0.8}
$$

An easier method is to use the complement:

$$
P(X\geq2)=1-P(X=1)
$$

$$
=1-0.2=\boxed{0.8}
$$

---

### Important Idea: Stopping Rules

The probability of buying 4 packs includes **all situations where Hugo reaches the fourth pack**, including cases where he finds the card on the fourth pack **and** cases where he never finds it.

That's why:

$$
P(X=4)=0.512
$$

can be larger than the probability of finding the card specifically on the fourth pack.

---

### Key Takeaways

> A discrete random variable takes specific, countable values.

> All probabilities in its distribution must add to 1.

$$
\boxed{\sum P(X)=1}
$$

> For $X\geq2$, add the probabilities for $X=2,3,4$.

> Often, a complement is easier:

$$
\boxed{P(X\geq2)=1-P(X<2)}
$$

### Memory Trick

> **Greater than or equal to → include that value and everything above it.**

> **Missing probability → $1-$ all known probabilities.**

### Video

[Probability with discrete random variable example](https://www.youtube.com/watch?v=d2STHFVHGAg)

---

# Theoretical & empirical probability distributions

## Lesson 1 : Probability with Discrete Random Variables

### Random Variable

A **random variable** assigns a numerical value to the outcome of a random experiment.

Example:

> Roll two 3-sided dice and let $D$ be the **non-negative difference** between their values.

Possible values:

$$
\boxed{D=0,1,2}
$$

The difference is always calculated as:

$$
\boxed{D=|\text{die 1}-\text{die 2}|}
$$

---

### Sample Space

Each die can show $1,2,$ or $3$.

There are:

$$
3\times3=9
$$

equally likely outcomes.

| Die 1 \ Die 2 | 1 | 2 | 3 |
|---|---:|---:|---:|
| **1** | 0 | 1 | 2 |
| **2** | 1 | 0 | 1 |
| **3** | 2 | 1 | 0 |

Each cell represents the value of $D$.

---

### Constructing the Probability Distribution

Count how many of the 9 outcomes produce each difference.

**Difference $0$:**

There are 3 outcomes:

$$
(1,1),(2,2),(3,3)
$$

Therefore:

$$
P(D=0)=\dfrac39=\boxed{\dfrac13}
$$

**Difference $1$:**

There are 4 outcomes:

$$
(1,2),(2,1),(2,3),(3,2)
$$

Therefore:

$$
P(D=1)=\boxed{\dfrac49}
$$

**Difference $2$:**

There are 2 outcomes:

$$
(1,3),(3,1)
$$

Therefore:

$$
P(D=2)=\boxed{\dfrac29}
$$

So the theoretical probability distribution is:

| $D$ | $P(D)$ |
|---:|---:|
| 0 | $\dfrac13$ |
| 1 | $\dfrac49$ |
| 2 | $\dfrac29$ |

Check:

$$
\dfrac13+\dfrac49+\dfrac29=\dfrac39+\dfrac49+\dfrac29=\dfrac99=1
$$

---

### Key Takeaways

> Build the **sample space** first.

> Group outcomes according to the value of the random variable.

$$
\boxed{P(D=d)=\dfrac{\text{number of outcomes producing }d}{\text{total equally likely outcomes}}}
$$

> The probabilities must add to 1.

### Memory Trick

> **List outcomes → calculate $D$ → count each value → divide by total.**

### Video

[Probability distribution for rolling two dice](https://www.youtube.com/watch?v=hA8VmhkKEJo)

---

## Lesson 2 : Theoretical Probability Distribution Example: Multiplication

### Setup

Kai visits a restaurant **twice**.

Each visit has:

$$
P(\text{free dessert})=\dfrac15
$$

Therefore:

$$
P(\text{no dessert})=\dfrac45
$$

Let $X$ = number of free desserts Kai gets in the two visits.

Possible values:

$$
\boxed{X=0,1,2}
$$

---

### Multiplication Rule

The two visits are **independent**.

For independent events:

$$
\boxed{P(A\text{ and }B)=P(A)\times P(B)}
$$

---

### Finding Each Probability

#### $X=0$

Kai gets no dessert on either visit:

$$
P(X=0)=\dfrac45\times\dfrac45=\boxed{\dfrac{16}{25}}
$$

#### $X=1$

There are **two ways** to get exactly one dessert:

- No dessert, then dessert
- Dessert, then no dessert

Therefore:

$$
P(X=1)=\dfrac45\dfrac15+\dfrac15\dfrac45
$$

$$
=\dfrac4{25}+\dfrac4{25}=\boxed{\dfrac8{25}}
$$

#### $X=2$

Kai gets a dessert on both visits:

$$
P(X=2)=\dfrac15\times\dfrac15=\boxed{\dfrac1{25}}
$$

---

### Probability Distribution

| $X$ | $P(X)$ |
|---:|---:|
| 0 | $\dfrac{16}{25}$ |
| 1 | $\dfrac{8}{25}$ |
| 2 | $\dfrac{1}{25}$ |

Check:

$$
\dfrac{16}{25}+\dfrac8{25}+\dfrac1{25}=\dfrac{25}{25}=1
$$

So this is a valid probability distribution.

---

### Key Takeaways

> **Independent events:** multiply their probabilities.

$$
\boxed{P(A\text{ and }B)=P(A)P(B)}
$$

> If an event can happen in multiple ways, calculate each way and **add** the probabilities.

$$
\boxed{\text{Multiply within a scenario, add across scenarios}}
$$

### Memory Trick

> **AND → multiply.**

> **Different ways → add.**

### Video

[Theoretical probability distribution example: multiplication](https://www.youtube.com/watch?v=2jExPaoTrQE)

---

## Lesson 3 : Theoretical & Empirical Probability Distributions

### Empirical Probability Distribution

An **empirical probability distribution** is based on **observed data** rather than a theoretical model.

When the true probability is unknown, we can use past observations to estimate it:

$$
\boxed{P(X=x)\approx\dfrac{\text{number of observations with }X=x}{\text{total observations}}}
$$

---

### Example: Restaurant Appetizers

Jada recorded the number of appetizers in **500 past orders**.

Let $X$ = number of appetizers in a randomly selected order.

| Appetizers $X$ | Orders | Approx. $P(X)$ |
|---:|---:|---:|
| 0 | 40 | $\dfrac{40}{500}=\dfrac{2}{25}$ |
| 1 | 90 | $\dfrac{90}{500}=\dfrac{9}{50}$ |
| 2 | 160 | $\dfrac{160}{500}=\dfrac{8}{25}$ |
| 3 | 120 | $\dfrac{120}{500}=\dfrac{6}{25}$ |
| 4 | 50 | $\dfrac{50}{500}=\dfrac{1}{10}$ |
| 5 | 30 | $\dfrac{30}{500}=\dfrac{3}{50}$ |
| 6 | 10 | $\dfrac{10}{500}=\dfrac{1}{50}$ |

These probabilities approximate the probability of each possible value of $X$.

---

### Why "Approximate"?

The data comes from only **500 observed orders**.

We don't know the exact underlying probability of each outcome, so the observed proportions are used as estimates.

$$
\boxed{\text{Observed data}\rightarrow\text{estimated probabilities}}
$$

This is different from a **theoretical probability distribution**, which comes from a mathematical model.

---

### Key Takeaways

> **Empirical probability** uses observed data.

$$
\boxed{P(X=x)\approx\dfrac{\text{frequency of }x}{\text{total observations}}}
$$

> The resulting distribution is an **approximation** of the underlying probabilities.

> More observed data can generally provide a more reliable estimate.

### Memory Trick

> **Empirical = observed.**

> **Count it → divide by total → estimate probability.**

### Video

[Probability distributions from empirical data](https://www.youtube.com/watch?v=wztjEa7893c)

---

# Decisions with probability

## Lesson 1 : Decisions with Probability

### Fair Decisions

A probability-based decision is **fair** when each person has the **same probability of being selected**.

Example:

- Roberto dusts if the dice sum to $7$.
- Jocelyn dusts if the dice sum to $10$ or $11$.
- Otherwise, roll again.

---

### Counting the Outcomes

Two fair six-sided dice have:

$$
6\times6=36
$$

equally likely outcomes.

#### Roberto: Sum of 7

There are **6** ways to roll a sum of 7:

$$
(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)
$$

Therefore:

$$
P(\text{Roberto})=\dfrac6{36}=\boxed{\dfrac16}
$$

#### Jocelyn: Sum of 10 or 11

There are:

- 3 ways to get 10
- 2 ways to get 11

So:

$$
3+2=5
$$

Therefore:

$$
P(\text{Jocelyn})=\dfrac5{36}
$$

---

### Is It Fair?

Compare:

$$
\dfrac16=\dfrac6{36}
$$

with:

$$
\dfrac5{36}
$$

Since:

$$
\dfrac6{36}>\dfrac5{36}
$$

Roberto has a higher probability of being chosen on each roll.

If neither outcome occurs, they roll again, but the same probabilities remain.

Therefore:

$$
\boxed{\text{The decision is not fair}}
$$

Roberto is more likely to end up doing the dusting.

---

### Key Takeaways

> A probability-based decision is fair when the participants have **equal chances** of being selected.

> Count the equally likely outcomes leading to each person's selection.

$$
\boxed{\text{Equal probabilities}\rightarrow\text{fair decision}}
$$

$$
\boxed{\text{Unequal probabilities}\rightarrow\text{unfair decision}}
$$

### Memory Trick

> **Fair = equal chance.**

> **Count favorable outcomes → compare probabilities.**

### Video

[Using probabilities to make fair decisions](https://www.youtube.com/watch?v=Z_5f3kys52o)

---

# Expected value

## Lesson 1: Mean (Expected Value) of a Discrete Random Variable

### Expected Value

The **expected value** (or **mean**) is the weighted average of all possible outcomes, using their probabilities.

It is commonly written as:

$$
\boxed{\mu=E(X)=\sum xP(X=x)}
$$

> **Outcome × probability, then add everything.**

---

### Example: Number of Workouts

Let $X$ = number of workouts in a week.

| $X$ | $P(X)$ |
|---:|---:|
| 0 | 0.10 |
| 1 | 0.15 |
| 2 | 0.40 |
| 3 | 0.25 |
| 4 | 0.10 |

Expected value:

$$
E(X)=0(0.10)+1(0.15)+2(0.40)+3(0.25)+4(0.10)
$$

$$
=0+0.15+0.80+0.75+0.40
$$

$$
\boxed{E(X)=2.1}
$$

---

### Interpreting 2.1

$2.1$ does **not** mean you literally do 2.1 workouts in a particular week.

It means that over a very large number of weeks, the **average number of workouts per week approaches 2.1**.

For example:

$$
10\text{ weeks}\rightarrow\text{roughly }21\text{ workouts}
$$

$$
100\text{ weeks}\rightarrow\text{roughly }210\text{ workouts}
$$

So a discrete random variable can have a **non-integer expected value**, even when its individual outcomes are integers.

---

### Key Takeaways

> **Expected value = weighted average of outcomes.**

$$
\boxed{E(X)=\sum xP(X=x)}
$$

> Multiply each outcome by its probability, then add.

> Expected value describes the **long-run average**, not necessarily an outcome that can occur in one trial.

### Memory Trick

> **Expected value = outcome × chance, added together.**

### Video

[Mean (expected value) of a discrete random variable](https://www.youtube.com/watch?v=qafPcWNUiM8)

---

## Lesson 2 : Interpreting Expected Value

### Expected Value

The **expected value** is the long-term average outcome of a random variable.

$$
\boxed{E(X)=\sum xP(X=x)}
$$

It does **not** mean the outcome you will most likely get on one trial.

---

### Example: Lottery Ticket

Suppose:

- Ticket costs: **$2**
- Expected return: **$0.95**

The expected return means:

> If many tickets were bought, the **average amount returned per ticket** would be about **$0.95**.

It does **not** mean:

- The probability of winning is $0.95$.
- You will most likely win exactly $0.95.
- You will receive $0.95 on every ticket.

The expected value is a **weighted average**, so rare large prizes can produce an expected return even when $0.95 is not an actual prize amount.

---

### Return vs. Net Gain

**Return** = money received from the ticket.

**Net gain** = return − cost.

For 1,000 tickets:

$$
1000(0.95)=\$950
$$

So the expected total **return** is:

$$
\boxed{\$950}
$$

But the tickets cost:

$$
1000(2)=\$2000
$$

Therefore expected net gain:

$$
950-2000=\boxed{-\$1050}
$$

So buyers would expect a **loss of $1,050**, not a gain.

---

### Key Takeaways

> **Expected value = long-term average outcome.**

> It does not predict what happens on one individual trial.

$$
\boxed{\text{Expected return} \neq \text{most likely return}}
$$

> Always distinguish **return** from **net gain**.

$$
\boxed{\text{Net gain}=\text{return}-\text{cost}}
$$

### Memory Trick

> **Expected value = "What would the average look like over many trials?"**

### Video

[Interpreting expected value: lottery ticket](https://www.youtube.com/watch?v=SNIW7MmCdhA)

---

## Lesson 3 : Expected Payoff Example: Lottery Ticket

### Expected Payoff

The **expected payoff** (or **expected net gain**) is the weighted average of all possible net gains.

$$
\boxed{E(X)=\sum xP(X=x)}
$$

The expected payoff **can be negative**.

---

### Example: Pick 4 Lottery

There are:

$$
10^4=10,000
$$

possible four-digit selections.

A $1 straight bet:

- Winning payout = **$4,500**
- Probability of winning = $\dfrac{1}{10,000}$
- Probability of losing = $\dfrac{9,999}{10,000}$

---

### Net Gain for Each Outcome

**Win:**

You pay $1 and receive $4,500:

$$
4500-1=\boxed{\$4,499}
$$

**Lose:**

You lose the $1 bet:

$$
\boxed{-\$1}
$$

---

### Expected Net Gain

Use the weighted average:

$$
E(X)=4499\left(\dfrac1{10000}\right)+(-1)\left(\dfrac{9999}{10000}\right)
$$

$$
=\dfrac{4499-9999}{10000}
$$

$$
=\dfrac{-5500}{10000}
$$

$$
\boxed{E(X)=-\$0.55}
$$

So, in the long run, the player expects to **lose about 55 cents per $1 bet**.

---

### Another Way to See It

Imagine buying **10,000 tickets**:

- Cost = $10,000
- Expected wins = 1
- Expected payout = $4,500

Therefore:

$$
4500-10000=\boxed{-\$5,500}
$$

Per ticket:

$$
\dfrac{-5500}{10000}=\boxed{-\$0.55}
$$

---

### Key Takeaways

> **Expected payoff = weighted average of net gains.**

> Always calculate **net gain**, not just the payout.

$$
\boxed{\text{Net gain}=\text{payout}-\text{cost}}
$$

> A negative expected payoff means you **expect to lose money in the long run**.

### Memory Trick

> **List outcomes → find net gain → find probability → multiply → add.**

### Video

[Expected payoff example: lottery ticket](https://www.youtube.com/watch?v=Ay1bVzqTKzg)

---

## Lesson 4 : Expected Payoff Example: Protection Plan

### Setup

A store sells a TV protection plan for **$80**.

- $2\%$ of customers need a replacement.
- Replacement costs the store **$1,200**.
- Let $X$ = store's **net gain** from one protection plan.

---

### Net Gain for Each Outcome

**Replacement needed:**

The store receives $80 but pays $1,200:

$$
80-1200=\boxed{-\$1,120}
$$

Probability:

$$
P(\text{replacement})=0.02
$$

**No replacement needed:**

The store keeps the $80:

$$
\boxed{\$80}
$$

Probability:

$$
P(\text{no replacement})=0.98
$$

---

### Expected Net Gain

Take the weighted average:

$$
E(X)=0.02(-1120)+0.98(80)
$$

$$
=-22.4+78.4
$$

$$
\boxed{E(X)=\$56}
$$

So the store expects to make **$56 per protection plan in the long run**.

---

### Key Takeaways

> Expected payoff is the **weighted average of all possible net gains**.

$$
\boxed{E(X)=\sum xP(X=x)}
$$

> A plan can have a large loss in one outcome but still have a **positive expected payoff** if that outcome is sufficiently unlikely.

### Memory Trick

> **Net gain × probability, for each outcome → add everything.**

### Video

[Expected payoff example: protection plan](https://www.youtube.com/watch?v=mKPeuVjPDo0)

---
