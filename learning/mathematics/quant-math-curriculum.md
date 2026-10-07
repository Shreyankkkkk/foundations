# Quant Mathematics — Self-Study Library

A focused mathematics curriculum for becoming a **quantitative researcher / derivatives quant / mathematical-finance quant** through self-study.

The goal of this collection is **not** to learn mathematics for its own sake.

The goal is to develop the mathematical foundations that are actually useful for:

- Quantitative Research
- Quantitative Trading
- Derivatives Pricing
- Mathematical Finance
- Quantitative Risk
- Numerical/Computational Finance

This collection is intentionally optimized to avoid spending time on mathematics that has little practical value for quant work.

---

# Curriculum

The curriculum currently consists of **18 core books**.

They are divided into:

- **14 books currently available**
- **2 books available externally**
- **4 books still missing**

The missing books are intentionally not replaced with random alternatives. They can be added later if necessary.

---

# Core Books

| #   | Book                                                                     | Subject                             | Status       |
| --- | ------------------------------------------------------------------------ | ----------------------------------- | ------------ |
| 1   | **Guichard — Single and Multivariable Calculus**                         | Calculus                            | 📁 Available |
| 2   | **Velleman — How to Prove It**                                           | Mathematical Proof / Maturity       | 📁 Available |
| 3   | **Strang — Introduction to Linear Algebra**                              | Linear Algebra                      | 📁 Available |
| 4   | **Boyce & DiPrima — Elementary Differential Equations**                  | ODEs                                | 📁 Available |
| 5   | **Ross — A First Course in Probability**                                 | Probability                         | 📁 Available |
| 6   | **Casella & Berger — Statistical Inference**                             | Mathematical Statistics             | 📁 Available |
| 7   | **Abbott — Understanding Analysis**                                      | Real Analysis                       | 📁 Available |
| 8   | **Axler — Measure, Integration & Real Analysis**                         | Measure Theory                      | 📁 Available |
| 9   | **Boyd & Vandenberghe — Convex Optimization**                            | Optimization                        | 📁 Available |
| 10  | **Burden & Faires — Numerical Analysis**                                 | Numerical Methods                   | 📁 Available |
| 11  | **Trefethen & Bau — Numerical Linear Algebra**                           | Numerical Linear Algebra            | ❌ Missing   |
| 12  | **Hamilton — Time Series Analysis**                                      | Time Series / Quant Research        | 📁 Available |
| 13  | **Williams — Probability with Martingales**                              | Martingales / Stochastic Processes  | ❌ Missing   |
| 14  | **Shreve I — Stochastic Calculus for Finance I**                         | Stochastic Calculus                 | 🌐 External  |
| 15  | **Shreve II — Stochastic Calculus for Finance II**                       | Mathematical Finance                | 🌐 External  |
| 16  | **Glasserman — Monte Carlo Methods in Financial Engineering**            | Monte Carlo / Computational Finance | ❌ Missing   |
| 17  | **Hull — Options, Futures, and Other Derivatives**                       | Derivatives / Finance               | 📁 Available |
| 18  | **Farlow — Partial Differential Equations for Scientists and Engineers** | PDEs / Derivatives                  | ❌ Missing   |

---

# Current Folder

The PDF files in this folder constitute the primary study library.

The folder currently contains the books marked:

> 📁 Available

The two Shreve books are available separately through the external GitHub repository being used for this study.

The remaining four books have not yet been acquired.

---

# Study Philosophy

This is **not** a "read 18 books cover-to-cover" curriculum.

The objective is to learn the mathematics required for quant work as efficiently as possible.

Some books will be studied deeply.

Some will be used selectively.

Some will primarily serve as references.

The important thing is **mastery of the relevant mathematics**, not completion of every page.

---

# Recommended Order

The books should not be studied in the numerical order shown above.

The recommended dependency order is:

```text
Guichard
Single and Multivariable Calculus
        │
        ├───────────────┐
        ▼               ▼
Velleman             Strang
Proofs               Linear Algebra
        │               │
        └───────┬───────┘
                ▼
       Boyce & DiPrima
              ODEs
                │
                ▼
             Ross
          Probability
                │
        ┌───────┴────────┐
        ▼                ▼
 Casella & Berger    Abbott
 Statistics       Real Analysis
        │                │
        │                ▼
        │             Axler
        │        Measure Theory
        │                │
        └───────┬────────┘
                ▼
     Williams / Advanced
        Probability
                │
        ┌───────┴─────────┐
        ▼                 ▼
    Hamilton          Shreve I
  Time Series       Stochastic Calc.
        │                 │
        │                 ▼
        │             Shreve II
        │         Mathematical Finance
        │
        ▼
Boyd & Vandenberghe
      Optimization
        │
        ▼
Burden & Faires
 Numerical Analysis
        │
        ▼
Trefethen & Bau
 Numerical Linear Algebra
        │
        ▼
Glasserman
 Monte Carlo
        │
        ├───────────────┐
        ▼               ▼
     Farlow           Hull
       PDEs          Derivatives
```
