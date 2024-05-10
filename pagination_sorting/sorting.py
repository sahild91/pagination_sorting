from typing import List, Any, Callable

def sort_items(items: List[Any], key: Callable[[Any], Any] = None, reverse: bool = False) -> List[Any]:
    return sorted(items, key=key, reverse=reverse)