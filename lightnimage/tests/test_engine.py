from unittest import TestCase
import math

from lightnimage.engine import SimpleAreaGroupingEngine


class TestSimpleAreaGroupingEngine(TestCase):

    def test_area_grouping_engine_single_area(self):
        areas = [((0, 0), (1, 1))]
        engine = SimpleAreaGroupingEngine({})
        grouped_areas = engine(areas)
        self.assertListEqual(areas, grouped_areas)

    def test_area_grouping_basically_correct(self):
        # Creating two areas, that are insanely small and really close, so they have to be grouped
        areas = [
            ((0, 2), (0, 2)),
            ((0, 2), (3, 4))
        ]

        engine = SimpleAreaGroupingEngine({})
        groups = engine.group_areas(areas)  # type: dict
        self.assertListEqual(sorted(areas), sorted(groups[0]))

        # Creating areas with really large proportions, so that they do not get grouped for sure
        areas = [
            ((100, 1000), (100, 10000)),
            ((100000, 10000000), (100000000, 10000000000000))
        ]

        engine = SimpleAreaGroupingEngine({})
        combined_areas = engine(areas)
        self.assertListEqual(sorted(areas), sorted(combined_areas))

    def test_area_size_calculated_correctly(self):
        area = ((0, 10), (0, 5))
        size = SimpleAreaGroupingEngine.area_size(area)
        self.assertEqual(50, size)

    def test_distance_between_areas_calculated_correctly(self):
        area1 = ((1, 3), (1, 3))
        area2 = ((5, 7), (6, 8))
        distance = SimpleAreaGroupingEngine.area_distance(area1, area2)
        self.assertAlmostEqual(math.sqrt(41), distance)

    def test_center_of_area_calculated_correctly(self):
        area = ((156, 278), (354, 800))
        center = SimpleAreaGroupingEngine.area_center(area)
        self.assertEqual((217, 577), center)

    def test_math_infinite(self):
        self.assertTrue(math.inf > 800000)
        self.assertTrue(math.inf > 0)
