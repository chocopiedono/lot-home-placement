from LotPlacementSvc import is_compatible
import unittest


def generate_square_coordinates(width: int, height: int) -> list:
    accum = []

    for i in range(width):
        for j in range(height):
            accum.append((i, j))

    return accum


class TestLotPlacement(unittest.TestCase):

    def test_placement_square_happy(self):

        self.home = [3, 3]
        self.lot_boundaries = generate_square_coordinates(5, 5)
        self.setbacks = 1

        self.assertEqual(is_compatible(self.home, self.lot_boundaries, self.setbacks), True)

    def test_placement_square_negative(self):

        self.home = [4, 4]
        self.lot_boundaries = generate_square_coordinates(5, 5)
        self.setbacks = 1

        self.assertEqual(is_compatible(self.home, self.lot_boundaries, self.setbacks), False)

    def test_placement_rect_positive(self):

        self.home = [88, 13]
        self.lot_boundaries = generate_square_coordinates(81, 59)
        self.setbacks = 0

        self.assertEqual(is_compatible(self.home, self.lot_boundaries, self.setbacks), True)

    def test_placement_rect_negative(self):

        self.home = [88, 60]
        self.lot_boundaries = generate_square_coordinates(81, 59)
        self.setbacks = 0

        self.assertEqual(is_compatible(self.home, self.lot_boundaries, self.setbacks), False)

    def test_placement_non_rect_positive(self):

        self.home = [1, 1]
        self.lot_boundaries = [(0, 0),         (0, 2), (0, 3),
                               (1, 0), (1, 1), (1, 2), (1, 3),
                               (2, 0), (2, 1), (2, 2), (2, 3),
                               (3, 0), (3, 1), (3, 2), (3, 3)]
        self.setbacks = 1

        self.assertEqual(is_compatible(self.home, self.lot_boundaries, self.setbacks), True)

    def test_placement_non_rect_negative(self):

        self.home = [1, 1]
        self.lot_boundaries = [(0, 0),         (0, 2), (0, 3),
                               (1, 0),         (1, 2), (1, 3),
                               (2, 0), (2, 1), (2, 2), (2, 3),
                               (3, 0), (3, 1), (3, 2), (3, 3)]
        self.setbacks = 1

        self.assertEqual(is_compatible(self.home, self.lot_boundaries, self.setbacks), False)

    def test_placement_long_rect_positive(self):

        self.home = [2, 1]
        self.lot_boundaries = [(0, 0),         (0, 2), (0, 3),
                               (1, 0), (1, 1), (1, 2), (1, 3),
                               (2, 0), (2, 1), (2, 2), (2, 3),
                               (3, 0), (3, 1), (3, 2), (3, 3)]
        self.setbacks = 1

        self.assertEqual(is_compatible(self.home, self.lot_boundaries, self.setbacks), True)

    def test_placement_long_rect_negative(self):

        self.home = [2, 1]
        self.lot_boundaries = [(0, 0),         (0, 2), (0, 3),
                               (1, 0),         (1, 2), (1, 3),
                               (2, 0), (2, 1), (2, 2), (2, 3),
                               (3, 0), (3, 1), (3, 2), (3, 3)]
        self.setbacks = 1

        self.assertEqual(is_compatible(self.home, self.lot_boundaries, self.setbacks), False)

    def test_placement_long_rect_rev_negative(self):

        self.home = [1, 2]
        self.lot_boundaries = [(0, 0),         (0, 2), (0, 3),
                               (1, 0),         (1, 2), (1, 3),
                               (2, 0), (2, 1), (2, 2), (2, 3),
                               (3, 0), (3, 1), (3, 2), (3, 3)]
        self.setbacks = 1

        self.assertEqual(is_compatible(self.home, self.lot_boundaries, self.setbacks), False)

    def test_placement_very_long_rect_positive(self):

        self.home = [3, 1]
        self.lot_boundaries = [(0, 0),         (0, 2), (0, 3),         (0, 5), (0, 6),
                               (1, 0),         (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                               (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                               (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)]
        self.setbacks = 1

        self.assertEqual(is_compatible(self.home, self.lot_boundaries, self.setbacks), True)


class TestBoundaries(unittest.TestCase):

    def setUp(self):

        self.home = [3, 3]
        self.lot_boundaries = generate_square_coordinates(5, 5)
        self.setbacks = 1

    def test_boundaries_empty(self):

        self.lot_boundaries = []

        with self.assertRaises(ValueError) as ve:
            is_compatible(self.home, self.lot_boundaries, self.setbacks)

        self.assertEqual("Lot's boundaries list is None or empty!", str(ve.exception))

    def test_boundaries_none(self):

        self.lot_boundaries = None

        with self.assertRaises(ValueError) as ve:
            is_compatible(self.home, self.lot_boundaries, self.setbacks)

        self.assertEqual("Lot's boundaries list is None or empty!", str(ve.exception))

    def test_boundaries_element_empty(self):

        self.lot_boundaries = [(0, 0), (0, 2), (0, 3), (0, 4), (0, 5),
                               (1, 0), (1, 2), (1, 3), (1, 4), (),
                               (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (),
                               (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), ()]

        with self.assertRaises(ValueError) as ve:
            is_compatible(self.home, self.lot_boundaries, self.setbacks)

        self.assertEqual("Lot's boundaries have incorrect values", str(ve.exception))

    def test_boundaries_element_none(self):

        self.lot_boundaries = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                               (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), None,
                               (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
                               (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)]

        with self.assertRaises(ValueError) as ve:
            is_compatible(self.home, self.lot_boundaries, self.setbacks)

        self.assertEqual("Lot's boundaries have incorrect values", str(ve.exception))

    def test_boundaries_element_small(self):

        self.lot_boundaries = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                               (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                               (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, None),
                               (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)]

        with self.assertRaises(ValueError) as ve:
            is_compatible(self.home, self.lot_boundaries, self.setbacks)

        self.assertEqual("Lot's boundaries have incorrect values", str(ve.exception))


class TestHomeBlueprint(unittest.TestCase):

    def setUp(self):

        self.home = [3, 3]
        self.lot_boundaries = generate_square_coordinates(5, 5)
        self.setbacks = 1

    def test_home_empty(self):

        self.home = []

        with self.assertRaises(ValueError) as ve:
            is_compatible(self.home, self.lot_boundaries, self.setbacks)

        self.assertEqual("Home blueprint is None or empty!", str(ve.exception))

    def test_home_none(self):

        self.home = None

        with self.assertRaises(ValueError) as ve:
            is_compatible(self.home, self.lot_boundaries, self.setbacks)

        self.assertEqual("Home blueprint is None or empty!", str(ve.exception))