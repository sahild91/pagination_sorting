from typing import List, Any, Optional, Callable
from math import ceil

class InvalidPageError(Exception):
    pass

class Paginator:
    """
    A class for paginating and sorting a list of items.

    Args:
        items (List[Any]): The list of items to paginate.
        items_per_page (int): The number of items per page.
        orphans (int, optional): The minimum number of items allowed on the last page. Defaults to 0.
        allow_empty_first_page (bool, optional): Whether to allow the first page to be empty. Defaults to True.
        pagination_style (str, optional): The pagination style. Can be 'paginate' (default), 'infinite_scroll', or 'load_more'.

    Raises:
        ValueError: If `items_per_page` is not a positive integer or `orphans` is a negative integer.
        InvalidPageError: If `allow_empty_first_page` is False and the list of items is empty.

    """
    def __init__(self, items: List[Any], items_per_page: int, orphans: int = 0, allow_empty_first_page: bool = True, pagination_style: str = 'paginate'):
        if items_per_page <= 0:
            raise ValueError("items_per_page must be a positive integer.")
        if orphans < 0:
            raise ValueError("orphans must be a non-negative integer.")

        self.items = items
        self.items_per_page = items_per_page
        self.orphans = orphans
        self.allow_empty_first_page = allow_empty_first_page
        self.pagination_style = pagination_style
        self.total_items = len(items)
        self.total_pages = ceil((self.total_items - self.orphans) / self.items_per_page)

        if not self.allow_empty_first_page and self.total_items == 0:
            raise InvalidPageError("Cannot paginate an empty list when allow_empty_first_page is False.")

    def get_page(self, page_number: int) -> List[Any]:
        """
        Get the items for a specific page number.

        Args:
            page_number (int): The page number.

        Returns:
            List[Any]: The items for the specified page.

        Raises:
            InvalidPageError: If the page number is invalid.

        """
        if page_number < 1:
            raise InvalidPageError(f"Invalid page number: {page_number}. Page number should be >= 1.")
        if page_number > self.total_pages:
            if page_number == 1 and self.allow_empty_first_page:
                return []
            raise InvalidPageError(f"Invalid page number: {page_number}. Page number exceeds the total number of pages.")

        start_index = (page_number - 1) * self.items_per_page
        end_index = min(start_index + self.items_per_page, self.total_items)

        return self.items[start_index:end_index]

    def has_previous(self, page_number: int) -> bool:
        """
        Check if there is a previous page.

        Args:
            page_number (int): The current page number.

        Returns:
            bool: True if there is a previous page, False otherwise.

        """
        return page_number > 1

    def has_next(self, page_number: int) -> bool:
        """
        Check if there is a next page.

        Args:
            page_number (int): The current page number.

        Returns:
            bool: True if there is a next page, False otherwise.

        """
        return page_number < self.total_pages

    def get_page_range(self, page_number: int, num_pages: int = 5, left_edge: int = 2, right_edge: int = 2) -> List[int]:
        """
        Get the range of page numbers to display in the pagination controls.

        Args:
            page_number (int): The current page number.
            num_pages (int, optional): The maximum number of pages to display. Defaults to 5.
            left_edge (int, optional): The number of pages to display on the left edge. Defaults to 2.
            right_edge (int, optional): The number of pages to display on the right edge. Defaults to 2.

        Returns:
            List[int]: The range of page numbers to display.

        Raises:
            InvalidPageError: If the page number is invalid.

        """
        if page_number < 1 or page_number > self.total_pages:
            raise InvalidPageError(f"Invalid page number: {page_number}. Page number should be between 1 and {self.total_pages}.")

        left_range = max(1, page_number - left_edge)
        right_range = min(page_number + right_edge, self.total_pages)

        if left_range > 1:
            left_range = [1, '...'] + list(range(max(1, page_number - num_pages // 2), page_number))
        else:
            left_range = list(range(1, page_number))

        if right_range < self.total_pages:
            right_range = list(range(page_number, min(page_number + num_pages // 2, self.total_pages) + 1)) + ['...', self.total_pages]
        else:
            right_range = list(range(page_number, self.total_pages + 1))

        return left_range + right_range

    def get_page_info(self, page_number: int) -> dict:
        """
        Get the pagination information for a specific page.

        Args:
            page_number (int): The page number.

        Returns:
            dict: A dictionary containing pagination information.

        """
        items = self.get_page(page_number)
        return {
            'current_page': page_number,
            'has_previous': self.has_previous(page_number),
            'has_next': self.has_next(page_number),
            'total_pages': self.total_pages,
            'total_items': self.total_items,
            'items_per_page': self.items_per_page,
            'items': items,
            'start_index': (page_number - 1) * self.items_per_page + 1,
            'end_index': min(page_number * self.items_per_page, self.total_items),
            'previous_page_url': self.get_page_url(page_number - 1) if self.has_previous(page_number) else None,
            'next_page_url': self.get_page_url(page_number + 1) if self.has_next(page_number) else None,
        }

    def get_paginated_items(self, page_number: int) -> Optional[List[Any]]:
        """
        Get the paginated items for a specific page number.

        Args:
            page_number (int): The page number.

        Returns:
            Optional[List[Any]]: The paginated items, or None if the page number is invalid.

        """
        try:
            items = self.get_page(page_number)
            return items
        except InvalidPageError:
            return None
        
    def get_page_url(self, page_number: int, base_url: str = '', query_param: str = 'page') -> str:
        """
        Generate the URL for a specific page number.

        Args:
            page_number (int): The page number.
            base_url (str, optional): The base URL. Defaults to an empty string.
            query_param (str, optional): The query parameter name for the page number. Defaults to 'page'.

        Returns:
            str: The generated URL for the page.

        Raises:
            InvalidPageError: If the page number is invalid.

        """
        if page_number < 1 or page_number > self.total_pages:
            raise InvalidPageError(f"Invalid page number: {page_number}. Page number should be between 1 and {self.total_pages}.")

        return f"{base_url}?{query_param}={page_number}"

    def set_custom_template(self, template: str) -> None:
        """
        Set a custom template for rendering the pagination controls.

        Args:
            template (str): The custom template string.

        """
        self.custom_template = template

    def render_pagination(self, page_number: int, base_url: str = '', query_param: str = 'page') -> str:
        """
        Render the pagination controls as HTML.

        Args:
            page_number (int): The current page number.
            base_url (str, optional): The base URL for the page links. Defaults to an empty string.
            query_param (str, optional): The query parameter name for the page number. Defaults to 'page'.

        Returns:
            str: The rendered HTML pagination controls.

        """
        page_info = self.get_page_info(page_number)
        page_range = self.get_page_range(page_number)

        if hasattr(self, 'custom_template'):
            return self.custom_template.format(page_info=page_info, page_range=page_range, base_url=base_url, query_param=query_param)
        else:
            # Default template implementation
            pagination_html = '<ul class="pagination">'
            if page_info['has_previous']:
                pagination_html += f'<li><a href="{page_info["previous_page_url"]}">&laquo; Previous</a></li>'
            for page in page_range:
                if page == '...':
                    pagination_html += '<li><span>...</span></li>'
                elif page == page_number:
                    pagination_html += f'<li class="active"><span>{page}</span></li>'
                else:
                    pagination_html += f'<li><a href="{self.get_page_url(page, base_url, query_param)}">{page}</a></li>'
            if page_info['has_next']:
                pagination_html += f'<li><a href="{page_info["next_page_url"]}">Next &raquo;</a></li>'
            pagination_html += '</ul>'
            return pagination_html

    def paginate(self, page_number: int, sort_key: Optional[Callable[[Any], Any]] = None, reverse: bool = False) -> dict:
        """
        Paginate and sort the items based on the specified page number and sorting criteria.

        Args:
            page_number (int): The page number.
            sort_key (Optional[Callable[[Any], Any]], optional): The key function for sorting the items. Defaults to None.
            reverse (bool, optional): Whether to sort the items in reverse order. Defaults to False.

        Returns:
            dict: A dictionary containing the paginated items and pagination information.

        """
        if sort_key:
            self.items.sort(key=sort_key, reverse=reverse)

        page_info = self.get_page_info(page_number)
        page_info['items'] = self.get_paginated_items(page_number)

        return page_info