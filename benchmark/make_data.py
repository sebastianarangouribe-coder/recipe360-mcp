"""Writes the benchmark's card file. Every value is invented; the card numbers use the brands' well-known test
prefixes. The same seed always writes the same file, and the default seed writes data/cards.csv exactly as it is
in this folder (and as Recipe360's own example ships it).

    python make_data.py                              # data/cards.csv, 400 cards
    python make_data.py --seed 7 --cards 2000 --out fresh/cards.csv   # a file nobody has seen before

A fresh file shows that nothing here is memorised: reference.py works the right answers out again for any file.
"""
import argparse
import csv
import random
from pathlib import Path

COLUMNS = ["id", "client_id", "card_brand", "card_type", "card_number", "expires", "cvv", "has_chip",
           "num_cards_issued", "credit_limit", "acct_open_date", "year_pin_last_changed", "card_on_dark_web"]
TEST_PREFIX = {"Visa": "411111", "Mastercard": "555555", "Amex": "378282", "Discover": "601111"}
LENGTH = {"Visa": 16, "Mastercard": 16, "Amex": 15, "Discover": 16}


def luhn_digit(body: str) -> str:
    total = 0
    for i, d in enumerate(reversed(body)):
        n = int(d) * (2 if i % 2 == 0 else 1)
        total += n - 9 if n > 9 else n
    return str((10 - total % 10) % 10)


def card_number(rnd: random.Random, brand: str) -> str:
    prefix = TEST_PREFIX[brand]
    body = prefix + "".join(rnd.choice("0123456789") for _ in range(LENGTH[brand] - len(prefix) - 1))
    number = body + luhn_digit(body)
    roll = rnd.random()
    if roll < 0.04:                                   # a typo: the check digit no longer matches
        number = number[:-1] + str((int(number[-1]) + 1) % 10)
    elif roll < 0.06:                                 # a digit lost on the way: wrong length for the brand
        number = number[:-1]
    return number


def rows(n_cards: int = 400, n_clients: int = 120, seed: int = 20261030):
    rnd = random.Random(seed)
    clients = [1000 + i for i in range(1, n_clients + 1)]
    weights = [6 if i % 17 == 0 else 1 for i in range(n_clients)]   # a few clients hold many cards
    for i in range(1, n_cards + 1):
        brand = rnd.choices(list(TEST_PREFIX), weights=[50, 35, 8, 7])[0]
        kind = rnd.choices(["Credit", "Debit", "Debit (Prepaid)"], weights=[40, 50, 10])[0]
        opened_year = rnd.randint(2008, 2024)
        expires_year = rnd.randint(2024, 2031)
        if rnd.random() < 0.02:                       # opened after it expires: the file is wrong
            opened_year = expires_year + 1
        cvv = "".join(rnd.choice("0123456789") for _ in range(4 if brand == "Amex" else 3))
        if rnd.random() < 0.03:
            cvv = cvv[:-1]
        if kind == "Credit":
            limit = 0 if rnd.random() < 0.03 else rnd.choice([rnd.randint(5, 60), rnd.randint(40, 90)]) * 1000
        else:
            limit = rnd.randint(1, 20) * 500
        yield {
            "id": i,
            "client_id": rnd.choices(clients, weights=weights)[0],
            "card_brand": brand,
            "card_type": kind,
            "card_number": card_number(rnd, brand),
            "expires": "%02d/%d" % (rnd.randint(1, 12), expires_year),
            "cvv": cvv,
            "has_chip": "NO" if rnd.random() < 0.1 else "YES",
            "num_cards_issued": rnd.choices([1, 2, 3], weights=[70, 22, 8])[0],
            "credit_limit": "${:,}".format(limit),
            "acct_open_date": "%02d/%d" % (rnd.randint(1, 12), opened_year),
            "year_pin_last_changed": rnd.randint(2012, 2026),
            "card_on_dark_web": "Yes" if rnd.random() < 0.02 else "No",
        }


def write(out: Path, n_cards: int = 400, n_clients: int = 120, seed: int = 20261030) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows(n_cards, n_clients, seed))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seed", type=int, default=20261030)
    ap.add_argument("--cards", type=int, default=400)
    ap.add_argument("--clients", type=int, default=120)
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "data" / "cards.csv"))
    a = ap.parse_args()
    print(write(Path(a.out), a.cards, a.clients, a.seed))
