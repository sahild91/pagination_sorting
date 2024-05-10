import unittest
from pagination_sorting.pagination import Paginator, InvalidPageError

class TestPaginator(unittest.TestCase):
    def setUp(self):
        self.items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.paginator = Paginator(self.items, 3)

    def test_invalid_items_per_page(self):
        with self.assertRaises(ValueError):
            Paginator(self.items, 0)

    def test_invalid_orphans(self):
        with self.assertRaises(ValueError):
            Paginator(self.items, 3, orphans=-1)

    def test_empty_list_pagination(self):
        empty_paginator = Paginator([], 3)
        self.assertEqual(empty_paginator.get_paginated_items(1), [])

        with self.assertRaises(InvalidPageError):
            Paginator([], 3, allow_empty_first_page=False)

    def test_get_page(self):
        self.assertEqual(self.paginator.get_page(1), [1, 2, 3])
        self.assertEqual(self.paginator.get_page(2), [4, 5, 6])
        self.assertEqual(self.paginator.get_page(4), [10])

    def test_invalid_page_number(self):
        with self.assertRaises(InvalidPageError):
            self.paginator.get_page(0)
        with self.assertRaises(InvalidPageError):
            self.paginator.get_page(5)

    def test_has_previous(self):
        self.assertFalse(self.paginator.has_previous(1))
        self.assertTrue(self.paginator.has_previous(2))

    def test_has_next(self):
        self.assertTrue(self.paginator.has_next(1))
        self.assertFalse(self.paginator.has_next(4))

    def test_get_page_range(self):
        self.assertEqual(self.paginator.get_page_range(1), [1, 2, 3, 4])
        self.assertEqual(self.paginator.get_page_range(4), [2, 3, 4])

    def test_get_page_info(self):
        page_info = self.paginator.get_page_info(2)
        self.assertEqual(page_info['current_page'], 2)
        self.assertTrue(page_info['has_previous'])
        self.assertTrue(page_info['has_next'])
        self.assertEqual(page_info['total_pages'], 4)
        self.assertEqual(page_info['total_items'], 10)
        self.assertEqual(page_info['items_per_page'], 3)

    def test_get_paginated_items(self):
        self.assertEqual(self.paginator.get_paginated_items(1), [1, 2, 3])
        self.assertEqual(self.paginator.get_paginated_items(4), [10])
        self.assertIsNone(self.paginator.get_paginated_items(5))

    def test_get_page_range_with_ellipsis(self):
        paginator = Paginator(list(range(1, 21)), 3)
        self.assertEqual(paginator.get_page_range(1), [1, 2, 3, '...', 20])
        self.assertEqual(paginator.get_page_range(4), [1, '...', 3, 4, 5, '...', 20])
        self.assertEqual(paginator.get_page_range(7), [1, '...', 6, 7, 8, 9, 10])

    def test_get_page_url(self):
        self.assertEqual(self.paginator.get_page_url(1), '?page=1')
        self.assertEqual(self.paginator.get_page_url(2, base_url='/products'), '/products?page=2')
        self.assertEqual(self.paginator.get_page_url(3, query_param='pg'), '?pg=3')

    def test_render_pagination(self):
        pagination_html = self.paginator.render_pagination(2)
        self.assertIn('<ul class="pagination">', pagination_html)
        self.assertIn('<li class="active"><span>2</span></li>', pagination_html)
        self.assertIn('<a href="?page=1">&laquo; Previous</a>', pagination_html)
        self.assertIn('<a href="?page=3">Next &raquo;</a>', pagination_html)

    def test_custom_template(self):
        custom_template = '<div class="custom-pagination">{page_info["current_page"]} of {page_info["total_pages"]}</div>'
        self.paginator.set_custom_template(custom_template)
        rendered_html = self.paginator.render_pagination(2)
        self.assertEqual(rendered_html, '<div class="custom-pagination">2 of 4</div>')

    def test_paginate_with_sorting(self):
        page_info = self.paginator.paginate(2, sort_key=lambda x: -x)
        self.assertEqual(page_info['items'], [7, 6, 5])

if __name__ == '__main__':
    unittest.main()