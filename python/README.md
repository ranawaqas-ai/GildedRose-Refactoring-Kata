# Gilded Rose in Python

For the exercise instructions see the [top level README](../README.md) and
[requirements](../GildedRoseRequirements.md).

## Setup and tests

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```sh
uv sync --group test
uv run pytest
```

Two kinds of test run:

- `tests/test_gilded_rose.py` holds one unit test per requirement, including
  the boundaries (sell_in at 11, 10, 6, 5, 1, 0; quality at 0, 1, 49, 50).
- `tests/test_gilded_rose_approvals.py` runs the 30-day text fixture and
  compares it against `tests/approved_files/*.approved.txt`. If it fails, a
  `.received.txt` file appears next to the approved one; inspect the diff and
  rename it over the approved file to accept the new output.

Branch coverage of `gilded_rose.py` is 100%:

```sh
uv run coverage run -m pytest && uv run coverage report
```

To print the fixture by hand for N days:

```sh
uv run python texttest_fixture.py N
```

## Design

`GildedRose.update_quality` looks up an `ItemUpdater` for each item by name
and delegates to it. Each item kind owns its own flat update:

| Item kind | Updater | Rule |
| --- | --- | --- |
| ordinary goods | `DegradingItemUpdater(rate=1)` | -1 a day, -2 once expired |
| Conjured ... | `DegradingItemUpdater(rate=2)` | -2 a day, -4 once expired |
| Aged Brie | `AgedBrieUpdater` | +1 a day, +2 once expired |
| Backstage passes | `BackstagePassUpdater` | +1, +2 within 10 days, +3 within 5, 0 after |
| Sulfuras | `LegendaryItemUpdater` | never changes |

The 0 and 50 quality bounds are enforced only in the `_degrade` and
`_improve` helpers on the base class, so a new updater cannot bypass them.
`Item` is unchanged, as the kata requires.

Conjured items are matched by the `Conjured` name prefix rather than an exact
name because the requirement describes a category of items, not one product.

Quality values outside 0..50 (other than Sulfuras at 80) are never produced by
this code, but if one is supplied the original behaviour is kept: an
out-of-range value is left alone rather than clamped.

### Adding an item kind

1. Subclass `ItemUpdater` and implement `update(item)`, using `_degrade`,
   `_improve` and `_age`.
2. Register it in `UPDATERS_BY_NAME` (or add a rule to `updater_for` if it is
   matched by something other than the exact name).
3. Add its tests to `tests/test_gilded_rose.py` and, if the fixture includes
   it, re-approve the golden master.

## Development history

The commits on this branch follow the order a refactor should: approve the
golden master of the original code, pin every rule with unit tests, refactor
with both nets unchanged, then add the Conjured feature as one new updater
plus tests, with the approval diff touching only the Conjured lines.
