# CODEMAP sumo-robot (auto-generated) | L<n> = line number
projects/sumo-robot/design/parametric/main_deck_PARAMETRIC_SOURCE.py
  box(cx, cy, z0, z1, w, l) L87
  cyl_z(cx, cy, z0, z1, d) L95
  cyl_y(cx, y0, y1, cz, d) L100
  cyl_x(x0, x1, cy, cz, d) L110
  add_bulkhead(deck, side, y0, y1) L141
  post(cx, cy, z0, z1, d, hole_d) L178
  add_driver_standoffs(deck, center) L197
projects/sumo-robot/firmware/strategy/v1.0_Strategy/Strategy_1.cpp
  beginSearchArc(SearchDirection initialDir) L14
  updateSearchArc() L20
  anyOpponentDetected(const OpponentReadings & readings) L36
  getTargetSide(const OpponentReadings & readings) L43
  approachTarget(const OpponentReadings & readings) L61
  getLastCorrection() L92
projects/sumo-robot/firmware/strategy/v1.0_Strategy/Strategy_2.cpp
  ApproachSteering L14
  beginSearchArc(SearchDirection initialDir) L25
  updateSearchArc() L35
  anyOpponentDetected(const OpponentReadings & readings) L51
  getTargetSide(const OpponentReadings & readings) L58
  approachTarget(const OpponentReadings & readings) L85
  getLastCorrection() L147
projects/sumo-robot/firmware/strategy/v1.1_Strategy/Motors.cpp
  initMotors() L28
  inhibitMotionUntil(unsigned long deadline) L58
  stopMotors() L63
  applySide(int speed,int rPwmPin,int lPwmPin) L68
  needsReversalBrake(int from,int to) L80
  drive(int leftSpeed,int rightSpeed) L87
  forward(int speed) L121
  backward(int speed) L126
  turnLeft(int speed) L132
  turnRight(int speed) L138
projects/sumo-robot/firmware/strategy/v1.1_Strategy/Robot.cpp
  initRobot() L22
  waitForStart() L30
  attack() L107
  holdAttack() L113
  attackCommitted() L117
  cancelAttack() L129
  edgeRecover(const EdgeReadings & edges) L138
  reposition(bool reverse) L254
projects/sumo-robot/firmware/strategy/v1.1_Strategy/Robot.h
  TargetSide L9
  SearchDirection L16
projects/sumo-robot/firmware/strategy/v1.1_Strategy/Sensors.cpp
  calibrateReading(int raw,int offset,int gain) L46
  medianBuffer(const int * buffer) L53
  recomputeCachedReadings() L70
  initSensors() L83
  initSensorDebug() L125
  printSensorDebug(OpponentReadings readings,EdgeReadings edges) L137
  readOpponentSensors() L153
  readEdgeSensorsRaw() L167
  readEdgeSensors() L176
  isOpponentDetected(int reading) L203
  anyEdgeDetected(EdgeReadings edges) L207
projects/sumo-robot/firmware/strategy/v1.1_Strategy/Sensors.h
  OpponentReadings L21
  EdgeReadings L29
projects/sumo-robot/firmware/strategy/v1.1_Strategy/Strategy_1.cpp
  beginSearchArc(SearchDirection initialDir) L16
  updateSearchArc() L26
  anyOpponentDetected(const OpponentReadings & readings) L44
  getTargetSide(const OpponentReadings & readings) L51
  approachTarget(const OpponentReadings & readings) L64
projects/sumo-robot/firmware/strategy/v1.1_Strategy/Strategy_2.cpp
  ApproachSteering L13
  clearPendingSteering() L29
  beginSearchArc(SearchDirection initialDir) L35
  updateSearchArc() L45
  anyOpponentDetected(const OpponentReadings & readings) L63
  getTargetSide(const OpponentReadings & readings) L70
  approachTarget(const OpponentReadings & readings) L83
