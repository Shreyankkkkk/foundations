# Simple Breaks — Project State

Status: in progress. Current Pine Script source: `Simple Breaks.pine` (Pine Script v6).
Last recorded source edits: 2026-10-23. TradingView compilation and runtime behavior have not been confirmed after those edits.

## Goal

Build a TradingView overlay indicator that marks the user's simple swing HIGH / LOW breaks. The indicator is not intended to implement MSS, BOS, or other structure systems.

## Current break rules

- A swing HIGH requires at least two consecutive bullish candles followed by at least two consecutive bearish candles. Its level is the highest wick in that reversal structure.
- A swing LOW requires at least two consecutive bearish candles followed by at least two consecutive bullish candles. Its level is the lowest wick in that structure.
- Break swings use the 2–2 pattern to avoid promoting smaller internal reversals; no separate minimum swing size applies beyond that candle pattern.
- Dojis inherit the previous non-doji candle's direction for counting consecutive candles.
- A swing can be tested only once. A doji (body at or below the configurable 10% of candle-range threshold by default) touching the level is ignored and does not start the test. If the first real candle touching the level misses, the same-direction continuation remains pending until it either meets the break body threshold or a real opposite-direction candle ends the attempt; then that swing is consumed.
- Break confirmation is based on the candle body's relation to the swing level. For a HIGH, the close must be at or above the 50% body threshold; for a LOW, the close must be at or below it. For a single candle this is evaluated as `close >= 2 * level - open` (HIGH) or `close <= 2 * level - open` (LOW).
- If the first-touch candle misses the threshold, each subsequent real candle continuing in the break direction is checked. A candle qualifies if either the combined first-touch-open to current-close body or the current candle's own body reaches the 50% threshold. This continues until a break qualifies or a real opposite-direction candle ends the attempt.
- If the first-touch candle misses and the directional sequence later ends with a real opposite-direction candle, the event is labeled `{timeframe} NC + S` (for example, `1H NC + S`) and drawn in neutral gray. Dojis cannot start or confirm a test, trigger NC + S, or end a pending continuation; they are skipped until the next real candle.
- NC + S uses its own stored swing records and keeps the 1–2 / 2–1 reversal qualification: a HIGH uses bullish then bearish runs, and a LOW uses bearish then bullish runs. Its swing level is the highest/lowest wick across the two runs; dojis inherit the prior non-doji direction.
- On a bearish break, the highest wick from the LOW swing pivot through the break candle is marked `{timeframe} Protected High`. On a bullish break, the lowest wick from the HIGH swing pivot through the break candle is marked `{timeframe} Protected Low`.
- Protected High/Low is drawn as a horizontal level from the extreme wick to the break candle, with the same endpoint as the BREAK line. NC + S cannot overlap a protected structure in both price and time; same-price NC + S marks at other times remain valid.
- A doji may count toward swing-pattern runs by inheriting the prior non-doji direction, but it is excluded from first-touch and break/NC + S body evaluation.

## Display and inputs

- Overlay drawings are placed on the price chart.
- Break and NC + S lines stop at their event candle. Their text sits left of and below the line's starting point.
- Protected High/Low lines run from the protected wick to the break candle and stop there; their lines and labels are removed when the associated break leaves the visible-break buffer or is suppressed by a higher-timeframe match.
- Break labels read `{timeframe} Break` for both directions, positioned left of and below the line start; bullish/bearish colors identify direction. NC + S labels use the same left-below-start placement. Protected structure lines have separate configurable color and solid/dashed/dotted style settings; labels use the selected protected color.
- Bullish breaks default to green; bearish breaks default to red. Both colors are user-configurable.
- The default visible-break count is two and can be changed by the user.
- NC + S has its own independent visible-mark count, defaulting to two; setting it to zero hides NC + S marks.
- The swing-to-first-test age limit is configurable. Current source default is 96 bars; the user has also used 48 bars.
- The doji body-to-range threshold is configurable and defaults to 10%.
- One general line style and line width apply to all selected timeframes.
- Timeframe checkboxes cover 1, 2, 3, 5, 10, 15, 30, and 45 minutes; 1, 2, 3, and 4 hours; daily, weekly; and 1, 3, 6, and 12 months.
- Only breaks from the chart's current timeframe are drawn, provided that timeframe is selected.
- If a lower-timeframe break matches the same structural point as a selected higher-timeframe break, the higher-timeframe break takes precedence and the lower-timeframe mark is suppressed.
- Alerts were removed at the user's request.

