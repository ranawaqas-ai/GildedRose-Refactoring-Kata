# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

AGED_BRIE = "Aged Brie"
BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"


def update(name, sell_in, quality):
    item = Item(name, sell_in, quality)
    GildedRose([item]).update_quality()
    return item.sell_in, item.quality


class NormalItemTest(unittest.TestCase):
    def test_quality_and_sell_in_drop_by_one(self):
        self.assertEqual((9, 19), update("Elixir", 10, 20))

    def test_quality_drops_twice_as_fast_after_sell_by(self):
        self.assertEqual((-1, 18), update("Elixir", 0, 20))

    def test_quality_never_negative(self):
        self.assertEqual((4, 0), update("Elixir", 5, 0))

    def test_quality_never_negative_after_sell_by(self):
        self.assertEqual((-1, 0), update("Elixir", 0, 1))

    def test_sell_in_keeps_decreasing_after_sell_by(self):
        self.assertEqual((-3, 0), update("Elixir", -2, 0))


class AgedBrieTest(unittest.TestCase):
    def test_quality_increases(self):
        self.assertEqual((1, 1), update(AGED_BRIE, 2, 0))

    def test_quality_increases_twice_as_fast_after_sell_by(self):
        self.assertEqual((-1, 2), update(AGED_BRIE, 0, 0))

    def test_quality_capped_at_fifty(self):
        self.assertEqual((1, 50), update(AGED_BRIE, 2, 50))

    def test_quality_capped_at_fifty_after_sell_by(self):
        self.assertEqual((-1, 50), update(AGED_BRIE, 0, 49))


class SulfurasTest(unittest.TestCase):
    def test_never_changes(self):
        self.assertEqual((0, 80), update(SULFURAS, 0, 80))

    def test_never_changes_past_sell_by(self):
        self.assertEqual((-1, 80), update(SULFURAS, -1, 80))


class BackstagePassTest(unittest.TestCase):
    def test_increases_by_one_more_than_ten_days_out(self):
        self.assertEqual((10, 21), update(BACKSTAGE, 11, 20))

    def test_increases_by_two_at_ten_days(self):
        self.assertEqual((9, 22), update(BACKSTAGE, 10, 20))

    def test_increases_by_two_at_six_days(self):
        self.assertEqual((5, 22), update(BACKSTAGE, 6, 20))

    def test_increases_by_three_at_five_days(self):
        self.assertEqual((4, 23), update(BACKSTAGE, 5, 20))

    def test_increases_by_three_on_last_day(self):
        self.assertEqual((0, 23), update(BACKSTAGE, 1, 20))

    def test_drops_to_zero_after_concert(self):
        self.assertEqual((-1, 0), update(BACKSTAGE, 0, 20))

    def test_stays_zero_after_concert(self):
        self.assertEqual((-2, 0), update(BACKSTAGE, -1, 0))

    def test_quality_capped_at_fifty(self):
        self.assertEqual((4, 50), update(BACKSTAGE, 5, 49))

    def test_quality_does_not_exceed_fifty(self):
        self.assertEqual((14, 50), update(BACKSTAGE, 15, 50))


if __name__ == '__main__':
    unittest.main()