projects/sumo-robot/firmware/strategy/v1.1_Strategy/v1.1_Strategy.ino
  setup() L12
  loop() L18
projects/sumo-robot/firmware/strategy/v1.2_Strategy/Motors.cpp
  initMotors() L13
  inhibitMotionUntil(unsigned long deadline) L41
  setMotorsEnabled(bool enabled) L50
  stopMotors() L56
  setSide(int rPwmPin,int lPwmPin,int speed) L62
  drive(int leftSpeed,int rightSpeed) L73
projects/sumo-robot/firmware/strategy/v1.2_Strategy/Robot.cpp
  startRawOn() L21
  roundRawOn() L24
  bothRawOn() L27
  startOn() L32
  switchesOn() L41
  abortAttack() L57
  initRobot() L61
  resetHammerState() L81
  hammerSpeed(int correction) L87
  commitAttack(int correction,int frontReading) L103
  hammerDrive(int correction) L109
  driveAwayFromEdge(const EdgeReadings & e,int speed,bool straight) L116
  repositionAway(bool goBack) L142
  edgeRecover(const EdgeReadings & edges) L156
  maneuverSafe(bool stopOnOpponent) L247
  executeManeuver(unsigned long pivotMs,unsigned long moveMs,bool pivotLeft,bool reverse,bool stopOnOpponent) L263
  executeBalancedOffset() L284
  executeRandomStart() L290
  pivotInPlace(unsigned long ms,bool pivotLeft,int speed) L297
  driveStraight(unsigned long ms,int speed) L307
  executeDiagonalStart() L320
  showSelfTest(bool sensorSeesWhite) L343
  waitForStart() L352
projects/sumo-robot/firmware/strategy/v1.2_Strategy/Robot.h
  SearchDirection L8
  StartRoutine L67
projects/sumo-robot/firmware/strategy/v1.2_Strategy/Sensors.cpp
  calibrateReading(int raw,int offset,int gain) L24
  medianBuffer(int * buffer) L29
  initSensors() L46
  primeOpponentSensors() L65
  readOpponentSensors() L76
  readEdgesOnce() L98
  readEdgeSensors() L109
  isOpponentDetected(int reading) L122
  anyEdgeDetected(EdgeReadings edges) L126
projects/sumo-robot/firmware/strategy/v1.2_Strategy/Sensors.h
  OpponentReadings L27
  EdgeReadings L36
projects/sumo-robot/firmware/strategy/v1.2_Strategy/Strategy_Hybrid.cpp
  beginSearchArc(SearchDirection initialDir) L20
  updateSearchArc() L35
  anyOpponentDetected(const OpponentReadings & readings) L51
  updateSideOverride(int requested) L65
  approachTarget(const OpponentReadings & r) L95
  getLastCorrection() L148
  getLastSeenDirection() L152
projects/sumo-robot/firmware/strategy/v1.2_Strategy/v1.2_Strategy.ino
  sensorDebug() L11
  setup() L51
  robotLoop() L60
  loop() L156
projects/sumo-robot/firmware/strategy/v1.3_Strategy/motors.cpp
  initMotors() L5
  stopMotors() L20
  setSide(int rPwmPin,int lPwmPin,int speed) L22
  drive(int leftSpeed,int rightSpeed) L27
projects/sumo-robot/firmware/strategy/v1.3_Strategy/robot.cpp
  initRobot() L8
  recoverFromEdge(bool frontTriggered) L25
  robotLoop() L52
projects/sumo-robot/firmware/strategy/v1.3_Strategy/sensors.cpp
  medianOf(const int * buffer) L13
  initSensors() L28
  primeOpponentSensors() L41
  readOpponentSensors() L51
  detectOpponent(const OpponentReadings & r) L69
  anyOpponentDetected(const OpponentDetection & d) L83
  anyEngaged(const OpponentDetection & d) L87
  readEdgesOnce() L91
  readEdgeSensors() L100
  anyEdgeDetected(const EdgeReadings & e) L112