## Current implementation notes

- Main implementation is in `Simple Breaks.pine`.
- Swing detection and break logic run in the requested source timeframe. The drawing context receives a six-value scalar tuple per timeframe rather than a returned array or custom object.
- Dynamic requests are conditional on the timeframe being selected and not lower than the chart timeframe.
- `request.security()` currently uses `calc_bars_count=1000` to limit requested history and memory use.
- The script retains a bounded set of swing records per side while waiting for first tests.
- Current break continuation requires actual bullish / bearish candles; after the first touch, the pending test remains active across same-direction candles until a candle qualifies or a real opposite candle ends the sequence. Dojis neither confirm nor end it. The swing-age limit applies before the first touch, not during the pending continuation.
- NC + S is now returned through the same scalar event tuple and drawn only on its own selected chart timeframe. Its candidates are independent of the Break swing arrays.
- The `TFEvent` type has one `ncSweep` field at the end, matching the added constructor argument.
- BREAK and NC + S drawings use separate line/label arrays and separate visible-count inputs. BREAK count also retains its protected labels; both counts are capped at 166 so combined visible labels stay within TradingView's 500-label limit.
- Protected extremes are calculated from a bounded chart-timeframe OHLC history sized to the swing-age input plus a small margin; only the exact current chart timeframe is drawn.
- Protected levels are tracked alongside their BREAK drawings. NC + S events are checked against active protected levels using configured tick tolerance and time-range overlap, preventing the same structure from being marked both ways without suppressing unrelated swings at the same price.

## Known issues and caveats

- The user has repeatedly reported `Runtime Error - Memory Limit Exceeded` on chart timeframes of 3 hours and above. The latest scalar-request and 1,000-bar changes are an evidence-based mitigation, not yet confirmed as a resolution in TradingView.
- Limiting requests to 1,000 source bars can hide older breaks outside that calculation history.
- The latest source ignores doji candles when starting or evaluating a break/NC + S test; dojis still inherit direction for swing-pattern runs. The user has not yet verified this revision in TradingView.
- The pending continuation now lasts until a real opposite-direction candle; verify this behavior on the user's manually marked HTF example.
- Protected-point/NC + S overlap uses price tolerance and intersection of the two finite line time ranges.
- There is no TradingView compiler/runtime available in this workspace; Pine compilation and chart behavior must be checked in TradingView.

## Key decisions

- Preserve the original script's chart-overlay drawing approach and modify only its break criteria and requested display behavior.
- Use 2–2 reversal-run qualification for Break swings and 1–2 / 2–1 qualification for NC + S, with separate records and their existing distinct first-test outcomes.
- Treat the first level touch as decisive; do not keep an unbroken swing level extended indefinitely.
- Use a time-based age limit to prevent extremely old lower-timeframe swings from remaining eligible.

## Next steps

1. Paste the latest `Simple Breaks.pine` into TradingView and verify it compiles.
2. Recheck the screenshot case on 1H and confirm dojis no longer trigger a break.
3. Retest 3H and higher charts for memory errors; if the error remains, capture the exact runtime panel and test a lower `calc_bars_count` or reduce active requested timeframes.
4. Confirm whether the 1,000-bar request window is sufficient for the latest two breaks across all selected timeframes.
5. Verify the consecutive-candle continuation and NC + S termination behavior on the user's manually marked HTF example.
