#!/usr/bin/env python3
"""Generate replies and docs with `claude -p` per condition, then score them with lint.py.

Conditions: `baseline` (no system prompt), `micro` (one line asking for plain
British English) and `skill` (SKILL.md appended to the system prompt). Outputs
are cached in --out, so a rerun only scores, and --report-only never calls the
model.

    python3 run.py --out results/2026-10-22
    python3 run.py --out results/2026-10-22 --report-only
"""
import argparse
import concurrent.futures as cf
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lint  # noqa: E402

SKILL = HERE.parent.parent / "skills" / "british-plain-english" / "SKILL.md"
MICRO = "Write in plain British English: UK spelling, short sentences, no jargon."
DOC_KEYS = ["us_spelling", "negative_contraction", "should_may_might", "eg_ie_etc", "em_dash", "semicolon",
            "please", "us_date_or_time", "sentence_over_25", "slop_word", "bold", "title_case_heading", "bullet_capital"]
REPLY_KEYS = ["us_spelling", "negative_contraction", "em_dash", "bold", "header", "bullet", "opener", "closer", "slop_word"]


def generate(prompt, system, model, effort):
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json", "--setting-sources", "",
           "--disallowedTools", "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Skill,Agent"]
    if system:
        cmd += ["--append-system-prompt", system]
    if effort:
        cmd += ["--effort", effort]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=400, cwd="/tmp", stdin=subprocess.DEVNULL)
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return ""
    if isinstance(data, list):
        data = next((d for d in reversed(data) if isinstance(d, dict) and d.get("type") == "result"), {})
    return "" if data.get("is_error") else data.get("result", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--effort", default="low")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    conds = {"baseline": None, "micro": MICRO, "skill": SKILL.read_text()}
    scen = json.loads((HERE / "scenarios.json").read_text())
    jobs = [(s, c, r) for s in scen for c in conds for r in range(1, a.runs + 1)]

    def path(s, c, r):
        return out / f"{c}__{s['id']}__{r}.txt"

    todo = [j for j in jobs if not path(*j).exists() or not path(*j).read_text().strip()]
    if todo and not a.report_only:
        with cf.ThreadPoolExecutor(a.jobs) as ex:
            futs = {ex.submit(generate, s["prompt"], conds[c], a.model, a.effort): (s, c, r) for s, c, r in todo}
            for f in cf.as_completed(futs):
                s, c, r = futs[f]
                text = f.result()
                if text.strip():
                    path(s, c, r).write_text(text)
                print(f"{'ok ' if text.strip() else 'ERR'} {c:8} {s['id']}", file=sys.stderr, flush=True)

    rows = []
    for s, c, r in jobs:
        p = path(s, c, r)
        if p.exists() and p.read_text().strip():
            res = lint.lint(p.read_text(), reply=s["kind"] == "reply")
            rows.append({"cond": c, "id": s["id"], "kind": s["kind"], "run": r, "words": res["words"],
                         "per_100w": res["per_100w"], **res["counts"]})
    (out / "scores.json").write_text(json.dumps(rows, indent=1))
    meta = {"model": a.model, "effort": a.effort, "runs": a.runs}
    (out / "meta.json").write_text(json.dumps(meta))

    for kind, keys in (("doc", DOC_KEYS), ("reply", REPLY_KEYS)):
        print(f"\n### {kind}s ({a.model}, effort {a.effort}): totals over all outputs\n")
        print("| condition | n | words | " + " | ".join(k.replace("_", " ") for k in keys) + " | hits/100w |")
        print("|---|---:|---:|" + "---:|" * (len(keys) + 1))
        for c in conds:
            rs = [x for x in rows if x["cond"] == c and x["kind"] == kind]
            if not rs:
                continue
            n = len(rs)
            print(f"| {c} | {n} | {sum(x['words'] for x in rs) / n:.0f} | "
                  + " | ".join(str(sum(x[k] for x in rs)) for k in keys)
                  + f" | {sum(x['per_100w'] for x in rs) / n:.2f} |")


if __name__ == "__main__":
    main()
