"""Does the task with Recipe360, several times, and scores every run against the reference.

    python with_recipe.py                 # 5 runs of Recipe360's example on data/cards.csv
    python with_recipe.py --runs 20
    python with_recipe.py --data fresh/cards.csv --cutoff 2027-03-31     # a file of your own (needs a licence)

Each run starts from an empty workspace, installs Recipe360's example recipe (card-review) and runs it through
the `recipe360` command, exactly what an agent's `recipe360_run` call does. A run is correct when every field
of its answers is right; the runs are consistent when they all carry the same delivery fingerprint.

The example and its data run without a licence. A file of your own needs one (the 15-day trial is enough).
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from check import differences
from reference import answers

HERE = Path(__file__).resolve().parent


def from_deliverables(folder):
    """The task's answers, read from the recipe's deliverables (report.json and letters.jsonl)."""
    report = json.loads((folder / "report.json").read_text(encoding="utf-8"))
    letters = [x for x in (folder / "letters.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    q, t = report["quality"], report["totals"]
    return {"cards_read": q["cards_read"], "excluded": q["excluded"], "check_digit_failures": q["luhn_invalid"],
            "cvv_incomplete": q["cvv_incomplete"], "clients": t["clients"],
            "concentrated_clients": t["concentrated_clients"], "by_validity": t["by_validity"],
            "by_level": t["by_level"], "by_decision": t["by_decision"],
            "active_without_chip": t["active_without_chip"], "old_pin": t["old_pin"],
            "active_credit_limit": t["active_credit_limit"], "total_limit_reduction": t["total_limit_reduction"],
            "committee_approvals": t["committee_approvals"], "letters": len(letters)}


def one_run(command, data, cutoff):
    home = Path(tempfile.mkdtemp(prefix="recipe360-benchmark-"))
    try:
        subprocess.run([command, "--home", str(home), "example"], check=True, capture_output=True, text=True)
        started = time.perf_counter()
        done = subprocess.run([command, "--home", str(home), "run", "card-review", "--data", str(data),
                               "--param", "cutoff=%s" % cutoff, "--json"], capture_output=True, text=True)
        seconds = time.perf_counter() - started
        if done.returncode != 0:
            return {"error": (done.stderr or done.stdout).strip(), "seconds": seconds}
        res = json.loads(done.stdout)
        return {"fingerprint": res["fingerprint"], "seconds": seconds,
                "answers": from_deliverables(Path(res["run_folder"]))}
    finally:
        shutil.rmtree(home, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--data", default=str(HERE / "data"), help="the folder with cards.csv, or the file itself")
    ap.add_argument("--cutoff", default="2026-10-31")
    ap.add_argument("--command", default="recipe360", help="the recipe360 command, when it is not on the PATH")
    a = ap.parse_args(argv)
    if shutil.which(a.command) is None:
        sys.exit("the recipe360 command was not found: install Recipe360 from https://recipe.pulso360.ai, or give "
                 "its path with --command")
    data = Path(a.data)
    expected = answers(data / "cards.csv" if data.is_dir() else data, a.cutoff)
    version = subprocess.run([a.command, "--version"], capture_output=True, text=True).stdout.strip()
    print("%s · %d run(s) · cut-off %s" % (version, a.runs, a.cutoff))
    exact, fingerprints = 0, set()
    for n in range(1, a.runs + 1):
        r = one_run(a.command, data, a.cutoff)
        if "error" in r:
            print("  run %d: FAILED: %s" % (n, r["error"]))
            continue
        wrong = differences(r["answers"], expected)
        exact += 0 if wrong else 1
        fingerprints.add(r["fingerprint"])
        print("  run %d: %s · fingerprint %s · %.1f s" % (n, "EXACT" if not wrong else "NOT EXACT %s" % sorted(wrong),
                                                         r["fingerprint"][:16], r["seconds"]))
    same = len(fingerprints) == 1
    print("Exact: %d of %d. %s" % (exact, a.runs, ("One fingerprint in every run: %s" % next(iter(fingerprints)))
                                   if same else "%d different fingerprints" % len(fingerprints)))
    return 0 if exact == a.runs and same else 1


if __name__ == "__main__":
    sys.exit(main())
