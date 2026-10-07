#ifndef MAP_H
#define MAP_H
#include "Hardware.h"

struct Pose
{
    float x, y, thetaDeg;
}; // cm from arena center; thetaDeg: 0=+x axis, CCW positive (standard math convention)

void initMap(); // resets pose to start position, U to U0, all uncertainty accumulators to 0

// THE motion layer — call once per tick with the PWM values just sent to drive().
// Handles pure spin, pure translation, and blended motion (e.g. commit + track correction)
// through one differential-drive model. NOT for use while anyContact() is true — use
// mapUpdateContact() instead during actual pushing contact.
void mapUpdateMotion(int leftPwm, int rightPwm, unsigned long dtMs);

// Contact-mode update: wheel slip during a push is unbounded and unmeasurable, so this
// assumes best-effort straight movement along the current heading at DRIVE_SPEED_MAX_CMS,
// freezes theta (track-correction trim is not modeled here), and inflates uncertainty
// directly and fast. Call every tick that anyContact() is true.
void mapUpdateContact(unsigned long dtMs);

// Ground-truth correction: call once, right when an edge sensor first fires, before backing off.
// Forces the triggering sensor's position to ARENA_RADIUS_CM at its current angle, backs out M,
// and resets all uncertainty accumulators — this is the only source of ground truth we have.
void mapSnapEdge(bool frontTriggered);

Pose getPose();
float getRadiusFromCenter();   // hypot(x,y)
float getUncertainty();        // U
float getFootprintMaxRadius(); // farthest footprint corner's distance from arena center, given current pose
bool isMapVoid();              // true once U alone could exceed our stopping margin — check this FIRST

// True only when the map confidently rules out being at the real boundary — use ONLY to
// suppress false triggers from a worn/patchy arena surface, NEVER to suppress a trusted reading.
bool isEdgeReadingImplausible();

float getReturnHeadingDeg();   // absolute heading to face arena center
float getReturnTurnDeltaDeg(); // shortest signed turn from current theta to face center, [-180,180]
bool shouldReturn();           // r > U + ROBOT_WIDTH_CM/2 — only meaningful when NOT void

float getGovernedMaxSpeedCms(); // speed cap so the robot can still stop before the rim, given current U and r_max

// Phantom gate — ONLY valid for weak-band (far, ambiguous) detections. A strong/contact-band
// reading physically cannot originate beyond the arena, so never gate those.
// whichSensor: -1 = left, 0 = center, +1 = right.
bool isPhantomDetection(int whichSensor, int rawAdc);

float getRearMaxRadius(); // farthest rear corner's distance from arena center

#endif