projects/sumo-robot/firmware/strategy/v1.3_Strategy/sensors.h
  OpponentReadings L5
  OpponentDetection L7
  EdgeReadings L12
projects/sumo-robot/firmware/strategy/v1.3_Strategy/strategy_ram.cpp
  trackHeading(int sign,int pwmMagnitude=0) L18
  getHeadingEstimate() L24
  updateSearch() L32
  enterAlign(int dir,unsigned long now) L67
  getRamState() L79
  resetRamStrategy() L81
  resetStateKeepHeading() L90
  goSearch() L97
  forceCommit() L102
  updateRamStrategy() L111
projects/sumo-robot/firmware/strategy/v1.3_Strategy/strategy_ram.h
  RamState L5
projects/sumo-robot/firmware/strategy/v1.3_Strategy/v1.3_Strategy.ino
  setup() L7
  loop() L8
projects/sumo-robot/firmware/strategy/v2.0_Strategy/Map.cpp
  normalizeDeg180(float deg) L13
  recomputeU() L24
  initMap() L30
  mapUpdateMotion(int leftPwm,int rightPwm,unsigned long dtMs) L42
  mapUpdateContact(unsigned long dtMs) L64
  mapSnapEdge(bool frontTriggered) L76
  getPose() L97
  getRadiusFromCenter() L106
  getUncertainty() L107
  cornerRadius(float localX,float localY) L109
  getFootprintMaxRadius() L117
  isMapVoid() L127
  isEdgeReadingImplausible() L132
  getReturnHeadingDeg() L140
  getReturnTurnDeltaDeg() L145
  shouldReturn() L150
  getGovernedMaxSpeedCms() L155
  isPhantomDetection(int whichSensor,int rawAdc) L164
projects/sumo-robot/firmware/strategy/v2.0_Strategy/Map.h
  Pose L5
projects/sumo-robot/firmware/strategy/v2.0_Strategy/Motors.cpp
  initMotors() L5
  stopMotors() L27
  setSide(int rPwmPin,int lPwmPin,int speed) L29
  drive(int leftSpeed,int rightSpeed) L43
projects/sumo-robot/firmware/strategy/v2.0_Strategy/Robot.cpp
  EdgeRecoveryPhase L10
  normalizeDeg180Local(float deg) L25
  computeEdgeEscapeDrive(int & leftPwm,int & rightPwm) L34
  handleEdgeRecoveryTick(const EdgeReadings & e,unsigned long dtMs) L50
  initRobot() L92
  handleDoubleEdgeTick(const EdgeReadings & e,unsigned long dtMs) L112
  robotLoop() L122
projects/sumo-robot/firmware/strategy/v2.0_Strategy/Sensors.cpp
  ChannelState L9
  resetChannel(ChannelState & c,int pin,int sensorIndex) L23
  updateChannel(ChannelState & c) L34
  initSensors() L74
  primeOpponentSensors() L87
  updateOpponentSensors() L95
  getOpponentReadings() L104
  getOpponentDetection() L113
  anyOpponentDetected(const OpponentDetection & d) L125
  anyContact(const OpponentDetection & d) L130
  estimateFarRangeCm(int rawAdc) L139
  readEdgesOnce() L152
  readEdgeSensors() L160
  anyEdgeDetected(const EdgeReadings & e) L173
projects/sumo-robot/firmware/strategy/v2.0_Strategy/Sensors.h
  OpponentReadings L5
  OpponentDetection L10
  EdgeReadings L16
projects/sumo-robot/firmware/strategy/v2.0_Strategy/Strategy.cpp
  ReturnPhase L23
  SweepLeg L31
  enterSearch() L53
  proportionalMag(int raw,int cap) L62
  spinCommand(bool towardLeft,int pwmMag) L70
  cmsToPwm(float cms) L86
  enterAlign(bool towardLeft) L91
  enterFromDetection(const OpponentDetection & d) L111
  resetStrategy(bool seenAtKickoff) L136
  strategyForceCommit() L155
  strategyForceReturn() L163
  strategyEngage() L175
  getStrategyState() L180
  updateStrategy(const OpponentDetection & d) L182
