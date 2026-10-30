# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

MIN_QUALITY = 0
MAX_QUALITY = 50

AGED_BRIE = "Aged Brie"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"
# The spec names a category ("Conjured" items), not one product, so any
# item whose name starts with this word is conjured.
CONJURED_PREFIX = "Conjured"


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemUpdater(ABC):
    """One day's worth of ageing for one kind of item.

    Subclasses implement `update`. The quality helpers here are the only
    place the 0..50 bounds are enforced, so a new kind cannot bypass them.
    """

    @abstractmethod
    def update(self, item: Item) -> None: ...

    @staticmethod
    def _degrade(item: Item, amount: int) -> None:
        if item.quality > MIN_QUALITY:
            item.quality = max(item.quality - amount, MIN_QUALITY)

    @staticmethod
    def _improve(item: Item, amount: int) -> None:
        if item.quality < MAX_QUALITY:
            item.quality = min(item.quality + amount, MAX_QUALITY)

    @staticmethod
    def _age(item: Item) -> bool:
        """Advance one day and report whether the sell-by date has passed."""
        item.sell_in -= 1
        return item.sell_in < 0


class DegradingItemUpdater(ItemUpdater):
    """Ordinary goods: lose `rate` quality per day, twice that once expired."""

    def __init__(self, rate: int = 1):
        self._rate = rate

    def update(self, item: Item) -> None:
        self._degrade(item, self._rate)
        if self._age(item):
            self._degrade(item, self._rate)


class AgedBrieUpdater(ItemUpdater):
    def update(self, item: Item) -> None:
        self._improve(item, 1)
        if self._age(item):
            self._improve(item, 1)


class BackstagePassUpdater(ItemUpdater):
    def update(self, item: Item) -> None:
        if item.sell_in > 10:
            self._improve(item, 1)
        elif item.sell_in > 5:
            self._improve(item, 2)
        else:
            self._improve(item, 3)
        if self._age(item):
            item.quality = MIN_QUALITY


class LegendaryItemUpdater(ItemUpdater):
    def update(self, item: Item) -> None:
        pass


DEFAULT_UPDATER: ItemUpdater = DegradingItemUpdater()
CONJURED_UPDATER: ItemUpdater = DegradingItemUpdater(rate=2)

UPDATERS_BY_NAME: dict[str, ItemUpdater] = {
    AGED_BRIE: AgedBrieUpdater(),
    BACKSTAGE_PASS: BackstagePassUpdater(),
    SULFURAS: LegendaryItemUpdater(),
}


def updater_for(item: Item) -> ItemUpdater:
    if item.name.startswith(CONJURED_PREFIX):
        return CONJURED_UPDATER
    return UPDATERS_BY_NAME.get(item.name, DEFAULT_UPDATER)


class GildedRose:
    def __init__(self, items: list[Item]):
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            updater_for(item).update(item)
