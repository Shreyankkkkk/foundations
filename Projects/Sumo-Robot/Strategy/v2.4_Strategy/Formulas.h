#ifndef FORMULAS_H
#define FORMULAS_H
// Everything here is CALCULATED from Hardware.h. Do not type numbers here.

// ---- arena ----
const float ARENA_RADIUS_CM = (ARENA_TOTAL_DIAMETER_CM - 2.0f * ARENA_FRAME_THICKNESS_CM) / 2.0f;         // 72 black surface
const float ARENA_OUT_RADIUS_CM = ARENA_TOTAL_DIAMETER_CM / 2.0f;                                         // 75 disqualifying radius
const float START_LINE_FAR_EDGE_RADIUS_CM = START_LINE_CENTER_RADIUS_CM + START_LINE_THICKNESS_CM / 2.0f; // 11
const float START_LATERAL_SPREAD_MAX_CM = START_LINE_LENGTH_CM;

// ---- robot geometry from the 4 ruler measurements ----
const float ROBOT_L_B_CM = REAR_TO_AXLE_CM;
const float ROBOT_L_F_CM = ROBOT_LENGTH_CM - REAR_TO_AXLE_CM;
const float EDGE_SENSOR_FRONT_OFFSET_CM = ROBOT_L_F_CM - WEDGE_TO_FRONT_SENSOR_CM;
const float EDGE_SENSOR_BACK_OFFSET_CM = ROBOT_L_B_CM - REAR_TO_BACK_SENSOR_CM;
const float ROBOT_R_SWING_CM = fmaxf(hypotf(ROBOT_WIDTH_CM / 2.0f, ROBOT_L_F_CM), hypotf(ROBOT_WIDTH_CM / 2.0f, ROBOT_L_B_CM));
const float EDGE_SENSOR_REACH_MARGIN_CM = ARENA_OUT_RADIUS_CM - ARENA_RADIUS_CM;
const float START_POSE_RADIUS_CM = START_LINE_FAR_EDGE_RADIUS_CM + ROBOT_L_F_CM;
const float START_OPPONENT_WORST_CASE_LONG_CM = 2.0f * START_LINE_FAR_EDGE_RADIUS_CM + ROBOT_L_F_CM;
const float OPEN_SWEEP_HALF_ANGLE_DEG = atanf(START_LATERAL_SPREAD_MAX_CM / START_OPPONENT_WORST_CASE_LONG_CM) * RAD_TO_DEG + THETA0_UNCERTAINTY_DEG;

// ---- motion ----
const float DRIVE_DECEL_CMS2 = (DRIVE_SPEED_MAX_CMS * DRIVE_SPEED_MAX_CMS) / (2.0f * STOP_DISTANCE_CM); // v^2 = 2ad
const float COMMIT_SOFT_START_S = DRIVE_SPEED_MAX_CMS / (FRICTION_MU * 981.0f);                         // t = v/(mu*g)
const float MOTOR_SLEW_PWM_PER_MS = DRIVE_PWM_MAX / (COMMIT_SOFT_START_S * 1000.0f);

// ---- opponent thresholds: measured-through-divider values, or old bench x divider ratio ----
const int WEAK_THRESHOLD = USE_MEASURED_THRESHOLDS ? MEASURED_WEAK : (int)(BENCH_NO_OBJECT_MAX * SENSOR_DIVIDER_RATIO * 1.5f); // floor +50%
const int CONTACT_BAND_LOW = USE_MEASURED_THRESHOLDS ? MEASURED_CONTACT_LOW : (int)(BENCH_CONTACT_LOW * SENSOR_DIVIDER_RATIO + 0.5f);
const int CONTACT_BAND_HIGH = USE_MEASURED_THRESHOLDS ? MEASURED_CONTACT_HIGH : (int)(BENCH_CONTACT_HIGH * SENSOR_DIVIDER_RATIO + 0.5f);
const int PEAK_BAND_LOW = USE_MEASURED_THRESHOLDS ? MEASURED_PEAK_LOW : (int)(BENCH_PEAK_LOW * SENSOR_DIVIDER_RATIO + 0.5f);
const int PEAK_BAND_HIGH = USE_MEASURED_THRESHOLDS ? MEASURED_PEAK_HIGH : (int)(BENCH_PEAK_HIGH * SENSOR_DIVIDER_RATIO + 0.5f);
const int STRONG_THRESHOLD = CONTACT_BAND_LOW;
const int NEAR_THRESHOLD = (CONTACT_BAND_HIGH + PEAK_BAND_LOW) / 2;
static_assert(CONTACT_BAND_HIGH < PEAK_BAND_LOW, "Peak band must sit above the contact band");
static_assert(WEAK_THRESHOLD < STRONG_THRESHOLD && STRONG_THRESHOLD < NEAR_THRESHOLD, "Thresholds must be ordered WEAK < STRONG < NEAR");