projects/sumo-robot/firmware/strategy/v2.0_Strategy/Strategy.h
  MotorCommand L5
  StrategyState L11
projects/sumo-robot/firmware/strategy/v2.0_Strategy/v2.0_Strategy.ino
  setup() L8
  loop() L9
projects/sumo-robot/firmware/strategy/v2.1_Strategy/Map.cpp
  normalizeDeg180(float deg) L13
  recomputeU() L24
  initMap() L30
  mapUpdateMotion(int leftPwm,int rightPwm,unsigned long dtMs) L42
  mapUpdateContact(unsigned long dtMs) L64
  mapSnapEdge(bool frontTriggered) L76
  getPose() L97
  getRadiusFromCenter() L106
  getUncertainty() L107
  cornerRadius(float localX,float localY) L109
  getFootprintMaxRadius() L117
  isMapVoid() L127
  isEdgeReadingImplausible() L132
  getReturnHeadingDeg() L140
  getReturnTurnDeltaDeg() L145
  shouldReturn() L150
  getGovernedMaxSpeedCms() L155
  isPhantomDetection(int whichSensor,int rawAdc) L164
projects/sumo-robot/firmware/strategy/v2.1_Strategy/Map.h
  Pose L5
projects/sumo-robot/firmware/strategy/v2.1_Strategy/Motors.cpp
  initMotors() L5
  stopMotors() L27
  setSide(int rPwmPin,int lPwmPin,int speed) L29
  drive(int leftSpeed,int rightSpeed) L43
projects/sumo-robot/firmware/strategy/v2.1_Strategy/Robot.cpp
  EdgeRecoveryPhase L10
  normalizeDeg180Local(float deg) L25
  computeEdgeEscapeDrive(int & leftPwm,int & rightPwm) L34
  handleEdgeRecoveryTick(const EdgeReadings & e,unsigned long dtMs) L50
  startButtonPressed() L92
  waitForStartButton() L97
  initRobot() L117
  handleDoubleEdgeTick(const EdgeReadings & e,unsigned long dtMs) L144
  robotLoop() L154
projects/sumo-robot/firmware/strategy/v2.1_Strategy/Sensors.cpp
  ChannelState L9
  resetChannel(ChannelState & c,int pin,int sensorIndex) L23
  updateChannel(ChannelState & c) L34
  initSensors() L74
  primeOpponentSensors() L87
  updateOpponentSensors() L95
  getOpponentReadings() L104
  getOpponentDetection() L113
  anyOpponentDetected(const OpponentDetection & d) L125
  anyContact(const OpponentDetection & d) L130
  estimateFarRangeCm(int rawAdc) L139
  readEdgesOnce() L152
  readEdgeSensors() L160
  anyEdgeDetected(const EdgeReadings & e) L173
projects/sumo-robot/firmware/strategy/v2.1_Strategy/Sensors.h
  OpponentReadings L5
  OpponentDetection L10
  EdgeReadings L16
projects/sumo-robot/firmware/strategy/v2.1_Strategy/Strategy.cpp
  ReturnPhase L23
  SweepLeg L31
  enterCommit() L53
  enterSearch() L63
  proportionalMag(int raw,int cap) L74
  spinCommand(bool towardLeft,int pwmMag) L82
  cmsToPwm(float cms) L100
  enterAlign(bool towardLeft) L105
  enterFromDetection(const OpponentDetection & d) L121
  resetStrategy(bool seenAtKickoff) L144
  strategyForceCommit() L163
  strategyForceReturn() L168
  strategyEngage() L180
  getStrategyState() L185
  updateStrategy(const OpponentDetection & d) L187
projects/sumo-robot/firmware/strategy/v2.1_Strategy/Strategy.h
  MotorCommand L5
  StrategyState L11
