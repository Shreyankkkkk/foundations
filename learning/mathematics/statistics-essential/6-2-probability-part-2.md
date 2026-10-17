# Source and attribution

These are my personal study notes based on the Khan Academy Statistics course.

- Course: Statistics
- Provider: Khan Academy
- Source: https://www.khanacademy.org/math/probability
- Copyright: © 2025 Khan Academy. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Khan Academy course materials.

# Probability from Simulation

## Lesson 1 : Experimental vs. Theoretical Probability

### Theoretical Probability

**Theoretical probability** is the probability predicted by a mathematical model.

For a fair coin:

$$
\boxed{P(\text{Heads})=50\%}
$$

This assumes the coin is fair and each flip has a $50\%$ chance of heads.

---

### Experimental Probability

**Experimental probability** is based on what actually happens in repeated trials.

$$
\boxed{P(\text{event})\approx\dfrac{\text{number of times event occurs}}{\text{number of trials}}}
$$

For example, if a coin is flipped 10 times and heads occurs 7 times:

$$
P(\text{Heads})=\dfrac7{10}=70\%
$$

The experimental probability is different from the theoretical $50\%$, which is completely possible with a small number of trials.

---

### Law of Large Numbers

The **Law of Large Numbers** says that as the number of trials increases, the experimental probability tends to get closer to the theoretical probability.

$$
\boxed{\text{More trials}\rightarrow\text{experimental probability tends toward theoretical probability}}
$$

For a fair coin:

$$
\text{10 flips}\rightarrow\text{could be far from }50\%
$$

$$
\text{1,000+ flips}\rightarrow\text{typically much closer to }50\%
$$

This does **not** mean the experimental probability must get closer after every additional trial.

---

### Why Small Samples Vary More

With only a few trials, each outcome has a large effect on the proportion.

For example:

$$
1\text{ head out of }1=100\%
$$

but:

$$
500\text{ heads out of }1000=50\%
$$

A single additional result has much less effect when there are thousands of previous trials.

> **Memory:** More data makes individual random fluctuations matter less.

---

### Runs Don't Break the Law of Large Numbers

A fair coin can produce unusual runs:

$$
HHHHHHHHHH
$$

or:

$$
TTTTTTTTTT
$$

These runs are possible even after many previous flips.

The Law of Large Numbers does **not** mean the outcomes will alternate or become perfectly balanced.

Instead, over many trials, the **overall proportion** tends to stabilize near the theoretical probability.

$$\boxed{\text{Randomness remains}\quad+\quad\text{long-run proportion stabilizes}}$$

---

### Simulation

A **simulation** uses a model to imitate repeated random experiments.

For a fair coin simulation:

- Each flip has $P(H)=0.5$.
- The computer generates many simulated flips.
- We track the proportion of heads.
- As the number of flips increases, the proportion tends toward $50\%$.

A simulation helps us **see random variation and long-run behavior** without physically performing every trial.

---

### Key Takeaways

> **Theoretical probability** = what the mathematical model predicts.

> **Experimental probability** = what the observed trials produce.

> With few trials, experimental probability can differ substantially from theoretical probability.

> With many trials, experimental probability tends to approach theoretical probability.

$$\boxed{\text{Law of Large Numbers}\rightarrow\text{long-run experimental probability tends toward theoretical probability}}$$

> The probability of unusual fluctuations does not become zero; their effect on the overall proportion becomes smaller.

### Memory Trick

> **Few trials = noisy.**

> **Many trials = stabilizes.**

> **Long run → theoretical probability.**

### Video

