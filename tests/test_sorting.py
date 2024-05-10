import unittest
from pagination_sorting.sorting import sort_items

class TestSorting(unittest.TestCase):
    def test_sort_items(self):
        items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        self.assertEqual(sort_items(items), [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9])
        self.assertEqual(sort_items(items, reverse=True), [9, 6, 5, 5, 5, 4, 3, 3, 2, 1, 1])
        self.assertEqual(sort_items(items, key=lambda x: x % 2), [2, 4, 6, 1, 1, 3, 3, 5, 5, 5, 9])

if __name__ == '__main__':
    unittest.main()