projects/sumo-robot/firmware/strategy/v2.1_Strategy/v2.1_Strategy.ino
  setup() L8
  loop() L9
projects/sumo-robot/firmware/strategy/v2.2_Strategy/Map.cpp
  normalizeDeg180(float deg) L13
  recomputeU() L24
  initMap() L30
  mapUpdateMotion(int leftPwm,int rightPwm,unsigned long dtMs) L42
  mapUpdateContact(unsigned long dtMs) L64
  mapSnapEdge(bool frontTriggered) L76
  getPose() L97
  getRadiusFromCenter() L106
  getUncertainty() L107
  cornerRadius(float localX,float localY) L109
  getFootprintMaxRadius() L117
  isMapVoid() L127
  isEdgeReadingImplausible() L132
  getReturnHeadingDeg() L140
  getReturnTurnDeltaDeg() L145
  shouldReturn() L150
  getGovernedMaxSpeedCms() L155
  isPhantomDetection(int whichSensor,int rawAdc) L164
projects/sumo-robot/firmware/strategy/v2.2_Strategy/Map.h
  Pose L5
projects/sumo-robot/firmware/strategy/v2.2_Strategy/Motors.cpp
  initMotors() L5
  disableMotorDrivers() L27
  stopMotors() L43
  setSide(int rPwmPin,int lPwmPin,int speed) L45
  drive(int leftSpeed,int rightSpeed) L59
projects/sumo-robot/firmware/strategy/v2.2_Strategy/Robot.cpp
  EdgeRecoveryPhase L10
  normalizeDeg180Local(float deg) L25
  computeEdgeEscapeDrive(int & leftPwm,int & rightPwm) L34
  handleEdgeRecoveryTick(const EdgeReadings & e,unsigned long dtMs) L50
  buttonDown(int pin) L92
  waitForPress(int pin,bool pollSensors) L98
  initRobot() L118
  handleDoubleEdgeTick(const EdgeReadings & e,unsigned long dtMs) L150
  robotLoop() L160
projects/sumo-robot/firmware/strategy/v2.2_Strategy/Sensors.cpp
  ChannelState L9
  resetChannel(ChannelState & c,int pin,int sensorIndex) L23
  updateChannel(ChannelState & c) L34
  initSensors() L74
  primeOpponentSensors() L87
  updateOpponentSensors() L95
  getOpponentReadings() L104
  getOpponentDetection() L113
  anyOpponentDetected(const OpponentDetection & d) L125
  anyContact(const OpponentDetection & d) L130
  estimateFarRangeCm(int rawAdc) L139
  readEdgesOnce() L152
  readEdgeSensors() L160
  anyEdgeDetected(const EdgeReadings & e) L173
projects/sumo-robot/firmware/strategy/v2.2_Strategy/Sensors.h
  OpponentReadings L5
  OpponentDetection L10
  EdgeReadings L16
projects/sumo-robot/firmware/strategy/v2.2_Strategy/Strategy.cpp
  ReturnPhase L23
  SweepLeg L31
  enterCommit() L53
  enterSearch() L63
  proportionalMag(int raw,int cap) L74
  spinCommand(bool towardLeft,int pwmMag) L82
  cmsToPwm(float cms) L100
  enterAlign(bool towardLeft) L105
  enterFromDetection(const OpponentDetection & d) L121
  resetStrategy(bool seenAtKickoff) L144
  strategyForceCommit() L163
  strategyForceReturn() L168
  strategyEngage() L180
  getStrategyState() L185
  updateStrategy(const OpponentDetection & d) L187
projects/sumo-robot/firmware/strategy/v2.2_Strategy/Strategy.h
  MotorCommand L5
  StrategyState L11
projects/sumo-robot/firmware/strategy/v2.2_Strategy/v2.2_Strategy.ino
  setup() L8
  loop() L9