[Experimental versus theoretical probability simulation](https://www.youtube.com/watch?v=Nos-xOCpQqg)

---

## Lesson 2 : Using a List of Random Numbers to Simulate Multiple Trials

### Simulation

A **simulation** uses random outcomes to imitate a real-world experiment.

Example: Each cereal box contains one of **6 equally likely prizes**.

Assign:

$$
1,2,3,4,5,6
$$

to the six prizes.

Random digits represent the prizes obtained from successive boxes.

---

### Running a Trial

For each experiment:

- Start at the next random number.
- **1–6** → valid prize; count the box.
- **0, 7, 8, 9** → ignore.
- Continue until all **6 prizes** have been collected.

Example results:

| Experiment | Boxes needed |
|---|---:|
| 1 | 8 |
| 2 | 17 |
| 3 | 10 |

The first experiment taking 8 boxes does **not** mean the expected number is 8.

---

### Estimating the Average

Run many independent trials and calculate their average:

$$\text{Experimental average}=\dfrac{\text{sum of results}}{\text{number of trials}}$$

For 3 trials:

$$
\dfrac{8+17+10}{3}=\dfrac{35}{3}=11\dfrac{2}{3}
$$

This is an **estimate**, not necessarily the true theoretical expected value.

As the number of trials increases, the experimental average is expected to get closer to the theoretical average.

$$
\boxed{\text{More trials}\rightarrow\text{more reliable estimate}}
$$

### Memory Trick

> **Random numbers → simulate trials → record results → average them.**

### Video

[Using a list of random numbers to simulate multiple trials of an experiment](https://www.youtube.com/watch?v=2AVLfSRpmfg)

---

## Lesson 3 : Using a List of Random Numbers to Calculate Experimental Probability

### Experimental Probability

**Experimental probability** is estimated by performing an experiment many times and finding the proportion of times an event occurs.

$$
\boxed{P(\text{event})\approx\dfrac{\text{number of successful trials}}{\text{total trials}}}
$$

---

### Example: Three Rolls to 10

Roll a fair six-sided die **3 times**.

- Sum $\geq 10$ → **Win**
- Sum $<10$ → **Lose**

To simulate the rolls using random digits:

$$
\boxed{1-6=\text{valid roll}}
$$

$$
\boxed{0,7,8,9=\text{ignore}}
$$

Each valid digit represents one die roll.

---

### Example Trials

| Experiment | Rolls | Sum | Result |
|---|---|---:|---|
| 1 | $1,5,6$ | 12 | Win |
| 2 | $6,2,4$ | 12 | Win |
| 3 | $6,3,2$ | 11 | Win |
| 4 | $1,2,5$ | 8 | Lose |
| 5 | $4,3,1$ | 8 | Lose |
| ... | ... | ... | ... |
| 10 | $5,2,6$ | 13 | Win |

After **10 experiments**, 5 were wins:

$$
P(\text{win})\approx\dfrac{5}{10}=50\%
$$

This is the **experimental probability** based on these 10 trials.

---

### Important

The experimental probability of **50%** does **not** mean the theoretical probability is exactly 50%.

With only a small number of trials, the estimate can differ significantly from the true probability.

Running more trials generally gives a more reliable approximation.

$$
\boxed{\text{More trials}\rightarrow\text{better estimate of theoretical probability}}
$$

### Memory Trick

> **Experimental probability = successes ÷ total trials.**

### Video

[Using a list of random number to calculate an experimental probability](https://www.youtube.com/watch?v=vjGINFbV8Cs)

---

## Lesson 4 : Statistical Significance

### Statistical Significance

**Statistical significance** asks whether an observed result is unlikely to have happened **by chance alone**.

Example:

- 500 children are randomly assigned to two groups.
- **Treatment:** food commercials.
- **Control:** non-food commercials.
- Children watching food commercials ate, on average, **10 grams more** crackers.

The question is:

$$
\boxed{\text{Could a 10-gram difference happen just by chance?}}
$$

---

### Simulating Random Chance

To investigate, the researchers:

1. Kept the same 500 children's results.
2. **Randomly reassigned** the results into two new groups.
3. Calculated the difference between the two group means.
4. Repeated this **150 times**.

This creates a distribution of differences that could occur **if there were no real treatment effect**.

> **Memory:** Randomly remix the results → see how often a difference this large appears.

---

### Interpreting the Simulation

The actual experiment found a difference of:

$$
10\text{ grams}
$$

A difference this large occurred only about **1 time out of 150** simulations.

$$
P(\text{difference this large by chance})\approx\dfrac{1}{150}\approx 0.67\%
$$

Since this is very small, the observed result is unlikely to be explained by random chance alone.

$$
\boxed{\text{Very unlikely by chance}\rightarrow\text{statistically significant}}
$$

---

### The 5% Threshold

A common threshold for statistical significance is **5%**.

$$
\boxed{P(\text{result by chance})<5\%\rightarrow\text{statistically significant}}
$$

Here:

$$
0.67\%<5\%
$$

so the result is statistically significant.

This gives evidence that watching food commercials **may have caused** the children to eat more crackers.

---

### Why Random Assignment Matters

The children were **randomly assigned** to the treatment and control groups.

Therefore, the experiment provides stronger evidence for a causal relationship.

$$
\boxed{\text{Random assignment}+\text{statistically significant result}\rightarrow\text{evidence of a treatment effect}}
$$

Statistical significance does **not** mean the result is guaranteed to be true. It means the result would be unusual if there were no real effect.

---

### Key Takeaways

> **Statistical significance** = the observed result is unlikely to be due to chance alone.

> A simulation can estimate how often a result this extreme occurs by chance.

> **Less than 5%** is a commonly used threshold.

$$
\boxed{\text{Small probability by chance}\rightarrow\text{statistically significant}}
$$

### Memory Trick

> **Rare by chance = significant.**

### Video

[Determining statistical significance](https://www.youtube.com/watch?v=jLFeqQxGtOc)

---

# Permutations

## Lesson 1 : Factorial and Counting Seat Arrangements

### Permutations

A **permutation** is an arrangement of objects where **order matters**.

Example: 3 people (A, B, C) sitting in 3 seats.

Possible arrangements include:

$$
ABC,\ ACB,\ BAC,\ BCA,\ CAB,\ CBA
$$

There are:

$$
\boxed{6\text{ arrangements}}
$$

---

### Counting Arrangements

For 3 people and 3 seats:

- **Seat 1:** 3 choices
- **Seat 2:** 2 remaining choices
- **Seat 3:** 1 remaining choice

Therefore:

$$
3\times2\times1=6
$$

In general, if $n$ objects are arranged in $n$ positions:

$$
\boxed{n!=n(n-1)(n-2)\cdots2(1)}
$$

The symbol $ ! $ means **factorial**.

---

### Example: 5 People in 5 Seats

With 5 people:

$$
5!=5\times4\times3\times2\times1
$$

$$
\boxed{5!=120}
$$

So there are **120 different arrangements**.

The reasoning:

$$
5\times4\times3\times2\times1
$$

because each occupied seat reduces the number of remaining choices by 1.

---

### Key Takeaways

> **Permutation = arrangement where order matters.**

> For $n$ objects in $n$ positions:

$$
\boxed{n!\text{ arrangements}}
$$

> Each position has one fewer choice than the previous position.

### Memory Trick

> **Arrange → order matters → factorial.**

### Video

[Factorial and counting seat arrangements](https://www.youtube.com/watch?v=eoxbgUIYhHo)

---

## Lesson 2 : Permutation Formula

### Permutations

A **permutation** counts arrangements where **order matters**.

If $n$ people are placed into $r$ seats:

$$
\boxed{P(n,r)=\dfrac{n!}{(n-r)!}}
$$

where:

- $n$ = total number of objects
- $r$ = number of positions being filled

---

### Example: 5 People, 3 Seats

There are 5 people and only 3 seats.

Think through the choices:

- Seat 1 → 5 choices
- Seat 2 → 4 choices
- Seat 3 → 3 choices

Therefore:

$$
5\times4\times3=60
$$

So:

$$
\boxed{P(5,3)=60}
$$

Using the formula:

$$
P(5,3)=\dfrac{5!}{(5-3)!}=\dfrac{5!}{2!}=\dfrac{120}{2}=60
$$

---

### Why the Formula Works

The factorial $5!$ is:

$$
5!=5\times4\times3\times2\times1
$$

But we only need:

$$
5\times4\times3
$$

So divide out the unused part:

$$
\dfrac{5!}{2!}=\dfrac{5\times4\times3\times2\times1}{2\times1}=5\times4\times3
$$

In general:

$$
\boxed{\dfrac{n!}{(n-r)!}}
$$

simply stops the factorial multiplication after $r$ choices.

---

### Reasoning Over Memorization

The formula is useful, but the underlying logic is more important:

> **Count the choices for each position and multiply them.**

For $n$ objects in $r$ positions:

$$
\boxed{n(n-1)(n-2)\cdots(n-r+1)}
$$

The factorial formula is just a compact way to write this.

### Key Takeaways

> **Permutation = order matters.**

> $n$ objects arranged in $r$ positions:

$$
\boxed{P(n,r)=\dfrac{n!}{(n-r)!}}
$$

> The denominator removes the factorial terms for positions that aren't being filled.

### Memory Trick

> **Permutation → positions matter → count choices one position at a time.**

### Video

[Permutation formula](https://www.youtube.com/watch?v=DROZVHObeko)

---

## Lesson 3 : Possible Three-Letter Words

### Repetition Allowed

Suppose the alphabet has **26 letters** and we want to create a 3-letter "word."

If letters can be repeated:

- 1st letter → 26 choices
- 2nd letter → 26 choices
- 3rd letter → 26 choices

Therefore:

$$
26\times26\times26=26^3
$$

$$
\boxed{26^3=17,576}
$$

Examples like $HHH$ are allowed.

> **Memory:** Repetition allowed → number of choices stays the same.

---

### Repetition Not Allowed

Now suppose all three letters must be different.

- 1st letter → 26 choices
- 2nd letter → 25 choices
- 3rd letter → 24 choices

Therefore:

$$
26\times25\times24
$$

$$
\boxed{15,600}
$$

This can also be written as a permutation:

$$
P(26,3)=\dfrac{26!}{(26-3)!}=\dfrac{26!}{23!}=26\times25\times24
$$

---

### The Important Distinction

Before using a formula, ask:

> **Can repetition occur?**

If **yes**:

$$
\boxed{26^3}
$$

If **no**:

$$
\boxed{26\times25\times24=P(26,3)}
$$

The number of available choices decreases only when a choice **cannot be reused**.

### Key Takeaways

> **Repetition allowed:** multiply the same number of choices each time.

> **No repetition:** each choice reduces the number of remaining possibilities.

$$
\boxed{\text{Repeat allowed}\rightarrow26^3}
$$

$$
\boxed{\text{No repeat}\rightarrow26P3=26\times25\times24}
$$

> Don't blindly apply permutations; first understand what the problem allows.

### Memory Trick

> **Can reuse? Same choices.**

> **Can't reuse? Choices decrease.**

### Video

[Possible three-letter words](https://www.youtube.com/watch?v=VYbqG2NuOo8)

---

## Lesson 4 : Zero Factorial or $0!$

### Factorial Review

For a positive integer $n$:

$$
\boxed{n!=n(n-1)(n-2)\cdots2(1)}
$$

Examples:

$$
3!=3\times2\times1=6
$$

$$
2!=2\times1=2
$$

$$
1!=1
$$

---

### What Is $0!$?

Mathematically:

$$
\boxed{0!=1}
$$

This is a **definition** chosen because it makes factorial-based formulas work consistently.

It may seem strange because there are no positive integers to multiply, but $0!$ is defined as $1$.

---

### Why Does $0!=1$ Matter for Permutations?

The permutation formula is:

$$
P(n,r)=\dfrac{n!}{(n-r)!}
$$

If we arrange **all $n$ objects** into $n$ positions:

$$
P(n,n)=\dfrac{n!}{(n-n)!}
$$

$$
=\dfrac{n!}{0!}
$$

We already know logically that arranging all $n$ objects gives:

$$
n!
$$

Therefore, we need:

$$
\dfrac{n!}{0!}=n!
$$

which works only when:

$$
\boxed{0!=1}
$$

---

### Key Takeaways

> $0!$ is **defined** to be $1$.

$$
\boxed{0!=1}
$$

> This makes formulas such as the permutation formula work consistently when all objects are being arranged.

$$
\boxed{P(n,n)=\dfrac{n!}{0!}=n!}
$$

### Memory Trick

> **Zero factorial = 1.**

> Think of $0!=1$ as a mathematical definition that keeps factorial formulas consistent.

### Video

[Zero factorial or 0!](https://www.youtube.com/watch?v=HGoZfzz6dU0)

---

## Lesson 5 : Ways to Arrange Colors

### Permutations with No Repetition

Suppose there are **6 colors** and we want to create a **4-color code**.

Conditions:

- Choose 4 colors from 6.
- Colors **cannot repeat**.
- **Order matters** because different arrangements are different codes.

For example:

$$
\text{Blue, Red, Yellow, Green}\neq\text{Green, Red, Yellow, Blue}
$$

Therefore, this is a **permutation** problem.

---

### Counting the Choices

There are 4 positions:

$$
\boxed{\_ \quad \_ \quad \_ \quad \_}
$$

For each position:

- 1st position → **6** choices
- 2nd position → **5** choices
- 3rd position → **4** choices
- 4th position → **3** choices

So:

$$
6\times5\times4\times3=360
$$

Therefore:

$$
\boxed{360\text{ possible codes}}
$$

---

### Using the Permutation Formula

The permutation formula is:

$$
P(n,r)=\dfrac{n!}{(n-r)!}
$$

Here:

$$
n=6,\qquad r=4
$$

Therefore:

$$
P(6,4)=\dfrac{6!}{(6-4)!}
$$

$$
=\dfrac{6!}{2!}
$$

$$
=6\times5\times4\times3
$$

$$
\boxed{=360}
$$

---

### Key Takeaway

> **No repetition + order matters → permutation.**

For 6 colors arranged into 4 positions:

$$
\boxed{P(6,4)=360}
$$

The core reasoning is simply:

$$
\boxed{6\times5\times4\times3}
$$

### Memory Trick

> **Each used color reduces the next number of choices.**

### Video

[Ways to arrange colors](https://www.youtube.com/watch?v=oQpKtm5TtxU)

---

## Lesson 6 : Ways to Pick Officers

### Officer Selection as a Permutation

A club has **9 people** and needs to choose:

- President
- Vice President
- Secretary

No person can hold more than one position.

Because the positions are **different**, who gets which position matters.

For example:

$$
\text{Alice = President, Bob = VP}\neq\text{Bob = President, Alice = VP}
$$

Therefore, this is a **permutation** problem.

---

### Counting the Choices

Choose the positions one at a time:

- President → **9** choices
- Vice President → **8** remaining choices
- Secretary → **7** remaining choices

Therefore:

$$
9\times8\times7=504
$$

So there are:

$$
\boxed{504\text{ possible boards}}
$$

---

### Using the Permutation Formula

There are 9 people and 3 positions:

$$
P(9,3)=\dfrac{9!}{(9-3)!}
$$

$$
=\dfrac{9!}{6!}
$$

$$
=9\times8\times7
$$

$$
\boxed{504}
$$

---

### Important Idea

The order of **selection** does not matter, but the **assignment of positions** does.

Whether you choose:

$$
\text{President}\rightarrow\text{VP}\rightarrow\text{Secretary}
$$

or:

$$
\text{Secretary}\rightarrow\text{VP}\rightarrow\text{President}
$$

you still get:

$$
9\times8\times7
$$

What matters is **who receives each office**.

### Key Takeaway

> **Different roles + no person can repeat → permutation.**

$$
\boxed{P(9,3)=504}
$$

### Memory Trick

> **Distinct positions → order matters → permutation.**

### Video

[Ways to pick officers](https://www.youtube.com/watch?v=v9NLtiVt3XY)

---

# Combinations

## Lesson 1 : Introduction

### Permutations vs. Combinations

Suppose there are **6 people** and **3 chairs**.

If we care about **who sits in which chair**, we are counting **permutations**.

$$
6\times5\times4=120
$$

$$
\boxed{120\text{ permutations}}
$$

For example:

$$
ABC,\ ACB,\ BAC,\ BCA,\ CAB,\ CBA
$$

are all different permutations because the positions differ.

---

### Combinations

If we only care about **which 3 people are chosen**, but **not their order**, we are counting **combinations**.

For example:

$$
ABC,\ ACB,\ BAC,\ BCA,\ CAB,\ CBA
$$

all represent the same combination:

$$
\boxed{\{A,B,C\}}
$$

---

### Why Divide by $3!$?

Every group of 3 people can be arranged in:

$$
3!=3\times2\times1=6
$$

different ways.

The 120 permutations therefore contain each 3-person group **6 times**.

So:

$$
\dfrac{120}{6}=20
$$

Therefore:

$$
\boxed{20\text{ combinations}}
$$

---

### The Core Difference

| | Permutation | Combination |
|---|---|---|
| **Order matters?** | Yes | No |
| **Example** | $ABC\neq BAC$ | $ABC=BAC$ |
| **6 people, choose 3** | $120$ | $20$ |

> **Permutation:** Which person goes in which position?

> **Combination:** Which people are chosen?

---

### Key Takeaway

A combination can be obtained from permutations by removing the different arrangements of the selected objects:

$$
\boxed{\text{Combinations}=\dfrac{\text{Permutations}}{\text{ways to arrange selected objects}}}
$$

For choosing 3 from 6:

$$
\boxed{\dfrac{6P3}{3!}=\dfrac{120}{6}=20}
$$

### Memory Trick

> **Permutation = position matters.**

> **Combination = group matters, position doesn't.**

### Video

[Permutations](https://www.youtube.com/watch?v=iKy-d5_erhI)

---

## Lesson 2 : Combination Formula

### Combinations

A **combination** counts selections where **order does not matter**.

If we have $n$ objects and choose $k$ of them:

$$
\boxed{\binom{n}{k}=\dfrac{n!}{k!(n-k)!}}
$$

This is also called **"n choose k"** or the **binomial coefficient**.

---

### Why Divide by $k!$?

First, count the **permutations**:

$$
P(n,k)=\dfrac{n!}{(n-k)!}
$$

But each group of $k$ objects can be arranged in:

$$
k!
$$

different ways.

Since combinations do **not** care about those arrangements:

$$
\boxed{\text{Combinations}=\dfrac{\text{Permutations}}{k!}}
$$

Therefore:

$$
\binom{n}{k}=\dfrac{n!}{k!(n-k)!}
$$

---

### Example: Choose 4 People from 6

Suppose 6 people are available and we want to choose 4.

If order matters:

$$
P(6,4)=6\times5\times4\times3=360
$$

But the same 4 people can be arranged in:

$$
4!=24
$$

ways.

Therefore:

$$
\binom64=\dfrac{360}{24}=15
$$

So:

$$
\boxed{\binom64=15}
$$

There are **15 different groups of 4 people**.

---

### Formula Example

Using the combination formula directly:

$$
\binom64=\dfrac{6!}{4!(6-4)!}
$$

$$
=\dfrac{6!}{4!2!}
$$

$$
=\dfrac{6\times5\times4\times3\times2\times1}{(4\times3\times2\times1)(2\times1)}
$$

$$
\boxed{=15}
$$

---

### Permutation vs. Combination

| | Permutation | Combination |
|---|---|---|
| **Order matters?** | Yes | No |
| **Formula** | $\dfrac{n!}{(n-k)!}$ | $\dfrac{n!}{k!(n-k)!}$ |
| **Meaning** | Arrange $k$ objects | Choose $k$ objects |

The extra $k!$ in the combination formula removes the different arrangements of the same selected group.

$$
\boxed{\text{Combination}=\dfrac{\text{Permutation}}{k!}
}
$$

### Key Takeaway

> **Permutation = arrange.**

> **Combination = choose.**

If changing the order creates a different result → **permutation**.

If changing the order does not create a different result → **combination**.

$$
\boxed{\binom nk=\dfrac{n!}{k!(n-k)!}}
$$

### Memory Trick

> **Combination = permutation ÷ arrangements of the chosen items.**

### Video

[Combination formula](https://www.youtube.com/watch?v=p8vIcmr_Pqo)

---

## Lesson 3 : Handshaking Combinations

### Handshakes as Combinations

Suppose there are **4 people**: $A,B,C,D$.

Each person shakes hands with every other person **exactly once**.

A handshake is simply a **selection of 2 people**.

Since:

$$
AB=BA
$$

the order does **not** matter.

Therefore, this is a **combination** problem.

---

### Counting with Permutations

If we temporarily care about order:

- First person → 4 choices
- Second person → 3 choices

$$
4\times3=12
$$

But this **double-counts** every handshake:

$$
AB\text{ and }BA
$$

are the same handshake.

Since 2 people can be arranged in:

$$
2!=2
$$

ways, divide by $2!$:

$$
\dfrac{4\times3}{2!}=\dfrac{12}{2}=6
$$

So:

$$
\boxed{6\text{ handshakes}}
$$

---

### Using the Combination Formula

A handshake chooses 2 people from 4:

$$
\binom42=\dfrac{4!}{2!(4-2)!}
$$

$$
=\dfrac{4!}{2!2!}=6
$$

Therefore:

$$
\boxed{\binom42=6}
$$

---

### The Six Handshakes

The unique pairs are:

$$
AB,\ AC,\ AD,\ BC,\ BD,\ CD
$$

Each pair appears only once.

---

### Key Takeaway

> A handshake between two people is a **combination of 2 people**, because $AB$ and $BA$ represent the same handshake.

$$
\boxed{\text{Handshakes among }n\text{ people}=\binom n2}
$$

### Memory Trick

> **Handshake = choose 2 people.**

> **Order doesn't matter → combination.**

### Video

[Handshaking combinations](https://www.youtube.com/watch?v=boH4l1SgJbM)

---

## Lesson 4 : Combination Example - 9 Card Hands

### Choosing a Hand

Suppose there are **36 unique cards** and we want to choose a hand of **9 cards**.

The order of cards in a hand **does not matter**.

For example:

$$
\{A,B,C,\ldots\}
$$

is the same hand regardless of how those cards are arranged.

Therefore, this is a **combination** problem.

---

### Counting as Permutations First

If order mattered, we could fill 9 positions:

- 1st card → 36 choices
- 2nd card → 35 choices
- 3rd card → 34 choices
- ...
- 9th card → 28 choices

So:

$$
36\times35\times34\times33\times32\times31\times30\times29\times28
$$

This counts **permutations**, because different orders are counted separately.

---

### Removing Overcounting

The same 9 cards can be arranged in:

$$
9!
$$

different orders.

Since the order of cards in a hand does not matter, divide by $9!$:

$$
\dfrac{36\times35\times\cdots\times28}{9!}
$$

Therefore:

$$
\boxed{94,143,280}
$$

There are **94,143,280 possible 9-card hands**.

---

### Using the Combination Formula

The combination formula is:

$$
\boxed{\binom nk=\dfrac{n!}{k!(n-k)!}}
$$

Here:

$$
n=36,\qquad k=9
$$

So:

$$
\binom{36}{9}=\dfrac{36!}{9!(36-9)!}
$$

$$
=\dfrac{36!}{9!27!}
$$

$$
\boxed{=94,143,280}
$$

---

### Why $27!$?

The $36!$ contains:

$$
36\times35\times\cdots\times28\times27\times\cdots\times1
$$

Dividing by $27!$ removes everything from $27$ down to $1$, leaving:

$$
36\times35\times\cdots\times28
$$

Then dividing by $9!$ removes the different arrangements of the same 9 cards.

---

### Key Takeaway

> A card hand is a **combination** because the order of the cards does not matter.

$$
\boxed{\text{9-card hands from 36}=\binom{36}{9}}
$$

$$
\boxed{\binom{36}{9}=94,143,280}
$$

### Memory Trick

> **Hand = choose cards, don't arrange cards → combination.**

> First count ordered selections, then divide by $9!$ to remove duplicate arrangements.

### Video

[Combination example: 9 card hands](https://www.youtube.com/watch?v=SbpoyXTpC84)

---

# Probability Using Combinations

## Lesson 1 : Probability Using Combinations

### Core Idea

When calculating probability, combinations are useful when:

> **Order does not matter, but we care about how many objects satisfy a condition.**

Example: Flip a fair coin **8 times** and find the probability of getting **exactly 3 heads**.

---

### Total Possible Outcomes

Each flip has 2 possible outcomes:

$$
H\text{ or }T
$$

For 8 flips:

$$
\boxed{2^8=256}
$$

So there are **256 equally likely outcomes**.

---

### Favorable Outcomes

We need exactly **3 heads** among the 8 flips.

This means:

> Choose which **3 of the 8 flip positions** will be heads.

Order doesn't matter when choosing the positions.

Therefore:

$$
\binom83
$$

Using the combination formula:

$$
\binom83=\dfrac{8!}{3!5!}
$$

$$
=\dfrac{8\times7\times6}{3\times2\times1}=56
$$

So there are:

$$
\boxed{56\text{ outcomes with exactly 3 heads}}
$$

---

### Probability

$$
P(\text{exactly 3 heads})=\dfrac{\text{favorable outcomes}}{\text{total outcomes}}
$$

$$
=\dfrac{\binom83}{2^8}
$$

$$
=\dfrac{56}{256}=\dfrac7{32}
$$

$$
\boxed{P(\text{exactly 3 heads})=\dfrac7{32}\approx21.875\%}
$$

---

### Why Combinations?

Suppose the heads occur on flips:

$$
1,2,3
$$

This is the same outcome as choosing the same three positions in a different order:

$$
3,2,1
$$

The **positions** are what matter, not the order in which we "choose" them.

Therefore, use a **combination**, not a permutation.

---

### General Pattern

For $n$ fair coin flips, the probability of getting exactly $k$ heads is:

$$
\boxed{P(\text{exactly }k\text{ heads})=\dfrac{\binom nk}{2^n}}
$$

The same idea can be extended to other probability problems where:

- There are equally likely outcomes.
- We need to choose which positions/items satisfy the condition.
- The order of selection does not matter.

### Key Takeaways

> **Total outcomes:** $2^n$ for $n$ fair coin flips.

> **Exactly $k$ heads:** choose $k$ positions from $n$.

$$
\boxed{\text{Favorable outcomes}=\binom nk}
$$

$$
\boxed{P(\text{exactly }k\text{ heads})=\dfrac{\binom nk}{2^n}}
$$

### Memory Trick

> **Choose the positions → combination.**

> **Probability = favorable ÷ total.**

### Video

[Probability using combinations](https://www.youtube.com/watch?v=Xqfcy1rqMbI)

---

## Lesson 2 : Lottery Probability

### Core Idea

A lottery asks you to choose **4 different numbers from 1–60**.

Since the winning numbers can appear in **any order**, order does **not** matter.

Therefore, use a **combination**:

$$
\binom{60}{4}
$$

---

### Total Possible Outcomes

Using the combination formula:

$$
\binom{60}{4}=\dfrac{60!}{4!(60-4)!}
$$

$$
=\dfrac{60!}{4!56!}
$$

$$
=\dfrac{60\times59\times58\times57}{4\times3\times2\times1}
$$

$$
\boxed{=487,635}
$$

So there are **487,635 possible groups of 4 numbers**.

---

### Probability of One Specific Combination

Suppose the winning numbers are:

$$
\{3,15,46,49\}
$$

This is **one specific combination** among the 487,635 possible combinations.

Therefore:

$$
P(\text{specific combination})=\dfrac{1}{487,635}
$$

$$
\boxed{P=\dfrac{1}{487,635}}
$$

Approximately:

$$
\boxed{0.00000205\approx0.000205\%}
$$

---

### Why Combinations?

If the winning numbers are:

$$
3,15,46,49
$$

then:

$$
3,15,46,49
$$

and

$$
49,46,15,3
$$

represent the **same lottery outcome**.

So we don't count different orders separately.

> **Order doesn't matter → combination.**

---

### General Pattern

If a lottery chooses $k$ numbers from $n$ numbers, with no repetition and order irrelevant:

$$
\boxed{\text{Total outcomes}=\binom nk}
$$

If exactly one combination wins:

$$
\boxed{P(\text{winning})=\dfrac{1}{\binom nk}}
$$

### Key Takeaways

> Lottery selections are usually **combinations** when order doesn't matter.

$$
\boxed{\text{Total possible selections}=\binom nk}
$$

> If only one selection wins, probability = **1 ÷ total selections**.

### Memory Trick

> **Lottery: choose numbers, don't arrange them → combination.**

### Video

[Example: Lottery probability](https://www.youtube.com/watch?v=DIjlllgq3dc)

---

## Lesson 3 : Probability with Permutations

### Core Idea

A club has **9 people** and chooses 3 officers:

- President
- Vice President
- Secretary

Because each position is **different**, who gets which position matters.

Therefore, this is a **permutation** problem.

---

### Total Possible Outcomes

Choose each position one at a time:

- President → 9 choices
- Vice President → 8 choices
- Secretary → 7 choices

$$
9\times8\times7=504
$$

So:

$$
\boxed{504\text{ possible officer assignments}}
$$

This is:

$$
P(9,3)=\dfrac{9!}{6!}=504
$$

---

### Probability of One Specific Assignment

Suppose we want exactly:

$$
\text{Marcia = President}
$$

$$
\text{Sabita = Vice President}
$$

$$
\text{Robert = Secretary}
$$

This is **one specific outcome** out of 504 possible assignments.

Therefore:

$$
P(\text{specific assignment})=\dfrac{1}{504}
$$

$$
\boxed{P=\dfrac1{504}\approx0.198\%}
$$

---

### Why Permutations?

Compare:

$$
\text{Marcia = President,\ Sabita = VP}
$$

with:

$$
\text{Sabita = President,\ Marcia = VP}
$$

These are **different outcomes** because the positions are different.

> **Different roles → order/assignment matters → permutation.**

---

### Key Takeaways

> When people are assigned to **distinct positions**, use permutations.

$$
\boxed{\text{Total outcomes}=P(n,k)}
$$

If one specific assignment is favorable:

$$
\boxed{P(\text{specific assignment})=\dfrac{1}{P(n,k)}}
$$

### Memory Trick

> **Different jobs = different outcomes → permutation.**

### Video

[Example: Different ways to pick officers](https://www.youtube.com/watch?v=l9ft9jpriNA)

---

## Lesson 4 : Probability with Permutations & Combinations

### Core Idea

Combinatorics can be used to calculate probabilities by counting:

$$
\boxed{P(\text{event})=\dfrac{\text{favorable outcomes}}{\text{total outcomes}}}
$$

The key question is:

> **Does order matter?**

- **Order matters → permutation**
- **Order does not matter → combination**

---

### Example: Olive Tasting

There are **15 distinct olive varieties**.

Samara chooses **3 different varieties** to make a blend.

The contestant only needs to identify **which 3 varieties** were used. The order does not matter.

Therefore:

$$
\boxed{\text{Total outcomes}=\binom{15}{3}}
$$

---

### Probability of a Correct Guess

The contestant randomly chooses one of the possible groups.

Only **1 combination** is correct.

Therefore:

$$
P(\text{correct})=\dfrac{1}{\binom{15}{3}}
$$

Calculate:

$$
\binom{15}{3}=\dfrac{15\times14\times13}{3!}
$$

$$
=\dfrac{15\times14\times13}{6}=455
$$

Therefore:

$$
\boxed{P(\text{correct})=\dfrac1{455}}
$$

Approximately:

$$
\boxed{0.22\%}
$$

---

### Why Not a Permutation?

The contestant does **not** need to guess the varieties in a particular order.

For example:

$$
A,B,C
$$

and

$$
C,A,B
$$

represent the same correct answer.

So:

$$
\boxed{\text{Order irrelevant}\rightarrow\text{combination}}
$$

If the contestant had to guess the varieties in a specific order, then a permutation would be appropriate.

---

### Key Takeaways

> **First decide whether order matters.**

$$
\boxed{\text{Order matters}\rightarrow P(n,k)}
$$

$$
\boxed{\text{Order doesn't matter}\rightarrow\binom nk}
$$

For one correct combination among all possible combinations:

$$
\boxed{P(\text{correct})=\dfrac1{\binom nk}}
$$

### Memory Trick

> **Guessing a group → combination.**

> **Guessing an arrangement → permutation.**

### Video

[Probability with permutations & combinations example: taste testing](https://www.youtube.com/watch?v=C6gQZ7qKtdM)

---

## Lesson 5 : Probability with Combinations - Choosing Groups

### Core Idea

When a group is chosen randomly and **order does not matter**, use combinations.

To find the probability that a specific person is included:

$$
\boxed{P(\text{person chosen})=\dfrac{\text{groups containing person}}{\text{total possible groups}}}
$$

---

### Example: Kyra's Conference Team

There are **13 people** on a team.

A manager randomly chooses **3 people**.

What is the probability that **Kyra** is chosen?

---

### Total Possible Groups

Choose 3 people from 13:

$$
\binom{13}{3}
$$

---

### Groups Containing Kyra

If Kyra is already included, we only need to choose the **other 2 people** from the remaining 12:

$$
\binom{12}{2}
$$

Therefore:

$$
P(\text{Kyra chosen})=\dfrac{\binom{12}{2}}{\binom{13}{3}}
$$

Calculate:

$$
\binom{12}{2}=66
$$

$$
\binom{13}{3}=286
$$

So:

$$
P=\dfrac{66}{286}=\boxed{\dfrac3{13}}
$$

Approximately:

$$
\boxed{23.1\%}
$$

---

### Why Two Combinations?

**Denominator:** all possible 3-person groups.

$$
\binom{13}{3}
$$

**Numerator:** only the groups that contain Kyra.

$$
\binom{12}{2}
$$

Kyra is already fixed in the group, so we choose the remaining 2 members from the other 12.

---

### Key Takeaways

> **Total groups:** choose the entire group from everyone.

> **Favorable groups:** fix the required person, then choose the remaining members.

$$
\boxed{P(\text{specific person included})=\dfrac{\binom{n-1}{k-1}}{\binom nk}}
$$

This simplifies to:

$$
\boxed{\dfrac{k}{n}}
$$

So for Kyra:

$$
\dfrac3{13}
$$

### Memory Trick

> **Person must be included → lock them in, then choose the rest.**

### Video

[Probability with combinations example: choosing groups](https://www.youtube.com/watch?v=gy8E0-wf4a0)

---

## Lesson 6 : Probability with Combinations - Drawing Two Aces and Two Kings

### Setup

A standard deck has:

- **4 aces**
- **4 kings**
- **44 other cards**
- **52 cards total**

Four cards are drawn **without replacement**.

We want the probability of getting **exactly 2 aces and 2 kings**, in any order.

---

### Total Possible Draws

Since the order of the 4 cards does **not** matter:

$$
\boxed{\text{Total outcomes}=\binom{52}{4}}
$$

---

### Favorable Draws

We need:

- 2 aces from 4:

$$
\binom42
$$

- 2 kings from 4:

$$
\binom42
$$

For every possible pair of aces, there are $\binom42$ possible pairs of kings, so multiply:

$$
\boxed{\text{Favorable outcomes}=\binom42\binom42}
$$

---

### Probability

Therefore:

$$
\boxed{P(2\text{ aces and }2\text{ kings})=\dfrac{\binom42\binom42}{\binom{52}{4}}}
$$

The order does not matter, so **combinations** are used.

---

### Key Takeaway

> When a probability problem asks for specific groups of objects and **order doesn't matter**, count the favorable groups and divide by all possible groups.

$$
\boxed{P=\dfrac{\text{favorable combinations}}{\text{total combinations}}}
$$

For this problem:

$$
\boxed{\dfrac{\binom42\binom42}{\binom{52}{4}}}
$$

### Memory Trick

> **Choose each required group separately → multiply → divide by total combinations.**

### Video

[Probability with combinations example: choosing cards](https://www.youtube.com/watch?v=Tp-SjgG11G8)

---

## Lesson 7 : Mega Millions Jackpot Probability

### Setup

Using the lottery setup from the video:

- **56** white balls → choose **5**
- **46** Mega Balls → choose **1**
- The 5 white-ball numbers can be in **any order**.

---

### White-Ball Combinations

Since order does **not** matter, use combinations:

$$
\binom{56}{5}
$$

Reasoning through permutations first:

$$
56\times55\times54\times53\times52
$$

Then divide by the ways to arrange 5 selected balls:

$$
5!=5\times4\times3\times2\times1
$$

So:

$$
\binom{56}{5}=\dfrac{56\times55\times54\times53\times52}{5!}
$$

$$
\boxed{3,819,816}
$$

---

### Include the Mega Ball

There are **46** possible Mega Balls.

Therefore:

$$
3,819,816\times46=175,711,536
$$

So there are:

$$
\boxed{175,711,536\text{ possible outcomes}}
$$

---

### Jackpot Probability

With one entry, only **one** of these outcomes wins:

$$
\boxed{P(\text{jackpot})=\dfrac{1}{175,711,536}}
$$

Approximately:

$$
\boxed{1\text{ in }175.7\text{ million}}
$$

---

### Key Takeaway

The 5 white balls use a **combination** because their order doesn't matter.

The Mega Ball is then an independent choice among 46 possibilities.

$$
\boxed{P=\dfrac{1}{\binom{56}{5}\times46}}
$$

> **Lottery probability = 1 ÷ total possible winning combinations.**

### Memory Trick

> **Choose the 5 unordered balls → multiply by the Mega Ball possibilities → take the reciprocal.**

### Video

[Probability of winning the Mega Millions jackpot](https://www.youtube.com/watch?v=gyqodNhM3EU)

---