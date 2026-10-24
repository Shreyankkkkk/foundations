# CODEMAP simple-breaks (auto-generated) | L<n> = line number
projects/simple-breaks/Simple Breaks.pine
  indicator "Simple Breaks — Selectable Timeframes" L3
  f_line_style(string style) L71
  f_range_extreme(int startTime, int endTime, bool findHigh) L77
  f_remove_aligned_nc(float protectedPrice, int protectedStart, int protectedEnd, array<line> ncLines, array<label> ncLabels) L91
  f_is_protected_level(float level, int eventStart, int eventEnd, array<line> protectedLines) L103
  type TFEvent L114
  f_is_duplicate(int direction, float level, int pivotTime, int timeframeSeconds, array<int> higherDirections, array<float> higherLevels, array<int> higherTimes, array<int> higherDurations, array<int> higherRanks) L131
  f_register_higher_break(bool triggered, int direction, float level, int eventTime, int pivotTime, int timeframeSeconds, array<string> keys, array<int> higherDirections, array<float> higherLevels, array<int> higherTimes, array<int> higherDurations, array<int> higherRanks, array<line> breakLines, array<label> breakLabels, array<label> protectedLabels, array<line> protectedLines, array<int> breakDirections, array<float> breakLevels, array<int> breakTimes, array<int> breakRanks) L143
  f_track_timeframe(TFEvent event, bool selected, int timeframeSeconds) L184
  f_tf_events() L188
  f_request_events(string sourceTf, bool selected, int timeframeSeconds) L594
  f_draw(string tfName, string sourceTf, int tfSeconds, bool enabled, string style, int width, bool newHigh, float highPrice, int highTime, bool newLow, float lowPrice, int lowTime, bool bullBreak, bool bearBreak, bool ncSweep, int bullEventTime, float bullEventLevel, int bearEventTime, float bearEventLevel, int bullStartTime, int bearStartTime, array<line> breakLines, array<label> breakLabels, array<label> protectedLabels, array<int> breakDirections, array<float> breakLevels, array<int> breakTimes, array<int> breakRanks, array<int> higherDirections, array<float> higherLevels, array<int> higherTimes, array<int> higherDurations, array<int> higherRanks, array<line> ncLines, array<label> ncLabels, int maxVisibleBreaks, int maxVisibleNCS) L637
