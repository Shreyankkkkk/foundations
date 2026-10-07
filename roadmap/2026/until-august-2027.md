# The Long Runway: Oct 3, 2026 → Aug 1, 2027
### What five years of this actually requires you to start now — not everything, just the next honest layer

This file starts where the summer file ends. It does not touch data analysis basics or the sumo robot — those are locked into the summer file and done by Oct 3. This is the next queue: one item at a time, same rule as always, just paced for a year that also has university in it.

The reasoning behind the order hasn't changed from what's already been said: finance fundamentals before statistics (a p-value on returns means nothing if you don't know what a return is), probability and linear algebra before anything resembling machine learning, and the heaviest, most infrastructure-dependent stuff (HFT, derivatives pricing at depth) pushed out past this window entirely — not because they're not worth doing, but because doing them properly requires everything above them to already be solid, and you have a degree running in parallel.

---

## The Queue (Oct 3, 2026 → Aug 1, 2027)

### 1. SQL
**Tools/libraries:** SQLite, `sqlite3` (Python standard library)
**What specifically:** schema design (primary/foreign keys, normalization to 3NF), `CREATE TABLE` / `ALTER TABLE`, `INSERT` / `UPDATE` / `DELETE`, `JOIN` (inner, left), `GROUP BY` + aggregate functions, indexes and why they matter for query speed, parameterized queries in Python to avoid SQL injection
**Resource:** CS50's Introduction to Databases with SQL (Harvard)
**Done when:** you can design a 3-table schema from scratch on paper, implement it, and write joins/aggregates without looking up syntax.

### 2. Finance fundamentals
**Tools/libraries:** none — this is conceptual, done through lecture + reading a real 10-K/annual report
**What specifically:** what a stock, bond, and derivative actually are; balance sheet, income statement, cash flow statement; revenue vs. operating profit vs. net income; what a valuation is and the basic idea of discounting future cash flows
**Resource:** Aswath Damodaran's Corporate Finance lectures (NYU Stern, free)
**Done when:** you can read one company's annual report and explain its financial position in plain English without hedging.

### 3. Probability
**Tools/libraries:** Python (`numpy`, `scipy.stats` for verifying calculations by hand-work first)
**What specifically:** random variables, discrete vs. continuous distributions (binomial, normal, Poisson), expectation and variance, conditional probability, Bayes' theorem, joint/marginal distributions
**Resource:** Harvard Stat 110 (Blitzstein)
**Done when:** you can compute expected value and variance of a real dataset (e.g. your own trade P&L) by hand, then verify it in code.

### 4. Statistics & regression for finance
**Tools/libraries:** `pandas`, `statsmodels` or `scipy.stats`, `matplotlib`
**What specifically:** hypothesis testing, null/alternative hypotheses, t-statistics and p-values, confidence intervals, ordinary least squares (OLS) regression, interpreting R², residuals
**Resource:** *Introductory Econometrics for Finance* — Chris Brooks, Chapters 2–3 (and later chapters as needed)
**Done when:** you can run a t-test on your own trading data and explain, in plain language, whether your edge is statistically distinguishable from noise.

### 5. Linear algebra
**Tools/libraries:** `numpy` (arrays, matrix operations, `numpy.linalg`)
**What specifically:** vectors and matrices, matrix multiplication, determinants, eigenvalues and eigenvectors, covariance matrices, an intuitive grasp of what an eigenvalue *means* for a covariance matrix (which direction carries the most variance)
**Resource:** MIT OpenCourseWare 18.06 — Gilbert Strang
**Done when:** you can compute the covariance matrix of 3 assets' returns, find its eigenvalues, and explain what the largest one represents.

### 6. APIs and live data
**Tools/libraries:** `requests` (REST APIs), a market data provider's free tier (Yahoo Finance API, EODHD, or Binance for crypto), basic `websockets` if you go the live-feed route
**What specifically:** REST vs. WebSocket, JSON parsing, authentication headers, rate limiting and why you respect it, writing a script that fetches OHLCV data and stores it via the SQL work from item 1
**Done when:** you have a script that pulls live/historical price data for 3+ tickers and writes it cleanly into your database, handling rate limits without crashing.

### 7. Research paper literacy (3 papers)
**Tools/libraries:** none additional — this is reading + replicating small pieces in `pandas`/`numpy`
**What specifically, in order:**
- Cont (2001), *Empirical Properties of Asset Returns* — the "stylized facts" of real return data (fat tails, volatility clustering); test each fact against your own traded assets
- Park & Irwin (2007), *The Profitability of Technical Analysis: A Review* — data-snooping bias and survivorship bias, and how they distort backtest results
- Hurst, Ooi & Pedersen (2013), *A Century of Evidence on Trend Following Investing* — extract and implement their core trend signal in Python on one asset class
**Done when:** each paper has a short written breakdown (claim → your test on real data → result) committed to your repo.

### 8. Light C++ introduction
**Tools/libraries:** g++ or clang, no frameworks yet
**What specifically:** syntax differences from Python, compilation vs. interpretation, basic memory concepts (stack vs. heap, what a pointer is conceptually — not pointer arithmetic gymnastics), why performance-critical code sometimes needs it
**Resource:** QuantStart's free C++ for quant finance articles
**Done when:** you can write, compile, and run a simple numeric program (e.g. a basic Monte Carlo loop) in C++ and explain why it runs faster than the Python equivalent.
**Note:** keep this light. CSCI291 will likely go deeper — this is just enough to not be starting from zero when it does.

### 9. Machine learning foundations (only if items 1–8 are solid — this is the stretch goal for the tail end of the window)
**Tools/libraries:** `scikit-learn`, `pandas`, `matplotlib`
**What specifically:** train/test split and why it exists, linear regression and logistic regression as your two first models, overfitting vs. underfitting, cross-validation, and — critically — *why* a model's output isn't automatically trustworthy just because it ran without errors
**Done when:** you've trained and evaluated one regression and one classification model on a real dataset, and can explain what would make you *not* trust the result.

---

## Small carry-over items (slot in whenever, low priority, low effort)
These don't need a dedicated queue position — they're finite side projects for whenever you want a break from the main queue without touching new territory:
- **Monte Carlo dissection:** go back through your old refactored 8-file Monte Carlo simulator and understand/fix it properly, now that items 1–5 give you the math to actually evaluate it
- **Notion trade logger automation:** small script to pull your weekly EURUSD/AUDUSD/XAUUSD data entry into something semi-automated (your actual trade journal stays manual, as decided)

---

## Beyond 2027
### Things that are real, worth doing eventually, and too much to stack on top of a working degree and this queue

**High-Frequency Trading prototype (full version)**
**Tools/libraries this actually requires:** `asyncio`, `websockets`/`aiohttp`/`uvloop` for concurrent I/O, Cython or C++ bindings for hot-path code, lock-free ring buffers for tick queues, Redis for in-memory state, TimescaleDB or DuckDB for tick-history storage, a custom event-driven backtester (standard backtesting libraries don't model queue position or market impact correctly)
**Why it's here and not in the queue:** this list alone is close to a semester's worth of systems programming on top of everything in items 1–9. It's not "impossible," it's sequenced wrong to attempt now — market microstructure (order books, bid-ask mechanics, order types) and inventory risk concepts also need to exist before any of this is meaningful rather than cargo-culted.

**Financial Engineering & Derivatives Pricing**
**Tools/libraries:** more advanced calculus/stochastic calculus, `numpy`/`scipy` for numerical pricing methods
**What it covers:** Black-Scholes and options pricing math, derivative structures, systemic risk management
**Resource when ready:** Columbia's Financial Engineering and Risk Management Part I (Coursera, audit free)
**Why later:** genuinely requires items 3–5 (probability, stats, linear algebra) to be deep, not just completed.

**Quantitative Modeling Foundations (Wharton) / advanced regression & risk frameworks**
Same logic — valuable, but it's consolidation-level material that means more once items 1–9 aren't fresh but *internalized*.

**Deep learning / LLM internals, if you want to go there**
`PyTorch`, transformer architecture, attention mechanisms — genuinely a separate multi-month track on its own, only worth starting once classical ML foundations (item 9) are solid, not skipped to.

**Signal processing & control theory**
These aren't being "added" — they're ECTE203 (Year 3) and ECTE344 (Year 4) in your actual degree. Nothing to pre-learn here; your math foundation from this queue makes them land better when they arrive on schedule.

---

## One honest note on pacing
Nine items across roughly 10 months, with university running for most of it, is a real pace — not a light one. If item 4 or 5 takes longer than expected because a trimester gets heavy, that's not the plan failing, that's the plan being realistic about the fact you have a degree to also actually do. The five-year version of this doesn't require items 1–9 to land by Aug 1, 2027 on the dot — it requires you to still be moving through the queue in good order a year from now, the same way Python-basics-then-git proved you could.
