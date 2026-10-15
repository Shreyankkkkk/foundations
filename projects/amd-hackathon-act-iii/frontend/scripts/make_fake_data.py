"""Writes realistic FAKE data (agreed format) into data/. The back end replaces it on 15 Oct. Run from frontend/: python scripts/make_fake_data.py"""
import json, random, datetime as dt
from pathlib import Path
DATA = Path(__file__).resolve().parent.parent / "data"
DATA.mkdir(exist_ok=True)
random.seed(7)
S = {"SOP-LOTO": [("Notify affected staff", "Tell everyone near the machine before shutdown."), ("Shut down the machine", "Use the normal stop sequence."),
     ("Isolate energy sources", "Switch off electrical, air and hydraulic supply."), ("Apply lock and tag", "Each worker fits a personal lock and a tag."),
     ("Release stored energy", "Bleed pressure and block moving parts."), ("Verify zero energy", "Try to start the machine. It must not move."),
     ("Perform the work", "Only after steps 1 to 6 are done."), ("Remove locks and restore", "Check the area, then remove locks and restart.")],
 "SOP-FORK": [("Park in the charging bay", "Set the brake and lower the forks."), ("Wear acid-resistant gloves and face shield", "Required for all battery work."),
     ("Check vent caps and electrolyte level", "Look before every charge."), ("Connect charger only when off", "Plug in with the charger switched off."),
     ("Charge to full without interruption", "Full charge takes eight hours."), ("Disconnect and wipe terminals", "Switch off first, then unplug.")],
 "SOP-CONF": [("Issue entry permit", "Supervisor signs before entry."), ("Test the atmosphere", "Check oxygen and gas levels."),
     ("Ventilate for 15 minutes", "Run the fan before anyone enters."), ("Station an attendant outside", "One person stays at the opening."),
     ("Confirm rescue plan and radio check", "Done at the start of each entry."), ("Enter and monitor continuously", "Keep gas readings on screen.")]}
SEEDS = [("SOP-LOTO", 6, "skipped_step", "we skipped the try-start on the press again", 8, 1), ("SOP-LOTO", 4, "workaround_substitution", "used a zip tie instead of a proper tag", 4, 0),
 ("SOP-LOTO", 1, "sop_unclear", "not sure who counts as affected staff", 3, 0), ("SOP-LOTO", 5, "reordered_steps", "did the stored energy release after the try-start", 3, 0),
 ("SOP-FORK", 2, "workaround_substitution", "used regular work gloves because the acid ones were out", 6, 1),
 ("SOP-FORK", 5, "sop_outdated_or_impractical", "topped up mid-shift because a full charge takes eight hours", 5, 1),
 ("SOP-FORK", 3, "skipped_step", "no time to check the vent caps", 3, 0), ("SOP-CONF", 3, "sop_outdated_or_impractical", "fifteen minutes of ventilation is not realistic on a night shift", 5, 1),
 ("SOP-CONF", 5, "sop_unclear", "we read the radio check as once per entry, not per shift", 3, 0), ("SOP-CONF", 2, "skipped_step", "skipped the gas test since the last reading was fine", 4, 0)]
SRC = ["handover", "near-miss", "maintenance"]; SH = ["Day", "Evening", "Night"]; START = dt.date(2026, 8, 24)
sop = [dict(sop_id=k, step_id=i + 1, title=t, text=x) for k, v in S.items() for i, (t, x) in enumerate(v)]
notes, flags = [], []
for sid, step, typ, q, n, rise in SEEDS:
    for _ in range(n):
        w = random.choices(range(6), [1, 1, 2, 3, 4, 5] if rise else [1] * 6)[0]
        d = START + dt.timedelta(days=7 * w + random.randint(0, 4)); nid = f"N{len(notes) + 1:03d}"; sh = random.choice(SH)
        notes.append(dict(note_id=nid, date=str(d), shift=sh, source=random.choice(SRC), text=f"Shift ran long and {q}. Flagging for the next team."))
        flags.append(dict(flag_id=f"F{len(flags) + 1:03d}", sop_id=sid, step_id=step, note_id=nid, date=str(d), shift=sh, drift_type=typ, quote=q,
                          confidence=round(random.uniform(.55, .97), 2), status=random.choices(["pending", "approved", "rejected"], [6, 3, 1])[0],
                          suggested_fix=f"Draft: revise step {step} to match the practical limit and name who checks it." if typ in ("sop_outdated_or_impractical", "sop_unclear") else ""))
while len(notes) < 100:
    d = START + dt.timedelta(days=random.randint(0, 40)); n = random.randint(1, 9)
    notes.append(dict(note_id=f"N{len(notes) + 1:03d}", date=str(d), shift=random.choice(SH), source=random.choice(SRC),
                      text=random.choice([f"Lockout on line {n} done with every check completed.", f"Charger bay {n} used, gloves and shield worn.", f"Confined-space entry {n} finished, readings normal."])))
low = [f["flag_id"] for f in sorted(flags, key=lambda f: f["confidence"])[:3]]
bench = dict(precision=.84, recall=.76, quote_verified_rate=1.0, notes_per_minute=212.4, matcher_model="Qwen3-4B", judge_model="Qwen3-32B", gpu="AMD Instinct MI300X", false_alarms=low)
amd = dict(endpoint_status="online", cost_per_1000_notes=.42, evolus_api_calls=128, evolus_blocks=["Document extractor", "Workflow with sub-agents"])
for k, v in dict(sop=sop, notes=notes, flags=flags, benchmark=bench, amd=amd).items():
    (DATA / f"{k}.json").write_text(json.dumps(v, indent=1), encoding="utf-8")
print(len(notes), "notes,", len(flags), "flags written")
