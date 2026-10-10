"""Small shared helpers."""


def clamp(value, low, high):
    try:
        value = int(value)
    except (TypeError, ValueError):
        value = low
    return max(low, min(value, high))


def first_present(mapping, keys, default=None):
    for key in keys:
        if mapping.get(key):
            return mapping[key]
    return default
