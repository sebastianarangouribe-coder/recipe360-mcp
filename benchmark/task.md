# The task: a card portfolio review

A bank's risk team reviews its card portfolio every month. You get one file, `cards.csv`, and a cut-off date.
Work through the rules below and write the answers to `answers.json`.

This is the whole task as a person would brief it. It is the same process Recipe360's example recipe
(`card-review`) runs.

## The file

`cards.csv` has one card per row:

| Column | What it holds |
| --- | --- |
| `id` | The card's number in the file |
| `client_id` | The client who holds it |
| `card_brand` | Visa, Mastercard, Amex or Discover |
| `card_type` | Credit, Debit or Debit (Prepaid) |
| `card_number` | The card number |
| `expires` | Month and year, as `MM/YYYY` |
| `cvv` | The security code |
| `has_chip` | `YES` or `NO` |
| `num_cards_issued` | How many cards were issued on the account |
| `credit_limit` | The limit, written like `$24,000` |
| `acct_open_date` | Month and year the account was opened, as `MM/YYYY` |
| `year_pin_last_changed` | A year |
| `card_on_dark_web` | `Yes` or `No` |

The cut-off date for this run is **2026-10-31**.

## The rules, in order

**1. Data quality.** For every card in the file:

- It is **excluded** from the rest of the review when either of these is true:
  - its number is not made only of digits, or does not have the length of its brand (Visa 16, Mastercard 16,
    Amex 15, Discover 16), or does not start with its brand's prefix (Visa `4`; Mastercard `5` or `2`; Amex `3`;
    Discover `6`);
  - it expires in a month earlier than the month its account was opened.
- Its number **fails the check digit** when it is not made only of digits or does not pass the Luhn check.
- Its **CVV is incomplete** when, without spaces around it, it has fewer than 3 characters (fewer than 4 for
  Amex).

The last two are counted over every card in the file, excluded ones too. Everything from here on uses only the
cards that were not excluded.

**2. Expiry.** A card is **expired** when it expires in a month before the cut-off's month. It is **expiring
soon** when it expires in the cut-off's month or in one of the three months after it. Otherwise it is **valid**.

**3. PIN.** The PIN's age is the cut-off's year minus the year the PIN was last changed. A PIN is **old** at
5 years or more.

**4. Chip.** A card has **no chip** when `has_chip` is `NO`.

**5. Exposure per client.** For each client, count the cards that are not expired (their **active** cards), and
add up the credit limits of their cards that are not expired and whose type is exactly `Credit` (their **active
credit limit**). A client is **concentrated** with 5 or more active cards, or an active credit limit above
100,000.

**6. Risk score.** Each card starts at 0 and adds:

| When | Points |
| --- | --- |
| It has no chip | 30 |
| Its PIN is old | 20 |
| Exactly 3 cards were issued on the account | 15 |
| Its type is `Credit` and its limit is above 50,000 | 15 |
| Its client is concentrated | 10 |
| Its CVV is incomplete | 10 |
| It is on the dark web (`Yes`) | 40 |

The score never goes above 100. Its **level** is low below 20, medium below 40, high below 60, and critical
from 60 up.

**7. Credit-limit cuts.** A card gets a cut when its type is `Credit`, it is not expired, its level is high or
critical, and its limit is above 10,000. The **recommended limit** is 80% of the limit, rounded down to the
hundred. The **reduction** is the limit minus the recommended limit; it is 0 for a card with no cut. A cut
**needs the committee** when the reduction is above 4,000. Separately, a card is a **credit card without a
limit** when its type is `Credit`, it is not expired, and its limit is 0.

**8. One decision per card.** Take the first that applies:

1. expired and critical: `do_not_renew`
2. expired: `renew`
3. a credit card without a limit: `review_limit`
4. its cut needs the committee: `cut_limit_committee`
5. it has a cut: `cut_limit`
6. it has no chip: `reissue_chip`
7. its PIN is old: `force_pin_change`
8. it is expiring soon: `renew_early`
9. otherwise: `no_action`

**9. Letters.** One letter goes to each client who has at least one card whose decision is `renew`,
`renew_early`, `reissue_chip`, `force_pin_change` or `cut_limit`.

## What to deliver

Write `answers.json` with exactly these fields, all whole numbers:

```json
{
  "cards_read": 0,
  "excluded": 0,
  "check_digit_failures": 0,
  "cvv_incomplete": 0,
  "clients": 0,
  "concentrated_clients": 0,
  "by_validity": {"expired": 0, "expiring_soon": 0, "valid": 0},
  "by_level": {"low": 0, "medium": 0, "high": 0, "critical": 0},
  "by_decision": {"do_not_renew": 0, "renew": 0, "review_limit": 0, "cut_limit_committee": 0, "cut_limit": 0,
                  "reissue_chip": 0, "force_pin_change": 0, "renew_early": 0, "no_action": 0},
  "active_without_chip": 0,
  "old_pin": 0,
  "active_credit_limit": 0,
  "total_limit_reduction": 0,
  "committee_approvals": 0,
  "letters": 0
}
```

- `cards_read` is every card in the file. `clients` is the clients with at least one card that was not
  excluded.
- `active_without_chip` is the cards that are not expired and have no chip. `old_pin` is the cards with an old
  PIN.
- `active_credit_limit` is the sum, over the whole portfolio, of the limits of the cards that are not expired
  and whose type is `Credit`. `total_limit_reduction` is the sum of every reduction.
- `committee_approvals` is the cuts that need the committee. `letters` is the letters written.

`python check.py answers.json` says whether every field is right.