projects/sumo-robot/firmware/strategy/v2.3_Strategy/Map.cpp
  normalizeDeg180(float deg) L13
  recomputeU() L24
  initMap() L30
  mapUpdateMotion(int leftPwm,int rightPwm,unsigned long dtMs) L42
  mapUpdateContact(unsigned long dtMs) L64
  mapSnapEdge(bool frontTriggered) L76
  getPose() L97
  getRadiusFromCenter() L106
  getUncertainty() L107
  cornerRadius(float localX,float localY) L109
  getFootprintMaxRadius() L117
  isMapVoid() L127
  isEdgeReadingImplausible() L132
  getReturnHeadingDeg() L140
  getReturnTurnDeltaDeg() L145
  shouldReturn() L150
  getGovernedMaxSpeedCms() L155
  isPhantomDetection(int whichSensor,int rawAdc) L164
  getRearMaxRadius() L186
projects/sumo-robot/firmware/strategy/v2.3_Strategy/Map.h
  Pose L5
projects/sumo-robot/firmware/strategy/v2.3_Strategy/Motors.cpp
  initMotors() L5
  disableMotorDrivers() L27
  stopMotors() L43
  slewToward(int cur,int target,int maxStep) L48
  setSide(int rPwmPin,int lPwmPin,int speed) L60
  drive(int leftSpeed,int rightSpeed,bool immediate) L74
  getAppliedLeft() L99
  getAppliedRight() L100
projects/sumo-robot/firmware/strategy/v2.3_Strategy/Robot.cpp
  EdgeRecoveryPhase L10
  normalizeDeg180Local(float deg) L25
  computeEdgeEscapeDrive(int & leftPwm,int & rightPwm) L34
  handleEdgeRecoveryTick(const EdgeReadings & e,unsigned long dtMs) L51
  buttonDown(int pin) L93
  waitForPress(int pin,bool pollSensors) L107
  constantsValid() L131
  armAndStart() L148
  initRobot() L171
  handleDoubleEdgeTick(const EdgeReadings & e,unsigned long dtMs) L189
  robotLoop() L209
projects/sumo-robot/firmware/strategy/v2.3_Strategy/Sensors.cpp
  ChannelState L9
  readFiltered(int pin) L25
  resetChannel(ChannelState & c,int pin,int sensorIndex) L43
  updateChannel(ChannelState & c) L55
  initSensors() L94
  primeOpponentSensors() L107
  updateOpponentSensors() L115
  getOpponentReadings() L124
  getOpponentDetection() L133
  anyOpponentDetected(const OpponentDetection & d) L145
  anyContact(const OpponentDetection & d) L150
  estimateFarRangeCm(int rawAdc) L159
  readEdgesOnce() L172
  readEdgeSensors() L180
  anyEdgeDetected(const EdgeReadings & e) L193
projects/sumo-robot/firmware/strategy/v2.3_Strategy/Sensors.h
  OpponentReadings L5
  OpponentDetection L10
  EdgeReadings L16
projects/sumo-robot/firmware/strategy/v2.3_Strategy/Strategy.cpp
  ReturnPhase L23
  SweepLeg L31
  enterCommit() L53
  enterSearch() L63
  proportionalMag(int raw,int cap) L74
  spinCommand(bool towardLeft,int pwmMag) L82
  cmsToPwm(float cms) L100
  enterAlign(bool towardLeft) L105
  enterFromDetection(const OpponentDetection & d) L121
  resetStrategy(bool seenAtKickoff) L144
  strategyForceCommit() L165
  strategyForceReturn() L170
  strategyEngage() L182
  rearClearForBackoff() L187
  getStrategyState() L192
  updateStrategy(const OpponentDetection & d) L194
projects/sumo-robot/firmware/strategy/v2.3_Strategy/Strategy.h
  MotorCommand L5
  StrategyState L11
projects/sumo-robot/firmware/strategy/v2.3_Strategy/v2.3_Strategy.ino
  setup() L8
  loop() L9