// ---- sensor timing ----
const unsigned long SENSOR_SAMPLE_INTERVAL_MS = (unsigned long)ceilf((SENSOR_REFRESH_NOMINAL_MS - SENSOR_REFRESH_JITTER_MS) / 2.0f);
const int WEAK_CONFIRM_SAMPLES = (int)ceilf((SENSOR_REFRESH_NOMINAL_MS + SENSOR_REFRESH_JITTER_MS) / (float)SENSOR_SAMPLE_INTERVAL_MS);
const int CLEAR_CONFIRM_SAMPLES = STRONG_CONFIRM_SAMPLES;
const unsigned long LOST_CONTACT_GRACE_MS = (unsigned long)fmaxf(WEAK_CONFIRM_SAMPLES * (float)SENSOR_SAMPLE_INTERVAL_MS, LOST_CONTACT_GRACE_FLOOR_MS);
const unsigned long EDGE_CAL_MS = 2UL * SENSOR_SAMPLE_INTERVAL_MS; // edge-polarity check window

// ---- ADC noise filter: N = (sigma / target)^2, odd, 3..15 ----
const int ADC_MIN_THRESHOLD_GAP = ((NEAR_THRESHOLD - CONTACT_BAND_HIGH) < (STRONG_THRESHOLD - WEAK_THRESHOLD)) ? (NEAR_THRESHOLD - CONTACT_BAND_HIGH) : (STRONG_THRESHOLD - WEAK_THRESHOLD);
const float ADC_NOISE_SIGMA_TARGET = ADC_MIN_THRESHOLD_GAP / 6.0f;
const int ADC_OVERSAMPLE_MAX = 15;
const int ADC_OVERSAMPLE_N = ((int)constrain(ceilf((ADC_NOISE_SIGMA / ADC_NOISE_SIGMA_TARGET) * (ADC_NOISE_SIGMA / ADC_NOISE_SIGMA_TARGET)), 3.0f, (float)ADC_OVERSAMPLE_MAX)) | 1;

// ---- start sequence / switch ----
const unsigned long START_COUNTDOWN_MS = START_DELAY_MS + START_DELAY_MARGIN_MS;
const unsigned long REARM_HOLD_MS = 10UL * BUTTON_DEBOUNCE_MS;                                // 300 ms: OFF must persist so a hit can't stop us
const int START_SWITCH_ON_ADC = (int)(((5.0f / 2.0f) / 3.3f) * ((1 << SENSOR_ADC_BITS) - 1)); // ~775 (divided 5V); 3.3V feed reads ~1023, also above threshold
const int START_SWITCH_THRESHOLD_ADC = START_SWITCH_ON_ADC / 2;

// ---- search / align ----
const float SEARCH_SPIN_CAP_DEGS = (2.0f * atanf((ROBOT_WIDTH_CM / 2.0f) / DETECT_RANGE_MAX_CM) * RAD_TO_DEG) / ((SENSOR_REFRESH_NOMINAL_MS + WEAK_CONFIRM_SAMPLES * (float)SENSOR_SAMPLE_INTERVAL_MS) / 1000.0f);
const int SEARCH_SPIN_PWM = (int)constrain(255.0f * (SEARCH_SPIN_CAP_DEGS / fminf(SPIN_RATE_CW_DEGS, SPIN_RATE_CCW_DEGS)), 0.0f, 255.0f);
const float SEARCH_ACTUAL_SPIN_DEGS = fminf(SEARCH_SPIN_CAP_DEGS, fminf(SPIN_RATE_CW_DEGS, SPIN_RATE_CCW_DEGS));
const unsigned long OPEN_SWEEP_LEG_A_MS = (unsigned long)((OPEN_SWEEP_HALF_ANGLE_DEG / SEARCH_ACTUAL_SPIN_DEGS) * 1000.0f);
const unsigned long OPEN_SWEEP_LEG_B_MS = 2UL * OPEN_SWEEP_LEG_A_MS;
const float ALIGN_ACTUAL_SPIN_DEGS = fminf(SPIN_RATE_CW_DEGS, SPIN_RATE_CCW_DEGS) * (ALIGN_BASE_SPEED / 255.0f);
const unsigned long ALIGN_TIMEOUT_MS = (unsigned long)(45.0f / ALIGN_ACTUAL_SPIN_DEGS * 1000.0f);
const float SEARCH_COVERAGE_SWEEP_DEG = 360.0f - 90.0f;
const unsigned long SEARCH_DWELL_MS = (unsigned long)(WEAK_CONFIRM_SAMPLES * SENSOR_SAMPLE_INTERVAL_MS);

// ---- stalemate ----
const float STALEMATE_BACKOFF_CM = DRIVE_SPEED_MAX_CMS * (EDGE_RECOVER_SPEED / 255.0f) * (STALEMATE_BACKOFF_MS / 1000.0f);
static_assert(STALEMATE_TIMEOUT_MS + STALEMATE_BACKOFF_MS < STALEMATE_HARD_CEILING_MS, "Stalemate cycle must stay under rule 6.6.D's 30s ceiling");

#endif
