#ifndef ROBOT_H
#define ROBOT_H

// Keep this interface independent of the sensor implementation. Source files
// that define these functions include Sensors.h before Robot.h.
struct OpponentReadings;
struct EdgeReadings;

enum TargetSide {
    TARGET_NONE,
    TARGET_LEFT,
    TARGET_RIGHT,
    TARGET_FRONT
};

enum SearchDirection {
    SEARCH_LEFT,
    SEARCH_RIGHT
};

// ===================== START TUNABLES =====================
// Rulebook 6.2 requires five seconds stationary; 7.3 makes moving early a
// warning, and three warnings loses the round. Being LATE costs nothing, so
// this carries deliberate margin over 5000 ms.
const unsigned long START_COUNTDOWN_MS          = 5200;
const unsigned long START_DEBOUNCE_MS           = 50;
const unsigned long START_EDGE_CHECK_INTERVAL_MS = 5;

// ===================== SEARCH TUNABLES =====================
const int SEARCH_SLOW_SPEED = 120;
const int SEARCH_FAST_SPEED = 180;

// First arc from the border is shorter, to turn inward from the start line.
const unsigned long SEARCH_FIRST_ARC_MS = 600;
// Standard arc time to maintain the S-curve across the ring.
const unsigned long SEARCH_ARC_FLIP_MS  = 1100;

// ===================== APPROACH / ATTACK TUNABLES =====================
const int APPROACH_SPEED = 165;
const int TURN_SPEED     = 100;
const int ATTACK_SPEED   = 240;

// How long the robot must read as squared-up before it commits to a charge.
// Guards against charging off a single lucky sample.
const unsigned long SQUARED_CONFIRM_MS = 60;

// THE BLIND-ZONE FIX.
//
// The GP2Y0A21 cannot see closer than about 10 cm — its output actually
// falls again below that distance. So the instant you make contact, the
// front readings collapse and naive code concludes the opponent vanished
// and drops back to searching, mid-push.
//
// Once attack() fires, the push is latched for this long regardless of what
// the front sensors report. The latch is cancelled early by an edge trigger
// (edgeRecover always wins) and refreshed whenever the sensors CAN still see
// the target, so a long clean push keeps extending itself.
//
// Tune against the ring: at ATTACK_SPEED you should not be able to cross
// more than roughly half the ring inside this window. The edge sensors are
// still the hard safety net.
const unsigned long ATTACK_COMMIT_MS = 500;

// ===================== EDGE RECOVERY TUNABLES =====================
const int EDGE_RECOVER_SPEED     = 170;
const int EDGE_RECOVER_MAX_SPEED = 230;

const unsigned long EDGE_BRAKE_MS         = 60;   // hard stop before reacting
const unsigned long EDGE_RETREAT_MS       = 180;  // straight retreat phase
const unsigned long EDGE_ESCALATE_MS      = 220;  // still triggered -> max power
const unsigned long EDGE_RECOVER_MAX_MS   = 700;  // still triggered -> fallback
const unsigned long EDGE_CONFIRM_CLEAR_MS = 30;   // confirmation before resuming

// ===================== STRATEGY 2 STEERING TUNABLES =====================
// Expressed in ADC counts, so they scale with ADC_MAX in Hardware.h.
// The values below assume the 12-bit setting; at 10 bits, divide by 4.
const int SIDE_TURN_MARGIN     = 100;
const int SIDE_TURN_HYSTERESIS = 40;
// Time-based, not loop-count based. The old cycle counter was satisfied in
// well under a millisecond and confirmed nothing.
const unsigned long SIDE_TURN_CONFIRM_MS = 50;

// ===================== REPOSITION TUNABLES =====================
const unsigned long REPOSITION_MS    = 300;
const int           REPOSITION_SPEED = 150;

// ===================== FUNCTIONS =====================
void initRobot();
void waitForStart();

// Drives both motors flat out AND latches the attack commit (see
// ATTACK_COMMIT_MS above). Calling it again while already attacking refreshes
// the latch rather than restarting it.
void attack();

// Keeps the charge going without refreshing the latch. This is what you call
// when the front sensors have gone quiet but the commit window is still open.
void holdAttack();

// True while the commit window from the last attack() is still open. The main
// loop MUST consult this before deciding a target was lost, otherwise contact
// range looks identical to an empty ring.
bool attackCommitted();

// Drops the latch immediately. Called automatically by edgeRecover() and
// waitForStart(); call it yourself if you deliberately abandon a push.
void cancelAttack();

// Corner-aware edge recovery. Returns:
//   false — the edge was confirmed clear and normal play can resume.
//   true  — recovery hit its time limit and fell back to a blind nudge.
//           The caller has lost its positional reference and should drop
//           back to SEARCH rather than resuming an approach.
bool edgeRecover(const EdgeReadings &edges);

// Nudges the robot to change its vantage point. `reverse` is the DIRECTION OF
// TRAVEL: true drives backwards, false drives forwards. It is not "which edge
// fired" — getting that backwards drives you off the ring.
// Returns true if the full nudge completed without meeting an edge.
bool reposition(bool reverse);

#endif