projects/sumo-robot/firmware/strategy/v2.4_Strategy/Map.cpp
  normalizeDeg180(float deg) L13
  recomputeU() L24
  initMap() L30
  mapUpdateMotion(int leftPwm,int rightPwm,unsigned long dtMs) L42
  mapUpdateContact(unsigned long dtMs) L64
  mapSnapEdge(bool frontTriggered) L76
  getPose() L97
  getRadiusFromCenter() L106
  getUncertainty() L107
  cornerRadius(float localX,float localY) L109
  getFootprintMaxRadius() L117
  isMapVoid() L127
  isEdgeReadingImplausible() L132
  getReturnHeadingDeg() L140
  getReturnTurnDeltaDeg() L145
  shouldReturn() L150
  getGovernedMaxSpeedCms() L155
  isPhantomDetection(int whichSensor,int rawAdc) L164
  getRearMaxRadius() L184
projects/sumo-robot/firmware/strategy/v2.4_Strategy/Map.h
  Pose L5
projects/sumo-robot/firmware/strategy/v2.4_Strategy/Motors.cpp
  initMotors() L5
  disableMotorDrivers() L27
  stopMotors() L43
  slewToward(int cur,int target,int maxStep) L48
  setSide(int rPwmPin,int lPwmPin,int speed) L60
  drive(int leftSpeed,int rightSpeed,bool immediate) L74
  getAppliedLeft() L99
  getAppliedRight() L100
projects/sumo-robot/firmware/strategy/v2.4_Strategy/Robot.cpp
  EdgeRecoveryPhase L10
  normalizeDeg180Local(float deg) L25
  computeEdgeEscapeDrive(int & leftPwm,int & rightPwm) L34
  handleEdgeRecoveryTick(const EdgeReadings & e,unsigned long dtMs) L51
  buttonDown(int pin) L93
  waitForPress(int pin,bool pollSensors) L107
  constantsValid() L131
  armAndStart() L148
  initRobot() L172
  handleDoubleEdgeTick(const EdgeReadings & e,unsigned long dtMs) L192
  robotLoop() L212
projects/sumo-robot/firmware/strategy/v2.4_Strategy/Sensors.cpp
  ChannelState L9
  readFiltered(int pin) L25
  resetChannel(ChannelState & c,int pin,int sensorIndex) L43
  updateChannel(ChannelState & c) L55
  initSensors() L94
  primeOpponentSensors() L107
  updateOpponentSensors() L115
  getOpponentReadings() L124
  getOpponentDetection() L133
  anyOpponentDetected(const OpponentDetection & d) L145
  anyContact(const OpponentDetection & d) L150
  estimateFarRangeCm(int rawAdc) L159
  calibrateEdgePolarity() L174
  readEdgesOnce() L187
  readEdgeSensors() L195
  anyEdgeDetected(const EdgeReadings & e) L208
projects/sumo-robot/firmware/strategy/v2.4_Strategy/Sensors.h
  OpponentReadings L5
  OpponentDetection L10
  EdgeReadings L16
projects/sumo-robot/firmware/strategy/v2.4_Strategy/Strategy.cpp
  ReturnPhase L23
  SweepLeg L31
  enterCommit() L53
  enterSearch() L63
  proportionalMag(int raw,int cap) L74
  spinCommand(bool towardLeft,int pwmMag) L82
  cmsToPwm(float cms) L100
  enterAlign(bool towardLeft) L105
  enterFromDetection(const OpponentDetection & d) L121
  resetStrategy(bool seenAtKickoff) L144
  strategyForceCommit() L165
  strategyForceReturn() L170
  strategyEngage() L182
  rearClearForBackoff() L187
  getStrategyState() L192
  updateStrategy(const OpponentDetection & d) L194
projects/sumo-robot/firmware/strategy/v2.4_Strategy/Strategy.h
  MotorCommand L5
  StrategyState L11
projects/sumo-robot/firmware/strategy/v2.4_Strategy/v2.4_Strategy.ino
  setup() L8
  loop() L9
