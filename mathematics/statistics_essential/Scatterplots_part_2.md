# Source and attribution

These are my personal study notes based on the Khan Academy Statistics course.

- Course: Statistics
- Provider: Khan Academy
- Source: https://www.khanacademy.org/math/probability
- Copyright: © 2025 Khan Academy. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Khan Academy course materials.

# Residuals

## Lesson 1 : Residuals and Least-Squares Regression

### Linear Regression

**Linear regression** is a method used to fit a straight line to data in a scatterplot.

The goal is to find a line that describes the **general trend** of the data as closely as possible.

For example, when studying the relationship between **height and weight**, the scatterplot may show that:

$$
\boxed{\text{As height increases, weight tends to increase}}
$$

A regression line attempts to model this relationship with a straight line.

---

### Regression Line

A regression line gives a **predicted value** of \(y\) for a given value of \(x\).

The predicted value is written as:

$$
\boxed{\hat{y}}
$$

The symbol \(\hat{y}\) is read as **"y-hat"**.

It represents the value of \(y\) predicted by the regression model, not necessarily the actual observed value.

A regression equation can be written as:

$$
\boxed{\hat{y}=a+bx}
$$

where:

- \(a\) → **y-intercept**
- \(b\) → **slope**
- \(x\) → explanatory/independent variable
- \(\hat{y}\) → predicted value of \(y\)

---

### Actual Value vs Predicted Value

For a given data point, there are two different \(y\)-values:

**Actual value:**

$$
y
$$

This is the value that was actually observed.

**Predicted value:**

$$
\hat{y}
$$

This is the value predicted by the regression line.

They will not necessarily be equal because data points usually do not lie exactly on the regression line.

$$
\boxed{y\neq\hat{y}\text{ in general}}
$$

---

### Residual

A **residual** is the difference between the actual value and the value predicted by the regression model.

The formula is:

$$
\boxed{\text{Residual}=y-\hat{y}}
$$

In words:

> **Residual = actual value − predicted value**

This measures how far the actual data point is from the regression line in the vertical direction.

---

### Interpreting a Residual

The sign of the residual tells us whether the actual point is above or below the regression line.

#### Positive Residual

If:

$$
y-\hat{y}>0
$$

then:

$$
y>\hat{y}
$$

The actual value is **above** the regression line.

$$
\boxed{\text{Positive residual}\rightarrow\text{point is above the line}}
$$

---

#### Negative Residual

If:

$$
y-\hat{y}<0
$$

then:

$$
y<\hat{y}
$$

The actual value is **below** the regression line.

$$
\boxed{\text{Negative residual}\rightarrow\text{point is below the line}}
$$

---

#### Zero Residual

If:

$$
y-\hat{y}=0
$$

then:

$$
y=\hat{y}
$$

The point lies exactly on the regression line.

$$
\boxed{\text{Zero residual}\rightarrow\text{point is on the line}}
$$

---

### Example: Height and Weight

Suppose the regression equation is:

$$
\hat{y}=-140+\frac{14}{3}x
$$

where:

- \(x\) = height in inches
- \(\hat{y}\) = predicted weight in pounds

Consider a person who is \(60\) inches tall and weighs \(125\) pounds.

The actual value is:

$$
y=125
$$

First calculate the predicted value:

$$\hat{y}=-140+\frac{14}{3}(60)$$

Since:

$$
\frac{60}{3}=20
$$

we get:

$$
\hat{y}=-140+14(20)
$$

$$
\hat{y}=-140+280
$$

$$
\boxed{\hat{y}=140}
$$

So the model predicts a weight of \(140\) pounds.

---

### Calculating the Residual

Use:

$$
\text{Residual}=y-\hat{y}
$$

Substitute the values:

$$
\text{Residual}=125-140
$$

Therefore:

$$
\boxed{\text{Residual}=-15}
$$

The residual is negative because the actual weight is **15 pounds below** the predicted weight.

$$
\boxed{-15\rightarrow\text{actual value is below the prediction}}
$$

---

### Visual Meaning of a Residual

A residual can be visualized as the **vertical distance** between a data point and the regression line.

For a point above the line:

$$
\boxed{\text{Positive residual}}
$$

For a point below the line:

$$
\boxed{\text{Negative residual}}
$$

The magnitude of the residual tells us how far the point is from the line.

For example:

$$
\text{Residual}=20
$$

means the point is \(20\) units above the predicted value.

While:

$$
\text{Residual}=-20
$$

means the point is \(20\) units below the predicted value.

---

### Least-Squares Regression

The most common method for finding a regression line is called **least-squares regression**.

The idea is to choose the line that minimizes the **sum of the squared residuals**.

Since:

$$
\text{Residual}=y-\hat{y}
$$

the squared residual is:

$$
(y-\hat{y})^2
$$

The least-squares regression line minimizes:

$$
\boxed{\sum (y-\hat{y})^2}
$$

This is why it is called **least squares**.

---

### Why Square the Residuals?

Residuals can be positive or negative.

If we simply added the residuals, positive and negative values could cancel each other out.

For example:

$$
10+(-10)=0
$$

even though both points are \(10\) units away from the predictions.

Squaring makes all residuals nonnegative:

$$
10^2=100
$$

$$
(-10)^2=100
$$

Therefore, squared residuals measure the overall size of the prediction errors without positive and negative errors canceling each other.

---

### What Makes a Good Regression Line?

