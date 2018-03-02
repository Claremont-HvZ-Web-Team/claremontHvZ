from hashlib import sha1

from django.core.cache import cache
from django.utils.encoding import smart_str

def cached(key=None, timeout=300):
    """
    Cache the result of function call.

    Args:
        key: the key with which value will be saved. If key is None
            then it is calculated automatically
        timeout: number of seconds after which the cached value would be purged.
    """
    _key = key

    def func_wrapper(func):
        def args_wrapper(*args, **kwargs):
            # this is workaround of strange python behaviour
            key = _key
            if key is None:
                # Not sure that this will work correct in all cases
                key = sha1(str(func.__module__) + str(func.__name__) +\
                           smart_str(args) +\
                           smart_str(frozenset(kwargs.items()))).hexdigest()
            value = cache.get(key)
            if value:
                return value
            else:
                value = func(*args, **kwargs)
                cache.set(key, value)
                return value
        return args_wrapper
    return func_wrapper
