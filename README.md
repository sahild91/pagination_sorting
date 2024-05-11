# Pagination and Sorting Package

[![PyPI Version](https://img.shields.io/pypi/v/pagination-sorting)](https://pypi.org/project/pagination-sorting/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/sahild91/pagination-sorting/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/pagination-sorting)](https://pypi.org/project/pagination-sorting/)

A powerful and flexible pagination and sorting package for arrays and lists, compatible with Django and Flask-based apps. It provides a wide range of features to simplify pagination and sorting in your Python projects.

## Features

- Paginate lists or arrays of any type
- Customize the number of items per page and handle orphaned items

* Support for multiple pagination styles:
  - Traditional page-based pagination
  - Infinite scrolling
  - Load more button
* Generate page URLs with customizable query parameters
* Render pagination controls as HTML with default or custom templates
* Integrate sorting functionality with pagination
* Comprehensive pagination information, including page range, previous/next page URLs, and more
* Extensive documentation and usage examples

## Installation

You can install the package using pip:

```bash
pip install pagination-sorting
```

## Usage

### Pagination

```python
from pagination_sorting.pagination import Paginator

items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
paginator = Paginator(items, items_per_page=3)

# Get paginated items
page1_items = paginator.get_page(1)
print(page1_items)  # Output: [1, 2, 3]

# Check if there are previous or next pages
has_previous = paginator.has_previous(2)
print(has_previous)  # Output: True

has_next = paginator.has_next(4)
print(has_next)  # Output: False

# Get page range with ellipsis
page_range = paginator.get_page_range(4, num_pages=5, left_edge=2, right_edge=2)
print(page_range)  # Output: [1, '...', 3, 4, 5, '...', 10]

# Get page information
page_info = paginator.get_page_info(2)
print(page_info)
# Output:
# {
#     'current_page': 2,
#     'has_previous': True,
#     'has_next': True,
#     'total_pages': 4,
#     'total_items': 10,
#     'items_per_page': 3,
#     'items': [4, 5, 6],
#     'start_index': 4,
#     'end_index': 6,
#     'previous_page_url': '?page=1',
#     'next_page_url': '?page=3'
# }

# Generate page URL
page_url = paginator.get_page_url(3, base_url='/products', query_param='pg')
print(page_url)  # Output: /products?pg=3

# Render pagination controls
pagination_html = paginator.render_pagination(2)
print(pagination_html)
# Output:
# <ul class="pagination">
#     <li><a href="?page=1">&laquo; Previous</a></li>
#     <li><a href="?page=1">1</a></li>
#     <li class="active"><span>2</span></li>
#     <li><a href="?page=3">3</a></li>
#     <li><a href="?page=4">4</a></li>
#     <li><a href="?page=3">Next &raquo;</a></li>
# </ul>

# Set custom pagination template
custom_template = '<div class="custom-pagination">{page_info["current_page"]} of {page_info["total_pages"]}</div>'
paginator.set_custom_template(custom_template)
rendered_html = paginator.render_pagination(2)
print(rendered_html)  # Output: <div class="custom-pagination">2 of 4</div>

# Paginate with sorting
page_info = paginator.paginate(2, sort_key=lambda x: -x)
print(page_info['items'])  # Output: [7, 6, 5]
```

### Sorting

```python
from pagination_sorting.sorting import sort_items

items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
sorted_items = sort_items(items)
print(sorted_items)  # Output: [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]

reverse_sorted_items = sort_items(items, reverse=True)
print(reverse_sorted_items)  # Output: [9, 6, 5, 5, 5, 4, 3, 3, 2, 1, 1]
```

### Testing

To run the tests, use the following command:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This package is licensed under the MIT License. See the LICENSE file for more details.