A good regression line should:

- Follow the **general trend** of the data.
- Be reasonably close to the data points.
- Have relatively small residuals.
- Minimize the **sum of squared residuals** when using least-squares regression.

A line where most points are far away from it would have large residuals and therefore would not be a good fit.

$$
\boxed{
\text{Least-squares line}
\rightarrow
\text{minimizes }\sum(y-\hat{y})^2
}
$$

---

### Important Distinction

Do not confuse the **actual value** with the **predicted value**.

$$
\boxed{y=\text{actual}}
$$

$$
\boxed{\hat{y}=\text{predicted}}
$$

The residual compares them:

$$
\boxed{\text{Residual}=y-\hat{y}}
$$

---

### Key Takeaway

> **A residual is the actual value minus the predicted value from the regression line.**

Remember:

- \(y\) → actual value
- \(\hat{y}\) → predicted value
- \(y-\hat{y}\) → residual
- Positive residual → point is **above** the regression line.
- Negative residual → point is **below** the regression line.
- Zero residual → point is **on** the regression line.
- Least-squares regression minimizes the **sum of squared residuals**.

The core idea:

$$\boxed{\text{Actual }y-\text{Predicted }\hat{y}=\text{Residual}}$$

and:

$$
\boxed{
\text{Least-squares regression}
\rightarrow
\min\sum(y-\hat{y})^2
}
$$

---

### Video

