"""The right answers of the task in task.md, worked out in plain Python from the rules as they are written there.

It uses nothing from Recipe360: it is an independent calculation, short enough to read in one sitting, that both
ways of doing the task are scored against.

    python reference.py                               # data/cards.csv, cut-off 2026-10-31
    python reference.py fresh/cards.csv --cutoff 2027-03-31
"""
import argparse
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LENGTH = {"Visa": 16, "Mastercard": 16, "Amex": 15, "Discover": 16}
PREFIX = {"Visa": ("4",), "Mastercard": ("5", "2"), "Amex": ("3",), "Discover": ("6",)}
POINTS = (("no_chip", 30), ("old_pin", 20), ("three_cards", 15), ("big_credit", 15), ("concentrated", 10),
          ("cvv_incomplete", 10), ("dark_web", 40))
LETTER_DECISIONS = {"renew", "renew_early", "reissue_chip", "force_pin_change", "cut_limit"}


def months(text):
    """'08/2026' -> the number of that month, counted from year 0."""
    month, year = text.strip().split("/")
    return int(year) * 12 + int(month) - 1


def passes_luhn(number):
    total = 0
    for position, digit in enumerate(reversed(number)):
        n = int(digit)
        if position % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def money(text):
    return int(text.replace("$", "").replace(",", "").strip())


def answers(path, cutoff):
    year, month = int(cutoff[:4]), int(cutoff[5:7])
    cutoff_month = year * 12 + month - 1
    with open(path, newline="", encoding="utf-8") as fh:
        cards = list(csv.DictReader(fh))

    # 1. Data quality, over every card in the file.
    kept = []
    excluded = check_digit_failures = cvv_incomplete = 0
    for c in cards:
        number, brand = c["card_number"], c["card_brand"]
        digits = number.isdigit()
        well_formed = digits and len(number) == LENGTH.get(brand, 0) and number.startswith(PREFIX.get(brand, ()))
        c["cvv_incomplete"] = len(c["cvv"].strip()) < (4 if brand == "Amex" else 3)
        check_digit_failures += 0 if (digits and passes_luhn(number)) else 1
        cvv_incomplete += 1 if c["cvv_incomplete"] else 0
        if not well_formed or months(c["expires"]) < months(c["acct_open_date"]):
            excluded += 1
        else:
            kept.append(c)

    # 2 to 4. Expiry, PIN and chip.
    for c in kept:
        expires = months(c["expires"])
        c["validity"] = "expired" if expires < cutoff_month else \
            "expiring_soon" if expires <= cutoff_month + 3 else "valid"
        c["limit"] = money(c["credit_limit"])
        c["credit"] = c["card_type"] == "Credit"
        c["old_pin"] = year - int(c["year_pin_last_changed"]) >= 5
        c["no_chip"] = c["has_chip"] == "NO"

    # 5. Exposure per client.
    clients = {}
    for c in kept:
        client = clients.setdefault(c["client_id"], {"active": 0, "active_credit_limit": 0})
        if c["validity"] != "expired":
            client["active"] += 1
            if c["credit"]:
                client["active_credit_limit"] += c["limit"]
    for client in clients.values():
        client["concentrated"] = client["active"] >= 5 or client["active_credit_limit"] > 100000

    # 6 to 8. Risk score, credit-limit cut and decision.
    for c in kept:
        signals = {"no_chip": c["no_chip"], "old_pin": c["old_pin"], "three_cards": int(c["num_cards_issued"]) == 3,
                   "big_credit": c["credit"] and c["limit"] > 50000,
                   "concentrated": clients[c["client_id"]]["concentrated"], "cvv_incomplete": c["cvv_incomplete"],
                   "dark_web": c["card_on_dark_web"] == "Yes"}
        score = min(100, sum(points for name, points in POINTS if signals[name]))
        c["level"] = "low" if score < 20 else "medium" if score < 40 else "high" if score < 60 else "critical"
        active_credit = c["credit"] and c["validity"] != "expired"
        cut = active_credit and c["level"] in ("high", "critical") and c["limit"] > 10000
        recommended = (c["limit"] * 8 // 10) // 100 * 100 if cut else None
        c["reduction"] = c["limit"] - recommended if cut else 0
        c["committee"] = cut and c["reduction"] > 4000
        if c["validity"] == "expired" and c["level"] == "critical":
            c["decision"] = "do_not_renew"
        elif c["validity"] == "expired":
            c["decision"] = "renew"
        elif active_credit and c["limit"] == 0:
            c["decision"] = "review_limit"
        elif c["committee"]:
            c["decision"] = "cut_limit_committee"
        elif c["reduction"] > 0:
            c["decision"] = "cut_limit"
        elif c["no_chip"]:
            c["decision"] = "reissue_chip"
        elif c["old_pin"]:
            c["decision"] = "force_pin_change"
        elif c["validity"] == "expiring_soon":
            c["decision"] = "renew_early"
        else:
            c["decision"] = "no_action"

    def count(key, names):
        return {name: sum(1 for c in kept if c[key] == name) for name in names}

    return {
        "cards_read": len(cards), "excluded": excluded, "check_digit_failures": check_digit_failures,
        "cvv_incomplete": cvv_incomplete,
        "clients": len(clients), "concentrated_clients": sum(1 for x in clients.values() if x["concentrated"]),
        "by_validity": count("validity", ("expired", "expiring_soon", "valid")),
        "by_level": count("level", ("low", "medium", "high", "critical")),
        "by_decision": count("decision", ("do_not_renew", "renew", "review_limit", "cut_limit_committee", "cut_limit",
                                          "reissue_chip", "force_pin_change", "renew_early", "no_action")),
        "active_without_chip": sum(1 for c in kept if c["validity"] != "expired" and c["no_chip"]),
        "old_pin": sum(1 for c in kept if c["old_pin"]),
        "active_credit_limit": sum(c["limit"] for c in kept if c["validity"] != "expired" and c["credit"]),
        "total_limit_reduction": sum(c["reduction"] for c in kept),
        "committee_approvals": sum(1 for c in kept if c["committee"]),
        "letters": len({c["client_id"] for c in kept if c["decision"] in LETTER_DECISIONS}),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("data", nargs="?", default=str(HERE / "data" / "cards.csv"))
    ap.add_argument("--cutoff", default="2026-10-31", help="the cut-off date, YYYY-MM-DD")
    a = ap.parse_args()
    json.dump(answers(a.data, a.cutoff), sys.stdout, indent=1)
    sys.stdout.write("\n")
