"""Scores one attempt at the task: every field of answers.json against the reference's.

    python check.py answers.json                              # data/cards.csv, cut-off 2026-10-31
    python check.py answers.json --data fresh/cards.csv --cutoff 2027-03-31

Prints EXACT when every field is right; otherwise each field that is not, with what was expected. An attempt
counts as correct only when it is EXACT: a report that is nearly right is a wrong report.
"""
import argparse
import json
import sys
from pathlib import Path

from reference import answers

HERE = Path(__file__).resolve().parent


def flat(doc, prefix=""):
    out = {}
    for k, v in (doc or {}).items():
        if isinstance(v, dict):
            out.update(flat(v, prefix + k + "."))
        else:
            out[prefix + k] = v
    return out


def differences(given, expected):
    """The fields that are wrong, missing or not asked for: {field: (given, expected)}."""
    g, e = flat(given), flat(expected)
    return {k: (g.get(k, "missing"), e.get(k, "not asked for")) for k in sorted(set(g) | set(e)) if g.get(k) != e.get(k)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("answers", help="the answers.json to score")
    ap.add_argument("--data", default=str(HERE / "data" / "cards.csv"))
    ap.add_argument("--cutoff", default="2026-10-31")
    a = ap.parse_args()
    try:
        given = json.loads(Path(a.answers).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("NOT EXACT: %s cannot be read as JSON (%s)" % (a.answers, e))
        sys.exit(1)
    wrong = differences(given, answers(a.data, a.cutoff))
    if not wrong:
        print("EXACT: all %d fields are right." % len(flat(given)))
        sys.exit(0)
    print("NOT EXACT: %d field(s) differ." % len(wrong))
    for field, (got, want) in wrong.items():
        print("  %s: got %r, expected %r" % (field, got, want))
    sys.exit(1)