[Residuals and least-squares regression](https://www.youtube.com/watch?v=VqD-nf1YUks)

---

## Lesson 2 : Calculating and Interpreting Residuals

### Least-Squares Regression Example

Vera records:

- **Customer height** in centimeters
- **Bicycle frame size** in centimeters

The relationship between the variables is fairly linear, so she uses a **least-squares regression line** to predict bicycle frame size from customer height.

The regression equation is:

$$
\boxed{\hat{y}=\frac{1}{3}+\frac{1}{3}x}
$$

where:

- \(x\) → customer's height
- \(\hat{y}\) → predicted bicycle frame size

---

### What the Regression Equation Does

The regression equation can be used to predict the frame size for a customer when their height is known.

$$
\boxed{
\text{Height}
\rightarrow
\text{Regression equation}
\rightarrow
\text{Predicted frame size}
}
$$

The prediction will not necessarily equal the customer's actual frame size.

---

### Residual Formula

A residual measures the difference between the **actual value** and the **predicted value**.

$$
\boxed{\text{Residual}=y-\hat{y}}
$$

In words:

> **Residual = actual − predicted**

---

### Example

A customer:

- is \(155\) cm tall
- rents a bicycle with a \(51\) cm frame

Therefore:

$$
x=155
$$

and the actual frame size is:

$$
y=51
$$

We need to find the predicted frame size first.

---

### Step 1: Calculate the Predicted Value

Use:

$$
\hat{y}=\frac{1}{3}+\frac{1}{3}x
$$

Substitute \(x=155\):

$$\hat{y}=\frac{1}{3}+\frac{1}{3}(155)$$

$$
=
\frac{1}{3}+\frac{155}{3}
$$

$$
=
\frac{156}{3}
$$

$$
\boxed{\hat{y}=52}
$$

The regression model predicts a frame size of \(52\) cm.

---

### Step 2: Calculate the Residual

The actual frame size is:

$$
y=51
$$

The predicted frame size is:

$$
\hat{y}=52
$$

Therefore:

$$
\text{Residual}=y-\hat{y}
$$

$$
=51-52
$$

$$
\boxed{\text{Residual}=-1}
$$

---

### Interpreting the Residual

The residual is:

$$
\boxed{-1\text{ cm}}
$$

This means the actual frame size was **1 cm smaller than the model predicted**.

The point lies **below the regression line**.

$$
\boxed{
\text{Negative residual}
\rightarrow
\text{actual value is below predicted value}
}
$$

---

### Positive vs Negative Residuals

#### Positive Residual

If:

$$
y>\hat{y}
$$

then:

$$
y-\hat{y}>0
$$

The actual value is **above** the regression line.

$$
\boxed{\text{Positive residual}\rightarrow\text{point above the line}}
$$

---

#### Negative Residual

If:

$$
y<\hat{y}
$$

then:

$$
y-\hat{y}<0
$$

The actual value is **below** the regression line.

$$
\boxed{\text{Negative residual}\rightarrow\text{point below the line}}
$$

---

### Residual as Vertical Distance

A residual can be thought of as the **signed vertical distance** between a data point and the regression line.

- Above the line → positive residual
- Below the line → negative residual
- On the line → zero residual

The **magnitude** tells us how far the point is from the line.

For example:

$$
\text{Residual}=+3
$$

means the point is \(3\) units above the prediction.

While:

$$
\text{Residual}=-3
$$

means the point is \(3\) units below the prediction.

---

### Important Distinction

The residual is **not**:

$$
\hat{y}-y
$$

Instead, the standard residual formula is:

$$
\boxed{y-\hat{y}}
$$

So always remember:

$$
\boxed{\text{Residual}=\text{Actual}-\text{Predicted}}
$$

---

### Key Takeaway

> **To calculate a residual, first use the regression equation to find the predicted value, then subtract the prediction from the actual value.**

For the bicycle example:

$$\hat{y}=\frac13+\frac13(155)=52$$

Then:

$$\text{Residual}=51-52=\boxed{-1}$$

Therefore:

$$
\boxed{
-1\text{ cm}
\rightarrow
\text{actual frame size was 1 cm below the prediction}
}
$$

Remember:

- **Actual** → \(y\)
- **Predicted** → \(\hat{y}\)
- **Residual** → \(y-\hat{y}\)
- Positive residual → **above** the regression line
- Negative residual → **below** the regression line
- Zero residual → **on** the regression line

The core process:

$$
\boxed{
x
\rightarrow
\hat{y}
\rightarrow
y-\hat{y}
\rightarrow
\text{Residual}
}
$$

---

### Video

[Calculating and interpreting residuals](https://www.youtube.com/watch?v=50ezMTE_BuA)

---

## Lesson 3 : Creating and Analyzing Residual Plots

### What Is a Residual Plot?

A **residual plot** is a graph that shows the residuals for the data points in a regression model.

Recall:

$$
\boxed{\text{Residual}=y-\hat{y}}
$$

where:

- \(y\) → actual value
- \(\hat{y}\) → predicted value from the regression line

A residual plot shows:

- \(x\) values on the horizontal axis
- residuals on the vertical axis

So instead of plotting the original \(y\)-values, we plot the **residual** for each data point.

$$
\boxed{(x,y)\rightarrow(x,\text{residual})}
$$

---

### Why Use a Residual Plot?

The main purpose of a residual plot is to determine **how well a linear regression model fits the data**.

A residual plot helps us identify whether:

- the regression line is a good model
- there is a pattern that the linear model is failing to explain
- a non-linear model might be more appropriate

The key question is:

> **Are the residuals randomly scattered around 0, or do they form a pattern?**

---

### How to Create a Residual Plot

To create a residual plot:

1. Start with the original data point.
2. Use the regression equation to calculate \(\hat{y}\).
3. Calculate the residual:

$$
\boxed{\text{Residual}=y-\hat{y}}
$$

4. Keep the original \(x\)-value.
5. Plot the point:

$$
\boxed{(x,\text{residual})}
$$

The horizontal axis is \(x\), and the vertical axis is the residual.

---

### Example: Calculating Residuals

Suppose the regression equation is:

$$
\hat{y}=2.5x-2
$$

Consider a data point where:

$$
x=1,\qquad y=1
$$

First find the predicted value:

$$
\hat{y}=2.5(1)-2
$$

$$
\hat{y}=0.5
$$

Now calculate the residual:

$$
\text{Residual}=y-\hat{y}
$$

$$
=1-0.5
$$

$$
\boxed{\text{Residual}=0.5}
$$

So the residual plot contains the point:

$$
\boxed{(1,0.5)}
$$

Because the residual is positive, the original data point was **above the regression line**.

---

### Another Example

Suppose:

$$
x=2,\qquad y=2
$$

Using:

$$
\hat{y}=2.5x-2
$$

we get:

$$
\hat{y}=2.5(2)-2
$$

$$
=5-2
$$

$$
=3
$$

Therefore:

$$
\text{Residual}=2-3
$$

$$
\boxed{\text{Residual}=-1}
$$

So the residual plot contains:

$$
\boxed{(2,-1)}
$$

The negative residual means the actual point was **below the regression line**.

---

### Example with Zero Residual

Suppose:

$$
x=2,\qquad y=3
$$

The regression equation predicts:

$$
\hat{y}=3
$$

Therefore:

$$
\text{Residual}=3-3=0
$$

So:

$$
\boxed{\text{Residual}=0}
$$

The original point lies exactly on the regression line.

In the residual plot, this point is located **on the horizontal axis**.

---

### Example Data Set

Suppose the data produce these residuals:

| \(x\) | Actual \(y\) | Predicted \(\hat{y}\) | Residual \(y-\hat{y}\) |
|---:|---:|---:|---:|
| 1 | 1 | 0.5 | \(+0.5\) |
| 2 | 3 | 3 | \(0\) |
| 2 | 2 | 3 | \(-1\) |
| 3 | 6 | 5.5 | \(+0.5\) |

The residual plot would contain:

$$
(1,0.5),\quad(2,0),\quad(2,-1),\quad(3,0.5)
$$

Notice that two observations can have the **same \(x\)-value** but different residuals.

---

### Understanding the Residual Plot

The horizontal axis represents:

$$
\boxed{x}
$$

The vertical axis represents:

$$
\boxed{\text{Residual}}
$$

The horizontal axis is therefore also the **zero-residual line**.

$$
\boxed{\text{Residual}=0}
$$

Points above this line have positive residuals.

Points below this line have negative residuals.

---

### Positive and Negative Residuals

#### Positive Residual

If:

$$
y-\hat{y}>0
$$

then:

$$
y>\hat{y}
$$

The actual value is greater than the predicted value.

Therefore, the original point is above the regression line.

$$
\boxed{\text{Positive residual}\rightarrow\text{above regression line}}
$$

---

#### Negative Residual

If:

$$
y-\hat{y}<0
$$

then:

$$
y<\hat{y}
$$

The actual value is less than the predicted value.

Therefore, the original point is below the regression line.

$$
\boxed{\text{Negative residual}\rightarrow\text{below regression line}}
$$

---

#### Zero Residual

If:

$$
y-\hat{y}=0
$$

then:

$$
y=\hat{y}
$$

The point lies exactly on the regression line.

$$
\boxed{\text{Zero residual}\rightarrow\text{on the regression line}}
$$

---

### What Does a Good Residual Plot Look Like?

A good residual plot should have residuals that are **randomly scattered around 0**.

Ideally:

- Some residuals are positive.
- Some residuals are negative.
- The points are spread around the horizontal axis.
- There is **no obvious pattern or trend**.

For example, a residual plot might look roughly like:

$$
\boxed{
\text{random scatter above and below }0
}
$$

When the residuals look randomly scattered, a **linear model is generally appropriate**.

The regression line is doing a reasonable job of explaining the relationship between \(x\) and \(y\).

---

### Key Rule for Residual Plots

$$
\boxed{
\text{Randomly scattered residuals}
\rightarrow
\text{linear model is probably appropriate}
}
$$

Think:

> **Random = good**

---

### What Does a Bad Residual Plot Look Like?

If the residuals form a **clear pattern**, the linear model may not be appropriate.

Examples of patterns include:

- upward trend
- downward trend
- curved pattern
- U-shape
- upside-down U-shape

For example, if the residuals first decrease and then increase, they may form a curved pattern.

$$
\boxed{
\text{Pattern in residuals}
\rightarrow
\text{linear model may not be appropriate}
}
$$

A non-linear model may better describe the relationship.

---

### Why Does a Pattern Matter?

A regression line assumes that the relationship between \(x\) and \(y\) can reasonably be described by a straight line.

If the residuals show a pattern, that means the regression line is systematically missing something about the relationship.

For example, if the residuals form a curve:

$$
\boxed{
\text{Curved residual pattern}
\rightarrow
\text{relationship may be non-linear}
}
$$

A curved regression model may fit the data better than a straight line.

---

### Residuals That Are Very Far from Zero

Another warning sign is when many residuals are **far away from 0**.

Remember:

$$
\text{Residual}=y-\hat{y}
$$

A large residual means the actual value is far from the predicted value.

For example:

$$
\text{Residual}=10
$$

means the actual value is \(10\) units above the prediction.

While:

$$
\text{Residual}=-10
$$

means the actual value is \(10\) units below the prediction.

If many residuals have large magnitudes, the regression line may not be a very good fit.

$$
\boxed{
\text{Large residuals}
\rightarrow
\text{predictions are often far from actual values}
}
$$

---

### Residual Plot vs Original Scatterplot

These two graphs answer slightly different questions.

#### Original Scatterplot

Shows the relationship between:

$$
\boxed{x\text{ and }y}
$$

It helps us see whether there appears to be a relationship between the variables.

---

#### Residual Plot

Shows the relationship between:

$$
\boxed{x\text{ and residual}}
$$

It helps us determine whether the **linear regression model is appropriate**.

This distinction is important.

A scatterplot may look roughly linear, but the residual plot can reveal a pattern that shows the linear model is not actually appropriate.

---

### Residual Plot and Regression Line Direction

The regression line can have either:

- positive slope
- negative slope

The residual plot still works the same way.

The residual is always:

$$
\boxed{y-\hat{y}}
$$

And we always look for residuals that are randomly scattered around \(0\).

Therefore:

$$
\boxed{
\text{Upward or downward regression line}
\rightarrow
\text{same residual-plot analysis}
}
$$

---

### Connection to Least-Squares Regression

The regression line discussed here is a **least-squares regression line**.

Recall that least-squares regression chooses the line that minimizes:

$$
\boxed{\sum(y-\hat{y})^2}
$$

The residual plot allows us to examine those residuals visually.

So the concepts connect like this:

$$
\boxed{
\text{Regression line}
\rightarrow
\text{Predictions}
\rightarrow
\text{Residuals}
\rightarrow
\text{Residual plot}
}
$$

---

### How to Analyze a Residual Plot

When given a residual plot, use this process:

#### Step 1: Look for randomness

Ask:

> Are the residuals randomly scattered around \(0\)?

If yes:

$$
\boxed{\text{Linear model is probably appropriate}}
$$

---

#### Step 2: Look for a pattern

Ask:

> Do the residuals form a trend or curve?

If yes:

$$
\boxed{\text{Linear model may not be appropriate}}
$$

---

#### Step 3: Look at the size of the residuals

Ask:

> Are many residuals far away from \(0\)?

If yes:

$$
\boxed{\text{The line may not fit the data very well}}
$$

---

### Common Residual Plot Patterns

| Residual plot | Interpretation |
|---|---|
| Randomly scattered around \(0\) | Linear model is probably a good fit |
| Clear upward trend | Linear model may not be appropriate |
| Clear downward trend | Linear model may not be appropriate |
| Curved pattern | Relationship may be non-linear |
| Many points far from \(0\) | Regression line may not fit well |

---

### Important Exam Rule

When analyzing a residual plot:

$$
\boxed{
\text{No pattern}
\rightarrow
\text{good evidence for a linear model}
}
$$

But:

$$
\boxed{
\text{Pattern}
\rightarrow
\text{evidence that a linear model may not be appropriate}
}
$$

Do **not** say that a residual plot must contain equal numbers of positive and negative residuals.

The important idea is that the residuals should be **randomly scattered around 0 with no clear pattern**.

---

### Key Takeaways

> **A residual plot plots each \(x\)-value against its residual.**

Remember:

$$
\boxed{\text{Residual}=y-\hat{y}}
$$

and:

$$
\boxed{\text{Residual plot}=(x,\text{residual})}
$$

The vertical axis represents residuals, and the horizontal axis represents \(x\).

### Good residual plot:

$$
\boxed{
\text{Random scatter around }0
\rightarrow
\text{linear model is probably appropriate}
}
$$

### Bad residual plot:

$$
\boxed{
\text{Clear pattern}
\rightarrow
\text{linear model may not be appropriate}
}
$$

### Large residuals:

$$
\boxed{
|\text{residual}|\text{ large}
\rightarrow
\text{actual value is far from prediction}
}
$$

The most important idea:

$$
\boxed{
\text{Residual plot}
\rightarrow
\text{check whether a linear regression model is a good fit}
}
$$

---

### Quick Memory Trick

> **Residuals tell you how far off the predictions are.**
>
> **Residual plots tell you whether those errors have a pattern.**

So:

$$
\boxed{
\text{Random errors}
\rightarrow
\text{linear model looks good}
}
$$

$$
\boxed{
\text{Patterned errors}
\rightarrow
\text{linear model may be wrong}
}
$$

---

### Video

[Creating and analyzing residual plots](https://www.youtube.com/watch?v=VamMrPZ-8fc)

---

## Lesson 4 : Covariance, Joint Variation, and Correlation

### Overview

When studying two variables \(X\) and \(Y\), we often want to know:

1. How much does each variable vary individually?
2. Do \(X\) and \(Y\) tend to move together?
3. If they move together, do they move in the **same direction** or in **opposite directions**?
4. How strong is their linear relationship?

Three important concepts help answer these questions:

$$
\boxed{\text{Standard Deviation}}
$$

$$
\boxed{\text{Covariance}}
$$

$$
\boxed{\text{Correlation}}
$$

A useful way to think about them is:

> **Standard deviation describes the variation of one variable.**
>
> **Covariance describes how two variables vary together.**
>
> **Correlation standardizes covariance so that the strength of the relationship can be compared.**

---

### 1. Deviation from the Mean

Before understanding covariance, we need to understand how far an observation is from its mean.

For an observation \(x_i\), the deviation from the mean is:

$$
\boxed{x_i-\bar{x}}
$$

For an observation \(y_i\), the deviation from the mean is:

$$
\boxed{y_i-\bar{y}}
$$

where:

- \(x_i\) → individual observation of \(X\)
- \(y_i\) → individual observation of \(Y\)
- \(\bar{x}\) → mean of \(X\)
- \(\bar{y}\) → mean of \(Y\)

These deviations tell us whether an observation is above or below its variable's mean.

---

#### Important Terminology

Be careful not to confuse **deviation from the mean** with a **regression residual**.

A regression residual is:

$$
\boxed{y_i-\hat{y}_i}
$$

where \(\hat{y}_i\) is the value predicted by a regression line.

A deviation from the mean is:

$$
\boxed{y_i-\bar{y}}
$$

These are different quantities.

#### Regression residual

$$
\boxed{y_i-\hat{y}_i}
$$

Measures:

> How far the actual observation is from the **regression prediction**.

#### Deviation from the mean

$$
\boxed{y_i-\bar{y}}
$$

Measures:

> How far the observation is from the **mean of the variable**.

Covariance and correlation use deviations from the **means**, not regression residuals.

---

### 2. How Two Variables Move Together

Suppose we have two variables:

$$
X
\quad\text{and}\quad
Y
$$

For each observation, we can determine whether \(X\) and \(Y\) are above or below their respective means.

Consider:

$$
x_i-\bar{x}
$$

and:

$$
y_i-\bar{y}
$$

There are four possibilities.

---

#### Case 1: Both Are Above Their Means

Suppose:

$$
x_i-\bar{x}>0
$$

and:

$$
y_i-\bar{y}>0
$$

Then both variables are above their means.

Their product is:

$$
(x_i-\bar{x})(y_i-\bar{y})>0
$$

because:

$$
(+)(+)=(+)
$$

Therefore, the product is **positive**.

---

#### Case 2: Both Are Below Their Means

Suppose:

$$
x_i-\bar{x}<0
$$

and:

$$
y_i-\bar{y}<0
$$

Then both variables are below their means.

Their product is:

$$
(x_i-\bar{x})(y_i-\bar{y})>0
$$

because:

$$
(-)(-)=(+)
$$

Again, the product is **positive**.

Therefore:

> When \(X\) and \(Y\) are both above their means or both below their means, their deviations have the same sign and their product is positive.

This is evidence that the variables are moving in the **same direction**.

---

### 3. When the Product Is Negative

Now suppose one variable is above its mean while the other is below its mean.

For example:

$$
x_i-\bar{x}>0
$$

but:

$$
y_i-\bar{y}<0
$$

Then:

$$
(x_i-\bar{x})(y_i-\bar{y})<0
$$

because:

$$
(+)(-) = (-)
$$

Similarly:

$$
(-)(+) = (-)
$$

Therefore, the product is negative whenever the two variables are on opposite sides of their means.

This indicates that they are moving in **opposite directions**.

---

### 4. The Joint Product

For each observation, we can multiply the two deviations:

$$
\boxed{
(x_i-\bar{x})(y_i-\bar{y})
}
$$

This product tells us whether the two variables are moving together for that particular observation.

We can define:

$$
e_{x,i}=x_i-\bar{x}
$$

and:

$$
e_{y,i}=y_i-\bar{y}
$$

Then the joint product is:

$$
\boxed{
e_{x,i}e_{y,i}
}
$$

or:

$$
\boxed{
(x_i-\bar{x})(y_i-\bar{y})
}
$$

---

### 5. Interpreting the Sign of the Joint Product

| \(X\) deviation | \(Y\) deviation | Product | Interpretation |
|---|---|---|---|
| \(+\) | \(+\) | \(+\) | Both are above their means |
| \(-\) | \(-\) | \(+\) | Both are below their means |
| \(+\) | \(-\) | \(-\) | \(X\) above, \(Y\) below |
| \(-\) | \(+\) | \(-\) | \(X\) below, \(Y\) above |

Therefore:

$$
\boxed{\text{Positive product}\rightarrow\text{same direction}}
$$

and:

$$
\boxed{\text{Negative product}\rightarrow\text{opposite directions}}
$$

This is the basic idea behind **covariance**.

---

### 6. Covariance

Covariance measures how two variables **vary together**.

The key idea is:

> Instead of looking at \(X\) and \(Y\) separately, covariance looks at whether their deviations from their means tend to have the same or opposite signs.

For a population, covariance is:

$$
\boxed{
\text{Cov}(X,Y)
=
\frac{1}{N}
\sum_{i=1}^{N}
(x_i-\mu_X)(y_i-\mu_Y)
}
$$

where:

- \(N\) → population size
- \(\mu_X\) → population mean of \(X\)
- \(\mu_Y\) → population mean of \(Y\)

For a sample, covariance is:

$$
\boxed{
s_{XY}
=
\frac{1}{n-1}
\sum_{i=1}^{n}
(x_i-\bar{x})(y_i-\bar{y})
}
$$

where:

- \(n\) → sample size
- \(\bar{x}\) → sample mean of \(X\)
- \(\bar{y}\) → sample mean of \(Y\)

The \(n-1\) denominator is used for the usual **sample covariance**.

---

### 7. Why Do We Take the Average?

For every observation, we calculate:

$$
(x_i-\bar{x})(y_i-\bar{y})
$$

Some products may be positive.

Some products may be negative.

If we simply looked at one observation, we would not know the overall relationship.

Instead, we combine all of the products and take their average.

Conceptually:

$$\boxed{\text{Covariance}=\text{average joint deviation}}$$

More precisely:

$$\boxed{\text{Covariance}=\text{average of the products of deviations from the means}}$$

This gives us an overall measure of how \(X\) and \(Y\) tend to move together.

---

### 8. Interpreting Covariance

#### Positive Covariance

If:

$$
\text{Cov}(X,Y)>0
$$

then \(X\) and \(Y\) tend to move in the **same direction**.

For example:

- \(X\) increases → \(Y\) tends to increase
- \(X\) decreases → \(Y\) tends to decrease

This is associated with a **positive linear relationship**.

$$
\boxed{
\text{Cov}(X,Y)>0
\rightarrow
\text{positive association}
}
$$

---

#### Negative Covariance

If:

$$
\text{Cov}(X,Y)<0
$$

then \(X\) and \(Y\) tend to move in **opposite directions**.

For example:

- \(X\) increases → \(Y\) tends to decrease
- \(X\) decreases → \(Y\) tends to increase

This is associated with a **negative linear relationship**.

$$
\boxed{
\text{Cov}(X,Y)<0
\rightarrow
\text{negative association}
}
$$

---

#### Covariance Near Zero

If:

$$
\text{Cov}(X,Y)\approx0
$$

then there is little overall tendency for the two variables to move together **linearly**.

However, covariance being zero does not necessarily mean there is no relationship of any kind.

For example, two variables could have a strong **nonlinear** relationship while having covariance close to zero.

---

### 9. A Very Important Correction

It is tempting to say:

> "If \(y-\hat{y}\) and \(x-\hat{x}\) are both positive, the covariance product is positive."

But this is not the standard definition of covariance.

For covariance, we use:

$$
\boxed{
(x_i-\bar{x})(y_i-\bar{y})
}
$$

not:

$$
(x_i-\hat{x}_i)(y_i-\hat{y}_i)
$$

In ordinary correlation/covariance calculations, there is no predicted \(x\)-value \(\hat{x}\) involved.

Therefore, remember:

#### Covariance:

$$
\boxed{
(x_i-\bar{x})(y_i-\bar{y})
}
$$

#### Regression residual:

$$
\boxed{
y_i-\hat{y}_i
}
$$

These concepts are related to analyzing data, but they are **not the same thing**.

---

### 10. Covariance and the Direction of a Scatterplot

Covariance gives information about the direction of a linear relationship.

### Positive relationship

A scatterplot that generally rises from left to right has:

$$
\boxed{\text{positive covariance}}
$$

For example:

$$
X\uparrow
\quad\Rightarrow\quad
Y\uparrow
$$

---

#### Negative relationship

A scatterplot that generally falls from left to right has:

$$
\boxed{\text{negative covariance}}
$$

For example:

$$
X\uparrow
\quad\Rightarrow\quad
Y\downarrow
$$

---

### No clear linear relationship

If the points do not show a consistent linear direction:

$$
\boxed{\text{Cov}(X,Y)\approx0}
$$

may occur.

---

### 11. The Problem with Covariance

Covariance tells us the **direction** of a relationship, but its magnitude is difficult to interpret by itself.

This is because covariance has units.

For example, suppose:

- \(X\) is measured in meters
- \(Y\) is measured in kilograms

Then covariance has units:

$$
\text{meters}\times\text{kilograms}
$$

If we change the units of measurement, the numerical value of covariance changes.

This makes it difficult to compare covariance values across different datasets.

This is where **correlation** becomes useful.

---

### 12. Standard Deviation

Before defining correlation, we need standard deviation.

Standard deviation measures how much a **single variable** tends to vary around its mean.

For a population:

$$
\boxed{
\sigma_X
=
\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}(x_i-\mu_X)^2
}
}
$$

Similarly:

$$
\boxed{
\sigma_Y
=
\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}(y_i-\mu_Y)^2
}
}
$$

