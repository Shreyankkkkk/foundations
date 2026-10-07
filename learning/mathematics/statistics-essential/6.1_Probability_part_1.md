# Source and attribution

These are my personal study notes based on the Khan Academy Statistics course.

- Course: Statistics
- Provider: Khan Academy
- Source: https://www.khanacademy.org/math/probability
- Copyright: © 2025 Khan Academy. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Khan Academy course materials.

# Venn diagrams and the addition rule

## Lesson 1 : Venn Diagrams and the Addition Rule

### Standard Deck of Cards

A standard deck has:

- **4 suits:** spades, diamonds, clubs, hearts
- **13 ranks:** Ace through 10, Jack, Queen, King

$$
4\times13=52
$$

So there are **52 equally likely outcomes** when randomly drawing one card.

---

### Equally Likely Events

**Equally likely** means every possible outcome has the same chance of occurring.

For one randomly selected card:

$$
P(\text{event})=\dfrac{\text{favorable outcomes}}{\text{total outcomes}}
$$

---

### Basic Card Probabilities

**Probability of a Jack:**

There are 4 Jacks.

$$
P(J)=\dfrac{4}{52}=\dfrac{1}{13}
$$

**Probability of a Heart:**

There are 13 Hearts.

$$
P(H)=\dfrac{13}{52}=\dfrac14
$$

**Probability of a Jack AND a Heart:**

Only the Jack of Hearts satisfies both conditions.

$$
P(J\cap H)=\dfrac{1}{52}
$$

---

### Overlapping Events

Two events **overlap** when some outcomes belong to both events.

In this example:

- Event $J$ = drawing a Jack
- Event $H$ = drawing a Heart
- $J\cap H$ = drawing the Jack of Hearts

A **Venn diagram** shows this overlap visually.

> **Memory:** Intersection $A\cap B$ = **A AND B**.

---

### The Addition Rule

For the probability of **A OR B**, add the probabilities but subtract the overlap:

$$
\boxed{P(A\cup B)=P(A)+P(B)-P(A\cap B)}
$$

Why subtract?

Because the overlapping outcomes are counted **twice** when $P(A)$ and $P(B)$ are added.

---

### Example: Jack OR Heart

There are:

- 4 Jacks
- 13 Hearts
- 1 card that is both: Jack of Hearts

Therefore:

$$
P(J\cup H)=\dfrac{4+13-1}{52}
$$

$$
=\dfrac{16}{52}=\boxed{\dfrac4{13}}
$$

So the probability of drawing a **Jack or a Heart** is:

$$
\boxed{\dfrac4{13}}
$$

---

### Venn Diagram Idea

For two overlapping events:

$$
\boxed{\text{Total}=A+B-\text{overlap}}
$$

If the sets have sizes $A$, $B$, and intersection $C$:

$$
\boxed{A+B-C}
$$

> **Memory:** **Add both circles → subtract the overlap.**

---

### Key Takeaways

> **OR** → union $A\cup B$

> **AND** → intersection $A\cap B$

> **Overlapping events** share some outcomes.

> For overlapping events, **subtract the overlap** when using the addition rule.

$$
\boxed{P(A\cup B)=P(A)+P(B)-P(A\cap B)}
$$

### Memory Trick

> **OR = Add, then subtract the overlap.**

### Video

