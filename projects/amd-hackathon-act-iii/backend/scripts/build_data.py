"""Builds sop.json, notes.json and answer_key.json (synthetic data, labelled as such).

Run from the backend folder:  python scripts/build_data.py
Edit the text below, re-run, then run:  python scripts/check_data.py
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data"

# ---------------------------------------------------------------- SOPs
# (sop_id, title of the whole procedure, [(step title, step text), ...])
SOPS = [
    ("SOP-01", "Lockout and tagout, Packaging Line 3", [
        ("Notify the crew", "Tell the line crew and the shift supervisor that Line 3 is going down for maintenance."),
        ("Stop the line", "Stop Line 3 from the control panel using the normal stop sequence."),
        ("Isolate energy", "Turn the main isolator for Line 3 to OFF and close the compressed air valve at the supply."),
        ("Apply your lock", "Fit your personal padlock to the isolator hasp and the air valve. Each person working on the line applies their own lock."),
        ("Attach your tag", "Attach a tag to each lock showing your name, the date and the reason for the lockout."),
        ("Release stored energy", "Bleed the air pressure at the bleed valve and wait until the gauge reads zero."),
        ("Try to start", "Press the start button once at the panel to confirm the line does not move, then return the control to stop."),
        ("Verify zero energy", "Check with the voltage tester that the isolator terminals read zero before touching any conductor."),
        ("Do the work", "Carry out the maintenance. Keep your lock on until you have finished."),
        ("Remove your lock", "When the work is done, check tools are clear, guards are refitted and everyone is out of the machine, then remove your own lock only."),
        ("Restart and inform", "Restore energy, start the line from the panel and tell the crew the line is running."),
    ]),
    ("SOP-02", "Forklift pre-shift inspection", [
        ("Read the truck log", "Read the previous shift's entries in the truck log for reported faults."),
        ("Walk around", "Walk around the truck and look for damage, leaks and loose parts."),
        ("Forks and mast", "Check the forks for cracks and bends and the mast chains for wear and correct tension."),
        ("Tyres", "Check the tyres for cuts and flat spots and check the wheel nuts are tight."),
        ("Battery", "Check the battery charge indicator reads above 30 percent and the battery restraint is secure."),
        ("Seat belt and horn", "Fit the seat belt, then test the horn."),
        ("Lights and alarm", "Test the headlights, the blue spot light and the reversing alarm."),
        ("Brakes and steering", "Drive a few metres in the yard and test the service brake, the parking brake and the steering."),
        ("Sign the log", "Record the result in the truck log and sign it. Report any fault to the supervisor and tag the truck out of service if it is unsafe."),
    ]),
    ("SOP-03", "Caustic clean-in-place (CIP) of Mixing Tank M2", [
        ("Confirm tank empty and permit", "Confirm Tank M2 is empty and that the supervisor has signed the CIP permit."),
        ("Put on PPE", "Put on chemical goggles, face shield, caustic-resistant gloves and apron before opening any caustic line."),
        ("Pre-rinse", "Pre-rinse the tank with water for 10 minutes until the drain runs clear."),
        ("Check caustic strength", "Test the caustic solution with the titration kit. The concentration must be 1.5 to 2.0 percent."),
        ("Connect hoses", "Connect the caustic supply hose and the return hose, and check both clamps are tight."),
        ("Circulate caustic", "Start the CIP pump and circulate caustic at 70 degrees C for 20 minutes."),
        ("Record temperature", "Read the temperature on the panel every 5 minutes and write it on the CIP sheet."),
        ("Drain caustic", "Stop the pump, return the caustic to the CIP tank and drain the line."),
        ("Final rinse", "Rinse the tank with fresh water for at least 15 minutes."),
        ("Check rinse water", "Test the outlet water with pH strips. The reading must be 7 to 8 before sign-off."),
        ("Disconnect and cap", "Disconnect the hoses with the line vented and cap the ports."),
        ("Close the permit", "Complete the CIP sheet and have the supervisor sign the permit closed."),
    ]),
]

# ---------------------------------------------------------------- planted drifts
# (sop_id, step_id, drift_type, source, text, evidence)
# evidence must appear word for word (ignoring capitals and extra spaces) in text.
DRIFTS = [
    ("SOP-01", 1, "skipped_step", "maintenance",
     "Fitters swapped the Line 3 gearbox. Crew was on break so we didn't tell the line crew before isolating, supervisor was informed afterwards.",
     "we didn't tell the line crew before isolating"),
    ("SOP-01", 4, "workaround_substitution", "maintenance",
     "Sensor replacement on Line 3 with two fitters. Used a single group lock on the isolator instead of a lock each, tags written with both names.",
     "a single group lock on the isolator instead of a lock each"),
    ("SOP-01", 10, "sop_unclear", "handover",
     "Fitters disagree on what everyone is out of the machine means in the lock removal step, a head count or just a look round. Raised with the supervisor.",
     "disagree on what everyone is out of the machine means"),
    ("SOP-02", 9, "sop_outdated_or_impractical", "handover",
     "Operators are using the tablet checklist for the truck checks now, but the SOP still says paper log and nobody has the log book at the bay.",
     "the SOP still says paper log"),
    ("SOP-01", 6, "reordered_steps", "maintenance",
     "Line 3 sensor job. Tested the terminals with the meter first, then bled the air line afterwards while waiting for the part.",
     "Tested the terminals with the meter first, then bled the air line afterwards"),
    ("SOP-02", 4, "skipped_step", "handover",
     "Dispatch were waiting so trucks 4 and 6 started without the tyre check. Everything else on the list was done and signed.",
     "started without the tyre check"),
    ("SOP-03", 4, "workaround_substitution", "handover",
     "Titration kit empty again, so we used the conductivity meter to estimate caustic strength instead. Reading looked fine.",
     "used the conductivity meter to estimate caustic strength instead"),
    ("SOP-03", 3, "sop_unclear", "handover",
     "Runs clear is a judgement call. One crew rinses M2 for 10 minutes and the other crew for 15 before moving on.",
     "Runs clear is a judgement call"),
    ("SOP-03", 6, "sop_outdated_or_impractical", "handover",
     "M2 heater cannot get past 65 degrees in winter, so the 70 degree circulation in the SOP can't be done as written.",
     "cannot get past 65 degrees in winter"),
    ("SOP-03", 2, "reordered_steps", "near-miss",
     "Near miss on the M2 CIP. The operator put the face shield and gloves on after connecting the hoses and a drip of caustic reached his sleeve. No injury, sleeve changed.",
     "put the face shield and gloves on after connecting the hoses"),
    ("SOP-01", 6, "skipped_step", "maintenance",
     "Replaced the air cylinder on Line 3 infeed. Locked out at the isolator and tagged. Did not bleed the air as the valve was shut so we assumed it was fine.",
     "Did not bleed the air"),
    ("SOP-01", 8, "workaround_substitution", "maintenance",
     "No tester at the Line 3 cabinet so the fitter used a non-contact pen instead of the voltage tester before touching the terminals.",
     "used a non-contact pen instead of the voltage tester"),
    ("SOP-02", 2, "sop_unclear", "handover",
     "New operators ask what the walk-around should cover. The SOP just says look for damage and nobody has said how closely to look.",
     "The SOP just says look for damage"),
    ("SOP-02", 5, "sop_outdated_or_impractical", "handover",
     "Trucks swapped batteries early again. The new trucks lock lifting at 20 percent, so the 30 percent rule makes us swap batteries too early.",
     "the 30 percent rule makes us swap batteries too early"),
    ("SOP-01", 5, "reordered_steps", "maintenance",
     "Locked out Line 3 for the wrapper repair. Tags were written up after the work started because the tag book was in the office.",
     "Tags were written up after the work started"),
    ("SOP-03", 10, "skipped_step", "handover",
     "CIP on M2 finished. Rinse ran 15 minutes and we signed off without pH strips as the tub was empty. Permit closed.",
     "signed off without pH strips"),
    ("SOP-02", 3, "workaround_substitution", "handover",
     "Trucks 1 and 3 done fast. Did the fork and chain check by looking from the seat instead of getting down. Everything else normal.",
     "by looking from the seat instead of getting down"),
    ("SOP-03", 8, "sop_unclear", "handover",
     "Not clear whether drain the line means opening the low point valve or just letting it run back. Two of us did it differently.",
     "whether drain the line means opening the low point valve"),
    ("SOP-03", 5, "sop_outdated_or_impractical", "maintenance",
     "SOP talks about clamped hoses but M2 now has quick-connect couplings, so the hose connection step no longer fits.",
     "M2 now has quick-connect couplings"),
    ("SOP-03", 4, "reordered_steps", "handover",
     "The crew titrated the caustic after it was already circulating because the kit was in the lab. Result 1.8 percent.",
     "titrated the caustic after it was already circulating"),
    ("SOP-01", 7, "skipped_step", "maintenance",
     "Fitter locked out Line 3 and went straight to the sensor swap without trying the start button, said the panel was dead anyway.",
     "without trying the start button"),
    ("SOP-03", 7, "workaround_substitution", "handover",
     "Panel temperature probe on M2 faulty. We used a handheld infrared thermometer on the outside of the pipe and wrote those readings on the CIP sheet.",
     "used a handheld infrared thermometer on the outside of the pipe"),
    ("SOP-02", 8, "sop_unclear", "handover",
     "Nobody knows how many metres the brake test drive should be, or whether it is done loaded or empty.",
     "Nobody knows how many metres"),
    ("SOP-01", 2, "sop_outdated_or_impractical", "maintenance",
     "Line 3 control panel was replaced in the summer and has no normal stop sequence any more. The SOP step does not match the new panel.",
     "The SOP step does not match the new panel"),
    ("SOP-02", 8, "reordered_steps", "handover",
     "Truck 6 did the brake test before the light check because the yard was clear and the lights needed the dark. Both passed.",
     "did the brake test before the light check"),
]

# ---------------------------------------------------------------- traps
# Look like drift (words like skipped, instead, without) but are not drift. (source, text, why)
TRAPS = [
    ("handover", "Skipped the second break to finish the Line 3 clean-down. All lockout steps were followed and the line was handed back on time.",
     "skipped refers to a break, not an SOP step"),
    ("handover", "Line 2 fitter used a group lock box during the belt change. Line 2 has its own local procedure, nothing to do with the Line 3 SOP.",
     "different line, no SOP in this set covers it"),
    ("near-miss", "Operator climbed on the conveyor to clear a jam instead of using the step. Reminded of the walkway rule, no injury.",
     "no SOP in this set covers climbing"),
    ("maintenance", "Used an extra danger sign and a second lock on the Line 3 isolator in addition to each fitter's own lock, more than the SOP asks.",
     "goes beyond the SOP, not a deviation"),
    ("handover", "Inspected truck 5 twice today, first at shift start and again after a pallet of caustic was moved into its path. Both checks clean and logged.",
     "extra check, compliant"),
    ("handover", "Without the usual crowd the dock was calm. Trucks 1 to 3 checked first thing as normal and logged.",
     "without refers to the crowd"),
    ("maintenance", "Replaced the Line 3 outfeed motor with a different brand of the same rating, supplier changed. Full lockout, zero volts confirmed.",
     "part substitution, procedure followed"),
    ("handover", "CIP on M2 started late because the caustic tote arrived late. All steps followed in order once it arrived.",
     "delay, not drift"),
    ("near-miss", "Forklift driver almost skipped the horn test because of a phone call, noticed and did it before moving. Log signed.",
     "step was done"),
    ("handover", "Line 3 panel screen replaced with an updated version, same buttons and same stop sequence as before.",
     "change that does not conflict with the SOP"),
    ("maintenance", "Fitter used a torque wrench instead of a spanner on the Line 3 guard bolts to match the new spec. Line locked out first.",
     "tool choice not covered by the SOP"),
    ("handover", "Instead of the usual pH strips the lab supplied a new brand with the same range, 0 to 14. M2 rinse water read 7.6.",
     "equivalent strips, step done"),
    ("near-miss", "Cleaner did not wear gloves while wiping the label printer. Not a hazard area and no procedure covers it, reminded anyway.",
     "PPE step in SOP-03 only applies to caustic work"),
    ("handover", "Pre-rinse on M2 was longer than normal, 15 minutes, as the drain was cloudy. Went on once it ran clear.",
     "longer than required, compliant"),
    ("maintenance", "Fitters wrote the tags in red pen for visibility. Every tag had name, date and reason and went on before work started.",
     "tags compliant"),
    ("handover", "Truck 3 battery was at 28 percent in the evening and was put on charge instead of going out.",
     "low battery correctly not used"),
    ("handover", "Line 3 ran on the new film first, then the old film after lunch. Product quality was identical.",
     "not related to any SOP step"),
    ("near-miss", "Colleague asked why the horn test comes after the seat belt. Explained it is the order in the SOP and that the steps were followed.",
     "question only, steps followed"),
    ("handover", "The permit was already signed by the supervisor so the CIP on M2 started right away with no wait.",
     "permit step done"),
    ("handover", "M2 caustic strength came in at 1.4 percent, below range, so the batch was topped up and retested before use.",
     "out of range value handled correctly"),
    ("near-miss", "Pedestrian walked through the forklift lane instead of using the walkway. Driver stopped in time. Reminded the person.",
     "pedestrian behaviour, not an SOP step"),
    ("maintenance", "Used a voltage tester borrowed from the other line because ours was out for calibration. Same model and in date. Zero volts read.",
     "equivalent tester, step done"),
    ("handover", "CIP rinse ran for 25 minutes instead of the minimum 15 because the plant wanted a safe margin. pH read 7.2.",
     "longer than minimum, compliant"),
    ("handover", "Packaging team changed the Line 3 film supplier last week. The SOP review is not due until next quarter.",
     "mentions SOP, no deviation"),
    ("near-miss", "New operator unsure where the first aid kit is kept. Pointed it out and added a sign.",
     "not an SOP step"),
    ("maintenance", "Replaced the Line 3 padlock hasp with a larger one so more locks fit. Hasp matches the lockout board.",
     "improvement, not drift"),
    ("handover", "Line 3 restart went quicker than usual today. Crew told the line was running, panel start used, no problems.",
     "restart step followed"),
    ("near-miss", "Forklift left with the keys in at the dock for a minute. Keys removed and driver reminded.",
     "key rule, not an inspection step"),
    ("handover", "Operators say the lockout SOP is clear and easy to follow after the refresher. No questions.",
     "positive feedback"),
    ("handover", "No deviations to report this shift. All locks, tags, checks and CIP readings were done as written.",
     "all compliant"),
]

# ---------------------------------------------------------------- clean notes
CLEAN_H = [
    "Line 3 ran normally all shift. Two label rolls changed, no stoppages. Spare film roll in the cage for the next shift.",
    "Quiet night. Caustic tote for M2 delivered at 02:00 and stored in the bunded area. Two pallets of cartons staged for the morning.",
    "All forklifts accounted for at the start of the day. Truck 2 battery swapped at 06:00. Dock 4 door sticking, work order raised.",
    "Line 3 stopped for 20 minutes for a film jam at the wrapper. Operator cleared it with the line stopped at the panel. No injuries.",
    "Truck 4 on charge, trucks 5 and 6 out. Pre-shift checks done and logged for all three.",
    "M2 caustic CIP done on schedule. Temperatures logged every 5 minutes on the sheet, rinse pH read 7.5 with strips. Permit closed by the supervisor.",
    "Packaging target hit for the third day running. No overtime needed tomorrow.",
    "New starter shadowed the Line 3 operator today. Started with housekeeping and the walkways, nothing on the machine yet.",
    "Dock scale recalibrated by the contractor. Certificate on the notice board.",
    "Truck 7 failed the brake test at the pre-shift check, tagged out of service and reported to the supervisor, entry made in the log. Hire truck arriving tomorrow.",
    "First aid kit by Line 3 checked and in date. Hand sanitiser stations on the mezzanine refilled.",
    "Line 3 ran slow after lunch because of a reel with uneven tension. Reel replaced, speed back to normal.",
    "M2 CIP booked for tomorrow morning. Permit prepared and waiting for the supervisor signature, caustic tote checked and in the bund.",
    "Cleaners finished the mezzanine early. Floor was wet at the stairs for ten minutes, sign was out.",
    "Fire alarm test at 10:30, evacuated in 4 minutes. Everyone at the muster point, headcount correct.",
    "Forklift tyres on truck 3 changed by the contractor. Truck re-inspected and logged before use.",
    "Cartons for the Hall A order arrived short by one pallet. Warehouse told, supplier chasing.",
    "Line 3 speed set to 85 percent, product code changed at 14:00, no issues since.",
    "Compressed air pressure dropped to 5 bar mid-morning, compressor restarted by maintenance, back to 7 bar.",
    "Safety walk by the manager today, no actions raised for Line 3 or the forklift bay.",
    "Caustic sample titrated at 1.8 percent before the CIP on M2, inside the range. Circulation ran 20 minutes at 70 degrees.",
    "Forklift charging bay clear and tidy. Spare battery on the second charger.",
    "Lockout refresher training booked for next Tuesday, six names so far.",
    "Line 3 operators asked for a second pair of gloves in size L. Request sent to stores.",
    "The M2 tank was empty and the permit signed by the supervisor before we started the CIP. Goggles, shield, gloves and apron on for everyone on the job.",
    "Outfeed conveyor on Line 3 running with a slight noise. Logged for maintenance, no action needed tonight.",
    "Production planning moved the Line 3 changeover to Thursday. Operators informed at the board.",
    "Rain overnight, loading dock floor slippery. Mats put down and the sign out.",
    "Trucks 1 and 2 inspected, logs signed. Truck 1 mast chain slightly stiff, greased by the fitter.",
    "Line 3 film tracking adjusted by the operator at the panel, line stopped first.",
    "Visitor group toured the packaging hall, escorted throughout and wearing hi-vis.",
    "Stores received a new voltage tester and two padlocks for the lockout board. Tester placed in the Line 3 cabinet.",
    "M2 rinse water tested after the final rinse, pH 7.4. Hoses disconnected with the line vented and ports capped.",
    "Quality hold on batch 4471 released after the lab result came back clear.",
    "Lights in the forklift bay replaced by the electrician. Fixed and tested.",
    "One pallet re-stacked by hand after a wrap failure. No damage to product.",
    "Dock door 2 repaired by the contractor and signed off.",
    "Line 3 stopped at 05:00 for the planned lubrication. Done under lockout by two fitters, own locks and tags, back running at 05:40.",
    "Spill of cleaning water near the CIP skid mopped up straight away, no product involved.",
    "Safety board updated with this month's days without incident. Count now 43.",
    "Operator trained on the new film splice tool. Sign-off sheet filed.",
    "Forklift horn on truck 5 tested at the pre-shift check, working. Log signed.",
    "Pallet wrap supply low. Reorder placed with stores.",
    "M2 empty and rinsed, ready for the next batch. CIP sheet filed in the folder, permit closed.",
    "Cold morning, trucks started slowly but passed all checks.",
    "The new label printer on Line 3 jammed twice, supplier contacted.",
    "Weekly housekeeping audit scored 94 percent. Actions: bin lids and one missing floor marking.",
    "Shift briefing covered the new emergency exit route. All present signed the sheet.",
    "Pre-rinse on M2 ran 10 minutes and the drain ran clear before moving on. Caustic circulation started after the strength test.",
    "Line 3 wrapper arm replaced. Maintenance team closed out the work order.",
    "Dock leveller on door 3 serviced, working normally.",
    "Spare forks for the trucks delivered and stored in the maintenance cage.",
    "Overtime list for the weekend posted on the board. Eight volunteers so far.",
    "Line 3 shift output 14,200 units against a target of 14,000.",
    "Forklift battery watering done by the fitter. Levels okay, logged.",
]

CLEAN_M = [
    "Replaced worn belt on Line 3 outfeed. Followed the full lockout, each fitter on own lock and tag, zero volts confirmed with the tester before work.",
    "Greased bearings on the Line 3 conveyor during the planned stop. Locks and tags on, tested for zero energy first, all removed by their owners after.",
    "Truck 3 pre-shift check found a loose wheel nut on the front left. Tightened, re-checked, logged, truck out after sign-off.",
    "Replaced a cracked guard on Line 3 infeed. Lockout applied by each person with own lock and tag, guard refitted and checked before the locks came off.",
    "Replaced the air regulator on Line 3. Air valve locked, line bled to zero on the gauge, then work started.",
    "Changed hydraulic hose on truck 6. Truck tagged out, repaired, brake and steering tested in the yard before release.",
    "Calibrated the M2 temperature probe, reading within 0.5 degrees of the reference.",
    "Replaced the horn on truck 2 and tested it with the seat belt fitted. Entry in the truck log.",
    "Cleaned the M2 spray ball. CIP permit signed before the cleaning started.",
    "Replaced worn mast chain on truck 1. Tension set to spec and checked by a second fitter.",
    "Line 3 photo-eye cleaned and realigned under lockout. Zero volts confirmed, locks removed by their owners.",
    "Replaced two door seals on the packaging hall entrance.",
    "Checked all fork tines on trucks 1 to 7 as part of the monthly inspection, no cracks found.",
    "Topped up CIP tank with fresh caustic. Strength 1.9 percent by titration.",
    "Replaced the Line 3 start button cover. Isolated, locked, tagged, tried the start button to confirm no movement, then worked.",
    "Rewired the M2 level sensor after testing dead with the meter. Locks and tags in place, tags written before the job started.",
    "Truck 5 blue spot light bulb replaced and tested.",
    "Serviced the Line 3 compressor filter. Air isolated and bled to zero before opening the housing.",
    "Replaced the pH probe in the M2 outlet. Probe calibrated with two buffers before use.",
    "Fitted new reversing alarm on truck 4. Tested and entered in the log.",
    "Replaced gasket on the M2 caustic return hose coupling. Line vented first.",
    "Changed the Line 3 motor contactor. Voltage tester used on all terminals, zero reading, work completed, locks off by the owners.",
    "Repaired the pallet jack handle near dock 2.",
    "Truck 7 charger fault traced to a loose lead. Re-seated and tested over a full cycle.",
    "Replaced the broken seat belt on truck 3. Fitted and tested before the truck went out.",
    "Deep clean of the CIP skid, caustic line drained and flushed first.",
    "Replaced worn rollers on Line 3 infeed during planned downtime. All locks on before starting, each person with own tag.",
    "Annual inspection of the lockout board. Padlocks counted and tags restocked.",
    "Greased all truck mast channels. Logged against each truck.",
    "Replaced the tank level gauge on M2. Tank empty and permit signed before work.",
    "Adjusted brake pedal free play on truck 2. Retested in the yard, fine.",
    "Replaced faulty pressure gauge at the Line 3 air bleed valve. Reads zero when vented.",
    "Welded cracked bracket on the Line 3 guard rail. Hot work permit signed, line locked out.",
    "Checked caustic hose clamps on both M2 hoses and replaced one worn clamp.",
    "Serviced truck 4 battery connector. Restraint checked and secure.",
    "Replaced the control cable on the Line 3 stop button. Isolation and lock applied, tested at zero volts.",
    "Repainted the walkway lines next to Line 3.",
    "Changed the CIP pump seal. Pump isolated and locked, tagged with name, date and reason.",
    "Replaced front tyre on truck 6. Wheel nuts torqued and rechecked after the first hour.",
    "Fixed the sticking gate on the forklift bay.",
    "Replaced a worn timing belt on the wrapper. Line stopped, isolated, own locks fitted, tag attached, start tried and zero volts confirmed.",
    "Descaled the M2 heater element. Tank empty, permit signed.",
    "Tightened loose guard bolts on Line 3 discharge.",
    "Replaced faulty indicator on truck 1 battery gauge, reads correctly against the charger.",
    "Cleaned and inspected the eye wash station near the CIP skid. Flow test passed.",
    "Changed the Line 3 safety relay under full lockout, own locks and tags, all removed by their owners at the end.",
    "Replaced the damaged top rail on the stair near M2.",
    "Replaced the fuse in the Line 3 control panel, tested at the terminals with the voltage tester first.",
    "Repaired the film cutter on the Line 3 wrapper.",
    "Checked the emergency stop on Line 3 operates correctly, test logged.",
]

CLEAN_N = [
    "Pallet of cartons left across the walkway near Line 3. Nobody hurt, moved it and reminded the packers about the yellow lines.",
    "Forklift reversed close to a packer at the dock door. Horn sounded, nobody touched. Briefed the driver and packer at the toolbox talk.",
    "Wet floor at the bottom of the mezzanine stairs, operator slipped but caught the rail. Dried and sign placed.",
    "A carton fell from a stack on the top rack, nobody underneath. Stack reorganised.",
    "Film roll slipped from the cart during loading. Nobody hurt, cart wheels checked.",
    "Hi-vis not worn by a visitor on the dock, spotted and corrected immediately.",
    "Trailing air hose near Line 3 caught a foot. No fall. Hose rerouted.",
    "Pallet jack rolled slightly on the ramp. Chocks fitted.",
    "Glove torn during the caustic hose connection, replaced before the caustic flowed.",
    "Splash of rinse water to the eyes of a cleaner during the M2 rinse. Eye wash used, no irritation, report filed.",
    "Forklift speed in the yard felt high. Driver reminded of the 8 km/h limit.",
    "Loose pallet board spotted and removed before use.",
    "Smell of overheated motor at the Line 3 outfeed. Line stopped, motor checked, thermal trip reset after the fan was cleaned.",
    "Step ladder footing slipped on the wet floor, operator held on. Ladder replaced with a platform.",
    "A packer's sleeve caught the moving belt edge near Line 3, freed himself, no injury. Guard extended.",
    "Light flickered in the forklift bay, no incident, electrician called.",
    "Visitor stepped over the yellow barrier near Line 3, stopped by the operator and escorted out. No contact with the machine.",
    "Caustic tote cap found loose at the delivery, tightened by the driver and logged.",
    "Cut finger on a strapping band. First aid applied.",
    "Oil patch on the floor near truck 2. Wiped up, leak found at the hydraulic fitting and reported.",
    "Cardboard blocking the emergency exit sign. Cleared.",
    "Forklift mirror knocked off at the dock door. No injury, mirror refitted.",
    "Spill of floor cleaner near the CIP skid, reported, cleared, area signed off.",
    "Operator slipped slightly on the dock plate. Anti-slip tape added.",
    "Door to the chemical store left unlocked briefly, locked on discovery and key log updated.",
    "Hot surface on the M2 heater touched briefly, minor redness, first aid, warning sign added.",
    "Forklift horn heard late by a pedestrian near the corner. Mirror and sign added at the corner.",
    "Pallet on the top rack leaning. Straightened with the truck, rack inspected.",
    "A fitter nearly dropped a wrench from the platform. Lanyard now required.",
    "Noise from the Line 3 outfeed bearing. Line stopped and bearing replaced under lockout.",
    "Hose on the M2 pump weeping slightly. Pump stopped and hose replaced.",
    "Static shock from the wrapper film. Operator unhurt.",
    "Truck 4 drifted slightly under braking in the yard. Wheel nut found loose and tightened, tested and logged.",
    "Late delivery driver parked across the fire exit. Moved on request.",
    "Operator tripped on a cable lead. Cable taped down.",
    "Dust from the carton cutting area, extraction cleaned.",
    "Pallet stacked too high at the dock, restacked to 1.6 m.",
    "A bag of caustic pellets stored near water, moved to the dry shelf.",
    "Forklift driver forgot hi-vis at the start of the shift, collected it from the locker, corrected.",
    "Door of the packaging hall swung into a passing packer. No injury, closer adjusted.",
]

# ---------------------------------------------------------------- layout
# One entry per block of 8 notes: (drift position 1-8, [trap positions]).
# Drifts are placed in this order of DRIFTS; traps in the order of TRAPS.
LAYOUT = [
    (3, [6]), (6, [1]), (2, [5]), (7, [2]), (4, [1, 7]),
    (1, [4]), (5, [8]), (8, [3]), (3, [6]), (6, [1, 3]),
    (2, [5]), (7, [2]), (4, [7]), (1, [4]), (5, [2, 8]),
    (8, [3]), (3, [6]), (6, [1]), (2, [5]), (7, [2, 4]),
    (4, [7]), (1, [4]), (5, [8]), (8, [3]), (3, [6, 8]),
]

# The 25 drifts above are listed in the order they should appear in time.
SHIFTS = ["Day", "Evening", "Night"]
START = date(2026, 9, 1)


def build():
    assert len(DRIFTS) == 25 and len(TRAPS) == 30, (len(DRIFTS), len(TRAPS))
    clean = [("handover", t) for t in CLEAN_H] + [("maintenance", t) for t in CLEAN_M] + [("near-miss", t) for t in CLEAN_N]
    assert len(clean) == 145, len(clean)
    random.Random(7).shuffle(clean)
    ci = iter(clean)

    sop_rows = []
    for sop_id, _name, steps in SOPS:
        for i, (title, text) in enumerate(steps, 1):
            sop_rows.append({"sop_id": sop_id, "step_id": i, "title": title, "text": text})

    notes, drifts, traps = [], [], []
    di = iter(DRIFTS)
    ti = iter(TRAPS)
    n = 0
    for dpos, tpos in LAYOUT:
        for pos in range(1, 9):
            n += 1
            nid = f"N{n:03d}"
            if pos == dpos:
                sop_id, step_id, dtype, source, text, evidence = next(di)
                drifts.append({"note_id": nid, "sop_id": sop_id, "step_id": step_id,
                               "drift_type": dtype, "evidence": evidence})
            elif pos in tpos:
                source, text, why = next(ti)
                traps.append({"note_id": nid, "why": why})
            else:
                source, text = next(ci)
            d = START + timedelta(days=(n - 1) // 7)
            notes.append({"note_id": nid, "date": d.isoformat(), "shift": SHIFTS[(n - 1) % 3],
                          "source": source, "text": text})

    def dump(name, obj):
        (OUT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    dump("sop.json", sop_rows)
    dump("notes.json", notes)
    dump("answer_key.json", {"drifts": drifts, "traps": traps})
    print(f"wrote {len(sop_rows)} SOP steps, {len(notes)} notes, {len(drifts)} drifts, {len(traps)} traps")


if __name__ == "__main__":
    build()