For a sample:

$$
\boxed{
s_X
=
\sqrt{
\frac{1}{n-1}
\sum_{i=1}^{n}(x_i-\bar{x})^2
}
}
$$

and similarly for \(Y\).

---

### 13. What Standard Deviation Measures

Standard deviation answers:

> **How spread out are the values of this variable?**

For example, if the heights of a group of people are very similar, their standard deviation will be relatively small.

If their heights vary substantially, their standard deviation will be relatively large.

Therefore:

$$
\boxed{
\text{Standard deviation}
\rightarrow
\text{individual variable's spread}
}
$$

It does not directly tell us whether two variables move together.

---

### 14. Correlation

Correlation takes covariance and standardizes it using the standard deviations of both variables.

The population correlation coefficient is:

$$\boxed{\rho=\dfrac{\text{Cov}(X,Y)}{\sigma_X\sigma_Y}}$$

The sample correlation coefficient is commonly written as:

$$\boxed{r=\dfrac{s_{XY}}{s_Xs_Y}}$$

Therefore, conceptually:

$$\boxed{\text{Correlation}=\dfrac{\text{Covariance}}{\text{Standard deviation of }X\times\text{Standard deviation of }Y}}$$

---

### 15. Why Divide by the Standard Deviations?

Covariance tells us how two variables vary **together**, but its scale depends on the units of \(X\) and \(Y\).

Dividing by:

$$
\sigma_X\sigma_Y
$$

standardizes the covariance.

This produces a unitless number.

Therefore, correlation tells us the **direction and strength of a linear relationship** on a standardized scale.

---

### 16. Range of the Correlation Coefficient

The correlation coefficient always satisfies:

$$
\boxed{-1\le r\le1}
$$

or, for a population:

$$
\boxed{-1\le\rho\le1}
$$

---

#### \(r=1\)

Perfect positive linear correlation.

$$
\boxed{r=1}
$$

All points lie exactly on a straight line with positive slope.

As \(X\) increases, \(Y\) increases perfectly.

---

#### \(r=-1\)

Perfect negative linear correlation.

$$
\boxed{r=-1}
$$

All points lie exactly on a straight line with negative slope.

As \(X\) increases, \(Y\) decreases perfectly.

---

#### \(r\approx0\)

Little or no **linear** correlation.

$$
\boxed{r\approx0}
$$

This does not necessarily mean there is no relationship at all.

A nonlinear relationship can still exist.

---

### 17. Relationship Between Covariance and Correlation

Covariance and correlation contain similar directional information.

If:

$$
\text{Cov}(X,Y)>0
$$

then:

$$
r>0
$$

If:

$$
\text{Cov}(X,Y)<0
$$

then:

$$
r<0
$$

The difference is that correlation is **standardized**.

Therefore:

$$
\boxed{
\text{Covariance}
\rightarrow
\text{direction + unstandardized magnitude}
}
$$

while:

$$
\boxed{
\text{Correlation}
\rightarrow
\text{direction + standardized strength}
}
$$

---

### 18. Covariance vs Correlation

A useful conceptual progression is:

$$
\boxed{
\text{Deviation}
\rightarrow
\text{Joint deviation}
\rightarrow
\text{Covariance}
\rightarrow
\text{Correlation}
}
$$

First, determine how far each observation is from its mean:

$$
x_i-\bar{x}
$$

and:

$$
y_i-\bar{y}
$$

Then multiply them:

$$
(x_i-\bar{x})(y_i-\bar{y})
$$

Then average those products:

$$
\text{Cov}(X,Y)
$$

Finally, standardize covariance:

$$
r=
\frac{\text{Cov}(X,Y)}
{\sigma_X\sigma_Y}
$$

---

### 19. Important Interpretation

A simple way to remember the concepts:

#### Standard deviation

> **How much does one variable vary?**

$$
\boxed{\text{SD}\rightarrow\text{spread of one variable}}
$$

#### Covariance

> **Do two variables tend to vary together?**

$$
\boxed{\text{Covariance}\rightarrow\text{joint variation}}
$$

#### Correlation

> **How strongly and in what direction do two variables have a linear relationship?**

$$
\boxed{\text{Correlation}\rightarrow\text{standardized linear association}}
$$

---

### 20. Example of the Sign Logic

Suppose:

$$
\bar{x}=50
$$

and:

$$
\bar{y}=100
$$

Consider an observation:

$$
x_i=60
$$

and:

$$
y_i=120
$$

Then:

$$
x_i-\bar{x}=60-50=10
$$

and:

$$
y_i-\bar{y}=120-100=20
$$

Their joint product is:

$$
(10)(20)=200
$$

which is positive.

This observation contributes **positively** to the covariance.

---

Now suppose:

$$
x_i=60
$$

but:

$$
y_i=80
$$

Then:

$$
x_i-\bar{x}=10
$$

and:

$$
y_i-\bar{y}=-20
$$

Therefore:

$$
(10)(-20)=-200
$$

This observation contributes **negatively** to the covariance.

---

### 21. The Big Picture

For every observation, ask:

#### Step 1: Is \(X\) above or below its mean?

$$
x_i-\bar{x}
$$

#### Step 2: Is \(Y\) above or below its mean?

$$
y_i-\bar{y}
$$

#### Step 3: Multiply the deviations

$$
(x_i-\bar{x})(y_i-\bar{y})
$$

#### Step 4: Look at the overall average

$$
\text{Cov}(X,Y)
$$

#### Step 5: Standardize the covariance

$$
r=
\frac{\text{Cov}(X,Y)}
{\sigma_X\sigma_Y}
$$

This gives the correlation coefficient.

---

### 22. Key Formulas

#### Deviation from the mean

$$
\boxed{x_i-\bar{x}}
$$

$$
\boxed{y_i-\bar{y}}
$$

#### Joint deviation

$$
\boxed{
(x_i-\bar{x})(y_i-\bar{y})
}
$$

#### Population covariance

$$
\boxed{
\text{Cov}(X,Y)
=
\frac{1}{N}
\sum_{i=1}^{N}
(x_i-\mu_X)(y_i-\mu_Y)
}
$$

#### Sample covariance

$$
\boxed{
s_{XY}
=
\frac{1}{n-1}
\sum_{i=1}^{n}
(x_i-\bar{x})(y_i-\bar{y})
}
$$

#### Population correlation

$$
\boxed{
\rho=
\frac{\text{Cov}(X,Y)}
{\sigma_X\sigma_Y}
}
$$

#### Sample correlation

$$
\boxed{
r=
\frac{s_{XY}}
{s_Xs_Y}
}
$$

#### Correlation range

$$
\boxed{-1\le r\le1}
$$

---

### 23. Standard Deviation vs Covariance

| Feature | Standard Deviation | Covariance |
|---|---|---|
| What does it measure? | Spread of **one variable** | How **two variables vary together** |
| Number of variables | One | Two |
| Main question | "How spread out is \(X\)?" | "Do \(X\) and \(Y\) move together?" |
| Formula involves | Squared deviations | Product of two deviations |
| Basic expression | \((x_i-\bar{x})^2\) | \((x_i-\bar{x})(y_i-\bar{y})\) |
| Sign | Always nonnegative | Can be positive, negative, or near zero |
| Positive value means | Greater spread | Variables tend to move in the same direction |
| Negative value | Impossible for standard deviation | Variables tend to move in opposite directions |
| Units | Same units as the variable | Product of the units of \(X\) and \(Y\) |
| Standardized? | Yes, in the sense of measuring spread in original units | No |
| Easy to compare across different units? | More useful, but still depends on the variable's scale | Generally difficult |
| Relationship between variables? | Does not measure relationship between two variables | Measures joint linear variation |
| Related concept | Variance | Correlation |

---

### 24. Standard Deviation vs Covariance vs Correlation

| Concept | Standard Deviation | Covariance | Correlation |
|---|---|---|---|
| Variables involved | 1 | 2 | 2 |
| Measures | Individual spread | Joint variation | Strength and direction of linear association |
| Formula idea | Square deviations | Multiply deviations | Standardize covariance |
| Sign | \(+\) only | \(+\), \(-\), or \(0\) | Between \(-1\) and \(1\) |
| Units | Same as variable | Product of units | Unitless |
| Same direction? | Not applicable | Positive | Positive |
| Opposite direction? | Not applicable | Negative | Negative |
| Strength easy to interpret? | Relatively | Not directly | Yes |
| Main purpose | Measure variability | Measure how two variables vary together | Measure standardized linear relationship |

---

### Key Takeaway

The most important chain to remember is:

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

For each observation:

$$
\boxed{
x_i-\bar{x}
}
$$

and:

$$
\boxed{
y_i-\bar{y}
}
$$

Then:

$$
\boxed{
(x_i-\bar{x})(y_i-\bar{y})
}
$$

tells us whether the two variables are moving in the same or opposite directions for that observation.

Averaging these products gives covariance:

$$
\boxed{
\text{Cov}(X,Y)
=
\text{average joint variation}
}
$$

Then standardizing covariance gives correlation:

$$
\boxed{
r=
\frac{\text{Cov}(X,Y)}
{\sigma_X\sigma_Y}
}
$$

So remember:

$$\boxed{\text{Standard deviation}=\text{how much ONE variable varies}}$$

$$\boxed{\text{Covariance}=\text{how TWO variables vary together}}$$

$$\boxed{\text{Correlation}=\text{standardized strength and direction of their linear relationship}}$$

#### One crucial distinction

Do **not** confuse:

$$
\boxed{y_i-\hat{y}_i}
\quad\text{(regression residual)}
$$

with:

$$
\boxed{y_i-\bar{y}}
\quad\text{(deviation from the mean)}
$$

Covariance and correlation are based on **deviations from the means**:

$$
\boxed{
(x_i-\bar{x})(y_i-\bar{y})
}
$$

not regression residuals.

---