[Venn diagrams and the addition rule](https://www.youtube.com/watch?v=obZzOq_wSCg)

---

## Lesson 2 : Addition Rule for Probability

### Venn Diagrams and Probability

A **Venn diagram** shows sets of outcomes and how they overlap.

For two events:

- $A$ = outcomes satisfying condition A
- $B$ = outcomes satisfying condition B
- $A\cap B$ = outcomes satisfying **both**
- $A\cup B$ = outcomes satisfying **A or B**

> **Memory:** Inside both circles = **AND**. Inside either circle = **OR**.

---

### Example: Objects in a Bag

The bag contains:

- 8 green cubes
- 9 green spheres
- 5 yellow cubes
- 7 yellow spheres

Total:

$$
8+9+5+7=29
$$

So there are **29 equally likely outcomes**.

---

### Basic Probabilities

**Cube:**

$$
P(\text{cube})=\dfrac{8+5}{29}=\boxed{\dfrac{13}{29}}
$$

**Yellow:**

$$
P(\text{yellow})=\dfrac{5+7}{29}=\boxed{\dfrac{12}{29}}
$$

**Yellow AND cube:**

Only the 5 yellow cubes satisfy both.

$$
P(\text{yellow}\cap\text{cube})=\boxed{\dfrac5{29}}
$$

---

### Addition Rule

To find the probability of **A or B**:

$$
\boxed{P(A\cup B)=P(A)+P(B)-P(A\cap B)}
$$

The overlap must be subtracted because it gets counted **twice** when $P(A)$ and $P(B)$ are added.

---

### Example: Yellow OR Cube

$$
P(\text{yellow or cube})=\dfrac{12}{29}+\dfrac{13}{29}-\dfrac5{29}
$$

$$
=\dfrac{20}{29}
$$

Therefore:

$$
\boxed{P(\text{yellow or cube})=\dfrac{20}{29}}
$$

> **Memory:** Add both events → **subtract the overlap**.

---

### Mutually Exclusive Events

Two events are **mutually exclusive** if they **cannot happen at the same time**.

Therefore:

$$
P(A\cap B)=0
$$

and the addition rule becomes:

$$
\boxed{P(A\cup B)=P(A)+P(B)}
$$

**Example:** Drawing one card that is either a Heart or a Spade.

A single card cannot be both a Heart and a Spade, so these events are mutually exclusive.

---

### Key Takeaways

> **$A\cup B$** = A **OR** B.

> **$A\cap B$** = A **AND** B.

> **Overlapping events** share outcomes.

> **Mutually exclusive events** have no overlap.

$$
\boxed{P(A\cup B)=P(A)+P(B)-P(A\cap B)}
$$

### Memory Trick

> **OR = Add − Overlap**

If there is **no overlap**, nothing needs to be subtracted.

### Video

[Venn diagrams and the addition rule for probability](https://www.youtube.com/watch?v=QE2uR6Z-NcU)

---

# Multiplication Rule of Probability

## Lesson 1 : Probability of Independent Events

### Probability of a Single Event

For a fair coin:

$$
P(\text{Heads})=\dfrac12
$$

$$
P(\text{Tails})=\dfrac12
$$

The probabilities of **all possible outcomes** must add up to 1:

$$
\boxed{\sum P(\text{all possible outcomes})=1}
$$

> **Memory:** All possible outcomes together = 100%.

---

### Probability by Listing Outcomes

For two coin flips, the equally likely outcomes are:

$$
HH,\ HT,\ TH,\ TT
$$

There are **4** possible outcomes.

Only $HH$ satisfies "heads and heads":

$$
P(HH)=\dfrac14
$$

For three flips, there are:

$$
2^3=8
$$

equally likely outcomes.

Therefore, the probability of one exact sequence, such as $THT$, is:

$$
\boxed{P(THT)=\dfrac18}
$$

---

### Independent Events

Two events are **independent** if the outcome of one does not affect the probability of the other.

Coin flips are independent:

$$
\boxed{\text{Previous flips do not affect future flips}}
$$

For independent events:

$$
\boxed{P(A\text{ and }B)=P(A)\times P(B)}
$$

Example:

$$
P(HH)=P(H)\times P(H)=\dfrac12\times\dfrac12=\dfrac14
$$

For $THT$:

$$
P(THT)=\dfrac12\times\dfrac12\times\dfrac12=\dfrac18
$$

---

### Gambler's Fallacy

The **gambler's fallacy** is the incorrect belief that previous independent outcomes affect future probabilities.

Example:

If a fair coin lands heads 5 times in a row, some people think tails is now more likely.

Wrong:

$$
P(\text{Tails on next flip})=\dfrac12
$$

The previous flips do not change it.

> **Memory:** Independent = **the past doesn't change the odds**.

---

### Two Ways to Calculate Exact Sequences

**Method 1: List all equally likely outcomes**

$$
P(\text{event})=\dfrac{\text{favorable outcomes}}{\text{total outcomes}}
$$

**Method 2: Multiply independent probabilities**

$$
\boxed{P(A\text{ and }B)=P(A)P(B)}
$$

Both methods give the same answer.

---

### Key Takeaways

> **All possible probabilities add to 1.**

> **Independent events:** one outcome does not affect another.

> **Independent events → multiply probabilities.**

$$
\boxed{P(A\text{ and }B)=P(A)P(B)}
$$

> **Gambler's fallacy:** past independent outcomes do not change future probabilities.

### Memory Trick

> **Independent = multiply.**

> **Exact sequence = multiply each step.**

> **Fair coin:** each flip is always $P(H)=P(T)=\dfrac12$.

### Video

[Probability of independent events](https://www.youtube.com/watch?v=xSc4oLA9e8o)

---

## Lesson 2 : Compound Probability of Independent Events

### Independent Events

When two events are **independent**, the outcome of one does not affect the probability of the other.

For independent events:

$$
\boxed{P(A\text{ and }B)=P(A)\times P(B)}
$$

> **Memory:** Independent events → **multiply**.

---

### Example: Multiple Choice Test

Problem 1 has **4 choices**, with 1 correct answer.

$$
P(\text{correct on 1})=\dfrac14
$$

Problem 2 has **3 choices**, with 1 correct answer.

$$
P(\text{correct on 2})=\dfrac13
$$

The guesses are independent, so:

$$
P(\text{correct on both})=\dfrac14\times\dfrac13=\boxed{\dfrac1{12}}
$$

Therefore, there is a **1 in 12** chance of guessing both correctly.

---

### Why Multiplication Works

The total number of possible combined outcomes is:

$$
4\times3=12
$$

Only **1** outcome gives correct answers on both problems.

Therefore:

$$
P(\text{both correct})=\dfrac{1}{12}
$$

This matches the multiplication rule:

$$
\dfrac14\times\dfrac13=\dfrac1{12}
$$

---

### General Idea

If:

- Event $A$ has $m$ possible outcomes
- Event $B$ has $n$ possible outcomes

then the combined experiment has:

$$
\boxed{m\times n}
$$

possible outcomes, assuming the choices are independent.

For one specific combination:

$$
\boxed{
P(\text{specific combination})
=
P(A)\times P(B)
}
$$

---

### Key Takeaways

> **Independent events:** one event does not affect the other.

$$
\boxed{P(A\text{ and }B)=P(A)P(B)}
$$

> For multiple-choice guessing, if each problem has one correct answer, the probability of getting it correct is:

$$
\boxed{\dfrac{1}{\text{number of choices}}}
$$

> For multiple independent questions, multiply the individual probabilities.

### Memory Trick

> **Both + Independent → Multiply.**

### Video

[Independent events example: test taking](https://www.youtube.com/watch?v=VWAfEbgf1Po)

---

## Lesson 3 : General Multiplication Rule — Independent Events

### General Multiplication Rule

The general multiplication rule for two events is:

$$
\boxed{P(A\text{ and }B)=P(A)\times P(B\mid A)}
$$

where $P(B\mid A)$ means the probability of $B$ **given that $A$ occurred**.

If $A$ and $B$ are **independent**, then:

$$
P(B\mid A)=P(B)
$$

so:

$$
\boxed{P(A\text{ and }B)=P(A)\times P(B)}
$$

---

### Example: Maya and Doug

Maya and Doug each spin a wheel with **6 equally likely outcomes**.

- 1 outcome = silk
- 5 outcomes = not silk

Therefore:

$$
P(\text{Maya no silk})=\dfrac56
$$

Because Maya's spin does not affect Doug's spin:

$$
P(\text{Doug no silk}\mid\text{Maya no silk})=P(\text{Doug no silk})=\dfrac56
$$

Therefore:

$$
P(\text{neither gets silk})=\dfrac56\times\dfrac56=\boxed{\dfrac{25}{36}}
$$

---

### Why Are They Independent?

Maya spins first, but her result does **not remove or change** any option on Doug's wheel.

So:

$$
\boxed{\text{Maya's result does not affect Doug's probability}}
$$

Therefore, the events are independent.

> **Memory:** If the first event doesn't change the second event's odds → independent.

---

### Conditional Probability Connection

The expression:

$$
P(B\mid A)
$$

means:

> **Probability of $B$, given that $A$ happened.**

For independent events:

$$
\boxed{P(B\mid A)=P(B)}
$$

So the general rule simplifies to:

$$
\boxed{P(A\text{ and }B)=P(A)P(B)}
$$

---

### Quick Exam Strategy

For "neither" or "both" questions:

1. Translate the wording into events.
2. Find the probability of the first event.
3. Determine whether the second event is independent.
4. If independent, multiply.

Example:

$$
P(\text{no silk, no silk})=\dfrac56\cdot\dfrac56=\boxed{\dfrac{25}{36}}
$$

### Key Takeaways

> **General multiplication rule:**

$$
\boxed{P(A\text{ and }B)=P(A)P(B\mid A)}
$$

> **For independent events:**

$$
\boxed{P(A\text{ and }B)=P(A)P(B)}
$$

> **Independent:** the first event does not change the probability of the second.

### Memory Trick

> **General rule = multiply by conditional probability.**

> **Independent = conditional probability stays the same.**

### Video

[General multiplication rule example: independent events](https://www.youtube.com/watch?v=OqbkCYy37hI)

---

## Lesson 4 : Dependent Probability

### Dependent Events

Two events are **dependent** when the outcome of one event changes the probability of the other.

A common cause is **not replacing** an item after selecting it.

$$
\boxed{\text{Dependent}=\text{first event changes the odds of the second}}
$$

> **Memory:** Dependent = **the first event affects the second**.

---

### Example: Drawing Marbles Without Replacement

A bag contains:

- 3 green marbles
- 2 orange marbles

Total:

$$
5\text{ marbles}
$$

The goal is to draw **2 green marbles in a row**, without replacing the first marble.

---

### First Draw

There are 3 green marbles out of 5:

$$
P(\text{first green})=\dfrac35
$$

If the first marble is green, it is **removed** from the bag.

Now there are:

- 2 green marbles
- 2 orange marbles
- 4 total marbles

---

### Second Draw

The probability of green on the second draw **given that the first was green** is:

$$
P(\text{second green}\mid\text{first green})=\dfrac24=\dfrac12
$$

The vertical bar means **"given that."**

$$
\boxed{P(B\mid A)=\text{probability of B given A}}
$$

---

### General Multiplication Rule

For any two events:

$$
\boxed{P(A\text{ and }B)=P(A)\times P(B\mid A)}
$$

For the two green marbles:

$$
P(\text{green, green})=\dfrac35\times\dfrac24
$$

$$
=\dfrac35\times\dfrac12=\boxed{\dfrac3{10}}
$$

So there is a **30% probability** of drawing two green marbles.

---

### Why You Cannot Multiply $\dfrac35\times\dfrac35$

It might seem that:

$$
\dfrac35\times\dfrac35
$$

should work.

But after the first green marble is removed, the situation changes:

$$
\dfrac35\rightarrow\dfrac24
$$

The second probability is no longer $\dfrac35$.

Therefore, the events are **dependent**.

$$
\boxed{\text{Without replacement}\rightarrow\text{probabilities can change}\rightarrow\text{dependent}}
$$

---

### With vs. Without Replacement

**Without replacement:**

The selected item stays out.

$$
\boxed{\text{Usually dependent}}
$$

**With replacement:**

The selected item is returned, so the original probabilities remain unchanged.

$$
\boxed{\text{Usually independent}}
$$

For example, if the green marble were replaced after the first draw:

$$
P(\text{second green}\mid\text{first green})=\dfrac35
$$

instead of $\dfrac24$.

---

### Key Takeaways

> **Dependent events:** the first event changes the probability of the second.

> **"Given" $=\mid$**

$$
\boxed{
P(B\mid A)
=
\text{probability of B given A}
}
$$

> **General multiplication rule:**

$$
\boxed{
P(A\text{ and }B)
=
P(A)P(B\mid A)
}
$$

> **Without replacement** often creates dependence because the composition of the remaining items changes.

### Memory Trick

> **Independent:** odds stay the same.

> **Dependent:** odds change.

> **Without replacement → think dependent.**

### Video

[Dependent probability introduction](https://www.youtube.com/watch?v=VjLEoo3hIoM)

---

## Lesson 5 : General Multiplication Rule — Dependent Events

### Dependent Events

When the outcome of one event changes the probability of another event, the events are **dependent**.

For dependent events, use the general multiplication rule:

$$
\boxed{P(A\text{ and }B)=P(A)\times P(B\mid A)}
$$

The conditional probability $P(B\mid A)$ accounts for the fact that $A$ has already happened.

---

### Example: Drawing Cards Without Replacement

There are **6 cards**:

- 1 silk card
- 5 non-silk cards

Maya draws first, then Doug draws **without replacement**.

We want:

$$
P(\text{Maya no silk and Doug no silk})
$$

---

### Maya's Draw

There are 5 non-silk cards out of 6:

$$
P(\text{Maya no silk})=\dfrac56
$$

Because Maya does not replace her card, there are now only **5 cards remaining**.

If Maya drew a non-silk card:

- 1 silk card remains
- 4 non-silk cards remain

Therefore:

$$
P(\text{Doug no silk}\mid\text{Maya no silk})=\dfrac45
$$

---

### Applying the General Multiplication Rule

$$
P(\text{neither gets silk})=\dfrac56\times\dfrac45
$$

$$
=
\boxed{\dfrac23}
$$

So there is a **$2/3$** probability that neither contestant draws silk.

---

### Why the "Given" Matters

Doug's probability depends on Maya's result.

If Maya gets no silk, Doug has:

$$
\dfrac45
$$

chance of getting no silk.

If Maya had drawn silk, Doug would have:

$$
\dfrac55=1
$$

chance of getting no silk.

So Doug's probability changes depending on what Maya drew.

$$
\boxed{\text{Maya's result affects Doug's probability}\rightarrow\text{dependent events}}
$$

---

### Without Replacement Creates Dependence

When an item is removed, the composition of what remains changes.

$$
\boxed{\text{Without replacement}\rightarrow\text{remaining probabilities change}\rightarrow\text{dependent}}
$$

If Maya replaced her card before Doug drew, the probability would remain:

$$
P(\text{Doug no silk}\mid\text{Maya no silk})=\dfrac56
$$

and the events would be independent.

---

### Key Takeaways

> **Dependent events:** one event changes the probability of another.

> **General multiplication rule:**

$$
\boxed{P(A\text{ and }B)=P(A)P(B\mid A)}
$$

> **$P(B\mid A)$** means the probability of $B$ **given that $A$ occurred**.

> **Without replacement** often makes events dependent.

### Memory Trick

> **Independent:** multiply $P(A)P(B)$.

> **Dependent:** multiply $P(A)P(B\mid A)$.

The difference is whether the second probability **changes after the first event**.

### Video

[General multiplication rule example: dependent events](https://www.youtube.com/watch?v=iyQNk090FGM)

---

## Lesson 6 : Interpreting the General Multiplication Rule

### Event Notation

Probability problems often use symbols to represent events.

If $K_1$ means **contestant 1 gets kale**, then:

$$
K_1^C
$$

means the **complement** of $K_1$:

$$
\boxed{K_1^C=\text{contestant 1 does not get kale}}
$$

Similarly:

$$
K_2^C=\text{contestant 2 does not get kale}
$$

> **Memory:** Superscript $C$ = **complement = not**.

---

### General Multiplication Rule

The probability that both $A$ and $B$ occur is:

$$
\boxed{P(A\text{ and }B)=P(A)P(B\mid A)}
$$

Equivalently:

$$
\boxed{P(A\cap B)=P(A)P(B\mid A)}
$$

The symbol $\cap$ means **"and."**

---

### Example: Neither Contestant Gets Kale

"Neither gets kale" means:

- Contestant 1 does **not** get kale.
- Contestant 2 does **not** get kale.

Therefore:

$$
P(K_1^C\cap K_2^C)
$$

If the contestants' spins are independent:

$$
P(K_1^C\cap K_2^C)=P(K_1^C)P(K_2^C)
$$

Because contestant 1's result does not affect contestant 2's wheel.

---

### Interpreting Conditional Probability

Consider:

$$
P(K_1^C\cap K_2)=P(K_1^C)P(K_2\mid K_1^C)
$$

Read this as:

> The probability that contestant 1 **does not get kale AND contestant 2 gets kale** equals the probability that contestant 1 does not get kale, multiplied by the probability that contestant 2 gets kale **given that contestant 1 did not get kale**.

The vertical bar:

$$
\boxed{\mid=\text{"given"}}
$$

So:

$$
P(K_2\mid K_1^C)
$$

means:

$$
\boxed{\text{Probability contestant 2 gets kale given contestant 1 did not}}
$$

---

### Independent vs. Dependent Form

**General case:**

$$
\boxed{P(A\cap B)=P(A)P(B\mid A)}
$$

**Independent case:**

$$
P(B\mid A)=P(B)
$$

so:

$$
\boxed{P(A\cap B)=P(A)P(B)}
$$

The conditional probability is necessary when the first event can change the probability of the second.

---

### Key Takeaways

> $A^C$ = **A does not occur**.

> $A\cap B$ = **A and B both occur**.

> $P(B\mid A)$ = **probability of B given A**.

> **General multiplication rule:**

$$
\boxed{P(A\cap B)=P(A)P(B\mid A)}
$$

> For independent events:

$$
\boxed{P(A\cap B)=P(A)P(B)}
$$

### Memory Trick

> **$C$ = complement = NOT**

> **$\cap$ = AND**

> **$|$ = GIVEN**

### Video

[Interpreting the general multiplication rule](https://www.youtube.com/watch?v=yTJawPRzCzI)

---

# Conditional Probability

## Lesson 1 : Conditional Probability and Independence

### Using Conditional Probability to Test Independence

Two events $A$ and $B$ are **independent** if knowing that one occurred does not change the probability of the other.

A useful test is:

$$
\boxed{P(B\mid A)=P(B)\quad\Rightarrow\quad\text{independent}}
$$

If:

$$
\boxed{P(B\mid A)\neq P(B)}
$$

then the events are **dependent**.

> **Memory:** If knowing $A$ changes the probability of $B$, they're dependent.

---

### Example: Weather and Train Delays

James records weather and train performance for **365 days**.

We want to know whether:

- $D$ = train is delayed
- $S$ = day is snowy

are independent.

---

### Probability of a Delay

The train was delayed on **35 out of 365 days**:

$$
P(D)=\dfrac{35}{365}\approx0.096
$$

So the experimental probability of a delay is about:

$$
\boxed{9.6\%}
$$

---

### Probability of Delay Given Snow

There were **20 snowy days**, and the train was delayed on **12** of them.

$$
P(D\mid S)=\dfrac{12}{20}=0.60
$$

So:

$$
\boxed{P(D\mid S)=60\%}
$$

---

### Compare the Probabilities

$$
P(D)\approx9.6\%
$$

while:

$$
P(D\mid S)=60\%
$$

These are very different.

Knowing that the day is snowy greatly changes the observed probability of a train delay.

Therefore:

$$
\boxed{D\text{ and }S\text{ are not independent}}
$$

They are **dependent**.

---

### Experimental Probability

These probabilities come from observed data, so they are **experimental probabilities**.

They estimate the underlying theoretical probabilities but may not equal them exactly.

With more observations, experimental probabilities generally tend to give better estimates of the true probabilities.

> **Memory:** Experimental probability = what the data observed; theoretical probability = what should happen in the underlying model.

---

### Key Takeaways

To test whether $A$ and $B$ are independent, compare:

$$
\boxed{P(B)}
$$

with:

$$
\boxed{P(B\mid A)}
$$

If they are equal:

$$
\boxed{\text{Independent}}
$$

If they differ:

$$
\boxed{\text{Dependent}}
$$

In the train example:

$$
P(D)\approx9.6\%\neqP(D\mid S)=60\%
$$

Therefore:

$$
\boxed{\text{Delayed and snowy are dependent}}
$$

### Memory Trick

> **Same probability → independent.**

> **Changed probability → dependent.**

### Video

[Conditional probability and independence](https://www.youtube.com/watch?v=pIfpHdGVwLU)

---

## Lesson 2 — Bayes' Formula

### 1. Conditional Probability

For events $E$ and $F$:

$$
\boxed{P(E\mid F)=\dfrac{P(EF)}{P(F)}}
$$

#### Rule

$$
\boxed{P(EF)=P(E\mid F)P(F)}
$$

This is the **multiplication rule**.

It tells us the probability that **both $E$ and $F$ occur**.

---

### 2. Multiplication Rule for Multiple Events

For three events:

$$
\boxed{P(E_1E_2E_3)=P(E_1)P(E_2\mid E_1)P(E_3\mid E_1E_2)}
$$

More generally:

$$
\boxed{P(E_1E_2\cdots E_n)=P(E_1)P(E_2\mid E_1)\cdotsP(E_n\mid E_1\cdots E_{n-1})}
$$

#### Key idea

When events are dependent, the probability of later events can change based on what happened earlier.

---

### 3. Splitting an Event into Cases

An event $E$ can be divided according to whether $F$ occurred:

$$
\boxed{E=EF\cup EF^c}
$$

There are two mutually exclusive ways for $E$ to happen:

1. $E$ happens and $F$ happens.
2. $E$ happens and $F$ does not happen.

Therefore:

$$
P(E)=P(EF)+P(EF^c)
$$

Using the multiplication rule:

$$
\boxed{P(E)=P(E\mid F)P(F)+P(E\mid F^c)P(F^c)}
$$

Since:

$$
P(F^c)=1-P(F)
$$

we can also write:

$$
\boxed{P(E)=P(E\mid F)P(F)+P(E\mid F^c)[1-P(F)]}
$$

---

### 4. Law of Total Probability

The previous identity is called the **law of total probability**.

For two cases:

$$
\boxed{P(E)=P(E\mid F)P(F)+P(E\mid F^c)P(F^c)}
$$

#### Intuition

Instead of calculating $P(E)$ directly, we divide the world into cases.

$$
\text{Overall probability}=\text{probability through case 1}+\text{probability through case 2}
$$

Each case contributes:

$$
\text{conditional probability}\times\text{probability of that case}
$$

So $P(E)$ is a **weighted average** of the conditional probabilities.

---

### 5. Bayes' Formula

Start with:

$$
P(F\mid E)=\dfrac{P(EF)}{P(E)}
$$

Using the multiplication rule:

$$
P(EF)=P(E\mid F)P(F)
$$

Therefore:

$$
\boxed{P(F\mid E)=\dfrac{P(E\mid F)P(F)}{P(E)}}
$$

Now substitute the law of total probability for $P(E)$:

$$
\boxed{P(F\mid E)=\dfrac{P(E\mid F)P(F)}{P(E\mid F)P(F)+P(E\mid F^c)P(F^c)}}
$$

This is **Bayes' Formula for two possibilities**.

---

### 6. General Bayes' Formula

Suppose:

$$
F_1,F_2,\ldots,F_n
$$

are mutually exclusive events whose union is the entire sample space.

Then:

$$
\boxed{P(F_j\mid E)=\dfrac{P(E\mid F_j)P(F_j)}{\sum_{i=1}^{n}P(E\mid F_i)P(F_i)}}
$$

The denominator is:

$$
\boxed{P(E)=\sum_{i=1}^{n}P(E\mid F_i)P(F_i)}
$$

This denominator is the **law of total probability**.

---

### 7. How to Think About Bayes

Bayes reverses the direction of conditioning.

You may know:

$$
P(E\mid F)
$$

but want:

$$
P(F\mid E)
$$

These are generally **not equal**:

$$
\boxed{P(E\mid F)\neq P(F\mid E)}
$$

Bayes gives us the connection between them.

#### Conceptually

$$
\boxed{\text{Prior belief}\quad+\quad\text{new evidence}\quad\longrightarrow\quad\text{updated belief}}
$$

In probability notation:

$$
\boxed{P(F)\longrightarrow P(F\mid E)}
$$

---

### 8. Prior, Likelihood, Posterior

A useful way to interpret Bayes is:

$$
\boxed{P(F\mid E)\proptoP(E\mid F)P(F)}
$$

The three important quantities are:

- $P(F)$ — **prior probability**
- $P(E\mid F)$ — how likely the evidence is if $F$ is true
- $P(F\mid E)$ — **posterior probability**

So:

$$
\boxed{\text{Posterior}\propto\text{Likelihood}\times\text{Prior}}
$$

The denominator normalizes the result so that the resulting probabilities sum correctly.

---

### 9. Odds

For an event $H$, the odds are:

$$
\boxed{\dfrac{P(H)}{P(H^c)}}
$$

For example, if:

$$
P(H)=0.2
$$

then:

$$
P(H^c)=0.8
$$

and:

$$
\text{Odds of }H=\dfrac{0.2}{0.8}=\dfrac14
$$

So the odds are $1:4$.

---

### 10. Bayes' Formula in Odds Form

The book gives:

$$
\boxed{\dfrac{P(H\mid E)}{P(H^c\mid E)}=\dfrac{P(H)}{P(H^c)}\dfrac{P(E\mid H)}{P(E\mid H^c)}}
$$

This can be interpreted as:

$$
\boxed{\text{Posterior odds}=\text{Prior odds}\times\text{Evidence ratio}}
$$

where:

$$
\boxed{\dfrac{P(E\mid H)}{P(E\mid H^c)}}
$$

measures how much the evidence $E$ favors $H$ over $H^c$.

This form becomes particularly important later in statistical inference and Bayesian statistics.

---

### 11. Independence

Two events $E$ and $F$ are independent if:

$$
\boxed{P(EF)=P(E)P(F)}
$$

This means that knowing one event occurred does not change the probability of the other.

Equivalent forms are:

$$
\boxed{P(E\mid F)=P(E)}
$$

and:

$$
\boxed{P(F\mid E)=P(F)}
$$

Therefore:

$$
\boxed{E\text{ and }F\text{ independent}\iffP(EF)=P(E)P(F)}
$$

provided the relevant conditional probabilities are defined.

---

### 12. Dependence

If:

$$
P(E\mid F)\neq P(E)
$$

then learning that $F$ occurred changes the probability of $E$.

Therefore the events are dependent.

Similarly:

$$
P(F\mid E)\neq P(F)
$$

indicates dependence.

#### Intuition

Independent:

$$
\boxed{\text{Knowing }F\text{ gives no information about }E}
$$

Dependent:

$$
\boxed{\text{Knowing }F\text{ gives information about }E}
$$

---

### 13. Independence and the Multiplication Rule

The general multiplication rule is:

$$
P(EF)=P(E\mid F)P(F)
$$

If $E$ and $F$ are independent:

$$
P(E\mid F)=P(E)
$$

so:

$$
P(EF)=P(E)P(F)
$$

Therefore, independence is essentially the situation where the conditional probability disappears:

$$
\boxed{P(E\mid F)=P(E)}
$$

---

### 14. Independence of Multiple Events

Events:

$$
E_1,E_2,\ldots,E_n
$$

are independent if **every subset** satisfies:

$$
\boxed{P(E_{i_1}E_{i_2}\cdots E_{i_r})=P(E_{i_1})P(E_{i_2})\cdots P(E_{i_r})}
$$

This is stronger than simply saying every pair is independent.

The distinction between **pairwise independence** and **mutual independence** becomes important later.

---

### 15. One Unified Picture

The ideas in this lesson fit together:

$$
\boxed{P(E\mid F)=\dfrac{P(EF)}{P(F)}}
$$

gives us conditional probability.

From it:

$$
\boxed{P(EF)=P(E\mid F)P(F)}
$$

gives the multiplication rule.

Breaking $E$ into the cases $F$ and $F^c$:

$$
\boxed{
P(E)=P(E\mid F)P(F)+P(E\mid F^c)P(F^c)}
$$

gives the law of total probability.

Then reversing the conditioning:

$$
\boxed{P(F\mid E)=\dfrac{P(E\mid F)P(F)}{P(E)}}
$$

gives Bayes' Formula.

So the logical progression is:

$$
\boxed{\text{Conditional Probability}\rightarrow\text{Multiplication Rule}\rightarrow\text{Total Probability}\rightarrow\text{Bayes' Formula}}
$$

And independence tells us when conditioning doesn't change anything:

$$
\boxed{P(E\mid F)=P(E)}
$$

---

### 16. Core Rules to Remember

$$
\boxed{P(E\mid F)=\dfrac{P(EF)}{P(F)}}
$$

$$
\boxed{P(EF)=P(E\mid F)P(F)}
$$

$$
\boxed{P(E_1\cdots E_n)=P(E_1)P(E_2\mid E_1)\cdots P(E_n\mid E_1\cdots E_{n-1})
}
$$

$$
\boxed{P(E)=\sum_i P(E\mid F_i)P(F_i)}
$$

$$
\boxed{P(F_j\mid E)=\dfrac{P(E\mid F_j)P(F_j)}{\sum_iP(E\mid F_i)P(F_i)}}
$$

$$
\boxed{E,F\text{ independent}\iffP(EF)=P(E)P(F)}
$$

$$
\boxed{E,F\text{ independent}\iffP(E\mid F)=P(E)}
$$

$$
\boxed{\text{Posterior odds}=\text{Prior odds}\times\text{Evidence ratio}}
$$

The most important conceptual distinction in this lesson is:

$$
\boxed{P(E\mid F)\text{ asks about }E\text{ when }F\text{ is known}}
$$

whereas

$$
\boxed{P(F\mid E)\text{ asks about }F\text{ when }E\text{ is known}}
$$

**Bayes' Formula is the bridge between those two directions.**

---

## Lesson 3 : Conditional Probability Tree Diagram Example

### Drug Test Example

A drug test has:

- **False positive rate:** $2\%$
- **False negative rate:** $1\%$
- **Actually using drugs:** $5\%$

Suppose there are **10,000 applicants**.

$$
\boxed{5\%=500\text{ on drugs}}
$$

$$
\boxed{95\%=9,500\text{ not on drugs}}
$$

---

### Applicants Actually Taking Drugs

The test correctly identifies $99\%$ of drug users:

$$
500\times99\%=495
$$

So:

- **495** → correctly test positive
- **5** → falsely test negative

---

### Applicants Not Taking Drugs

The false positive rate is $2\%$:

$$
9,500\times2\%=190
$$

So:

- **190** → falsely test positive
- **9,310** → correctly test negative

---

### Tree Diagram Probabilities

Each branch is multiplied along the path:

$$
P(\text{on drugs and positive})=0.05\times0.99=0.0495
$$

$$
\boxed{4.95\%}
$$

For not taking drugs but testing positive:

$$
P(\text{not drugs and positive})=0.95\times0.02=0.019
$$

$$
\boxed{1.9\%}
$$

> **Memory:** In a probability tree, **multiply along branches**.

---

### Given a Positive Test

We want:

$$
P(\text{drugs}\mid\text{positive})
$$

All positive tests:

$$
495+190=685
$$

Of these, **495** are actually taking drugs.

Therefore:

$$
P(\text{drugs}\mid\text{positive})=\dfrac{495}{685}
$$

$$
\approx\boxed{72\%}
$$

So a person who tests positive has only about a **72% probability of actually taking drugs**.

---

### Why Isn't It 98%?

The false positive rate is only $2\%$, but **95% of applicants do not use drugs**.

Therefore, even a small false positive rate applied to the much larger non-drug population produces many false positives.

$$
\boxed{\text{Low false positive rate}\neq\text{high probability of actually having the condition}}
$$

This is an important application of **conditional probability**.

---

### False Positive Perspective

Among positive tests:

- **495** actually use drugs → about $72\%$
- **190** do not use drugs → about $28\%$

$$
\boxed{P(\text{not drugs}\mid\text{positive})\approx28\%}
$$

So a positive result does **not** guarantee the person is taking drugs.

---

### Quick Exam Strategy

For questions like:

> "Given a positive test, what is the probability the person actually has the condition?"

Use:

$$
\boxed{P(\text{condition}\mid\text{positive})=\dfrac{\text{true positives}}{\text{all positive results}}}
$$

For this example:

$$
\boxed{\dfrac{495}{495+190}\approx72\%}
$$

### Key Takeaways

> **False positive:** no drugs → test says positive.

> **False negative:** drugs → test says negative.

> **Multiply probabilities along a tree path.**

> **Add probabilities/counts of all paths leading to the desired condition.**

$$
\boxed{P(\text{drugs}\mid\text{positive})=\dfrac{\text{true positives}}{\text{true positives + false positives}}}
$$

The key idea:

$$
\boxed{\text{Positive test}\neq\text{certainly has condition}}
$$

The underlying prevalence of the condition matters.

### Memory Trick

> **Tree:** multiply down a path.

> **Conditional probability:** desired cases ÷ all cases matching the condition.

> **Rare condition + false positives → positive results can contain many false positives.**

### Video

[Conditional probability tree diagram example](https://www.youtube.com/watch?v=hxEdXUB_IdQ)

---