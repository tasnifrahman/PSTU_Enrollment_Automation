<<<<<<< HEAD
# Inside your app's templatetags/custom_filters.py
=======
>>>>>>> eb1577276d374ae26f979cb62368ddfc44600e2a
from django import template

register = template.Library()

@register.filter
<<<<<<< HEAD
def get_item(dictionary, key):
    return dictionary.get(key)
=======
def dict_key(d, key):
    if d is None:
        return None  # Handle NoneType dictionary
    return d.get(key, None)
>>>>>>> eb1577276d374ae26f979cb62368ddfc44600e2a
