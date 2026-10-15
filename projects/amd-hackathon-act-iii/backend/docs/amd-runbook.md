# AMD Developer Cloud runbook

Who does what: Shreyank runs these commands on the AMD machine and pastes the output back. Claude fixes code from the output.
Plan: the pipeline runs ON the AMD machine, next to vLLM. The model address is localhost, so nothing is exposed and no address goes into the repo.

## 0. Machine facts (fill in when known)

| Fact                                        | Value                                                                                                         |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| GPU                                         | PLACEHOLDER (plan: 1x MI300X, 192 GB)                                                                         |
| Price per hour                              | PLACEHOLDER                                                                                                   |
| Credit hours (100 / price per hour)         | PLACEHOLDER                                                                                                   |
| OS                                          | PLACEHOLDER                                                                                                   |
| Python version                              | PLACEHOLDER (pre-built vLLM ROCm wheels need Python 3.12, per the research report; verify)                    |
| ROCm preinstalled                           | PLACEHOLDER                                                                                                   |
| Docker preinstalled                         | PLACEHOLDER                                                                                                   |
| vLLM preinstalled                           | PLACEHOLDER                                                                                                   |
| Model name for the judge                    | PLACEHOLDER (one open instruct model of about 7-8 billion parameters; check the exact name on the model page) |
| How to log in (ssh command or web terminal) | PLACEHOLDER                                                                                                   |

## 1. Check the machine

```bash
rocm-smi            # GPU visible?
python3 --version
docker --version
tmux -V             # tmux keeps a command running after you close the terminal
```

Paste the output to Claude. It decides how vLLM is installed (PLACEHOLDER: install steps come from the vLLM-on-ROCm docs once the machine facts are known).

## 2. Get the code

```bash
git clone https://github.com/Shreyankkkkk/procedure-drift-finder
cd procedure-drift-finder/backend
pip install -r requirements.txt
python scripts/check_data.py     # every line should say PASS
```

## 3. Start the model server (in tmux, so it keeps running)

```bash
tmux new -s vllm
vllm serve <MODEL_NAME> --port 8000      # PLACEHOLDER: exact command and flags after step 1
```

Wait until it prints that it is ready. Detach with Ctrl+B, then D. Reattach later with `tmux attach -t vllm`.

In a second terminal on the same machine:

```bash
curl http://localhost:8000/v1/models
```

It should list the model name. Use that exact name below.

## 4. Settings for the pipeline (environment variables, never committed)

```bash
export JUDGE_BASE_URL=http://localhost:8000/v1
export JUDGE_MODEL=<MODEL_NAME as listed by /v1/models>
# export JUDGE_API_KEY=...    only if the server was started with a key
```

Variables last only for this terminal session. Set them again in any new terminal.

## 5. The GPU runs (from the backend folder on the machine)

| Run                | Command                                                 | Check                                                  | Paste to Claude                                             |
| ------------------ | ------------------------------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------- |
| 1. Smoke test      | `python -m src.pipeline --limit 1`                      | finishes, no `failed` line, `output/flags.json` exists | the printed lines and `output/flags.json`                   |
| 2. Ten notes       | `python -m src.pipeline --limit 10`                     | few or no failed notes                                 | printed lines, `output/flags.json`, `output/run_stats.json` |
| 3. Full run, timed | `python -m src.pipeline`                                | 200 notes done, failed list empty                      | printed lines, `output/run_stats.json`                      |
| 3b. Score it       | `python -m src.evaluation.benchmark --gpu "<GPU name>"` | prints precision, recall                               | `output/benchmark.json`, `output/benchmark_details.json`    |
| 4. Final run       | same as 3 and 3b, after the fixes                       | nothing new broken                                     | same as 3 and 3b                                            |

Each run overwrites the files in `output/`. Copy a run's files out before the next one if you want to keep them.
Stop and send the output to Claude if a run fails. Do not edit files on the machine; Claude fixes them in Foundations and you pull again with `git pull`.

## 6. Numbers to calculate after run 3 (Claude does the arithmetic from `run_stats.json`)

- Minutes for 1,000 notes = 1000 / notes_per_minute
- Cost per 1,000 notes = (minutes for 1,000 notes / 60) x price per hour
- Fix-round cap = floor(minutes from first accuracy run to freeze / minutes per full run)
- Credit hours left = credit hours total minus the hours the machine has been on

## 7. Get the results off the machine

PLACEHOLDER: depends on how you log in (scp command or web download). Files needed: `output/flags.json`, `output/benchmark.json`. They go into `data/` and `data/demo/` for the front end.

## 8. When idle

Shut the machine down when you are not running anything. Credits run while it is on.
Save the proof: screenshot of `rocm-smi` and of the vLLM server running (needed for the AMD proof).

## If something fails

| Symptom                                         | Likely cause                              | Try                                                               |
| ----------------------------------------------- | ----------------------------------------- | ----------------------------------------------------------------- |
| `Missing environment variable(s)`               | step 4 not done in this terminal          | export both variables again                                       |
| Connection refused                              | vLLM not running or not ready             | `tmux attach -t vllm`, check it printed ready                     |
| 404 or `model not found`                        | `JUDGE_MODEL` does not match `/v1/models` | copy the name exactly                                             |
| `note N0xx failed: no JSON list in model reply` | model answered in words                   | send Claude the note and run 2 output (prompt wording is the fix) |
| Many flags dropped by the quote check           | model paraphrases quotes                  | send Claude `output/run_stats.json`                               |
| Run very slow                                   | request time not measured yet             | send Claude the stats; timeout and retry are set from it          |
