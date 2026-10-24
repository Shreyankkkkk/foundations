# Simple Breaks (TradingView indicator)

A Pine Script v6 overlay indicator (short title `MTF BREAK`) that marks swing breaks, protected highs/lows and "no close + sweep" (NC + S) on the chart you are viewing. It exists to make the owner's top-down structure rules mechanical, so entries are less emotional and less over-thought. It does not implement MSS, BOS or other structure systems.

## Files
- `simple_breaks.pine`: the indicator source.
- `STATE.md`: current rules, inputs, known issues, next steps. Read this first.
- `LOG.md`: dated change history (one line per change, newest at the bottom).
- `docs/indicator-settings-xauusd-4h.png`: screenshot of the settings panel on XAUUSD 4H.

## How to use
1. In TradingView open the Pine Editor, paste `simple_breaks.pine`, click Add to chart.
2. Tick the timeframes you want under "Visible Timeframes". Only breaks from the chart's own timeframe are drawn, so tick the one you are viewing.
3. Settings used in the screenshot: maximum visible breaks 6, NC + S marks 6, swing age 48 bars, doji threshold 10%, dotted lines.

## What it marks (short version)
- Swing HIGH: at least 2 bullish then 2 bearish candles. Swing LOW is the mirror. Level is the extreme wick.
- Break: the swing level is touched; the candle body must cross the 50% point (`close >= 2*level - open` for a HIGH). If it misses, later same-direction candles can still confirm it.
- NC + S: the first test missed and a real opposite candle ended the attempt (uses its own 1-2 / 2-1 swing rule).
- Protected High / Low: the extreme wick between the swing pivot and the break candle.
- A doji (body at or below 10% of range by default) never starts or confirms a test.
- If a higher selected timeframe marks the same swing, the lower one is hidden.

Full rules: `STATE.md`.

## Known issues
- Memory error on charts of 3 hours and above was reported and a mitigation applied; not confirmed fixed.
- Only 1,000 bars per timeframe are calculated, so older breaks can be missing.
- No Pine compiler was available while writing, so check compile and behaviour in TradingView.

## Licence / origin
The first line of the file carries the Mozilla Public License 2.0 header from the script it was adapted from. Confirm the original source and its terms before relying on this repo being fully original.
