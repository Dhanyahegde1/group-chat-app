# ---------------------------------------------------
# Aspect Utilities
# ---------------------------------------------------
# This file implements simple Aspect-Oriented helpers.
# It can be used for cross-cutting concerns like logging,
# validation, or monitoring across multiple APIs.

import functools


# ---------------------------------------------------
# Logging Aspect
# ---------------------------------------------------
# Logs whenever an API function is called
def log_api_call(func):
    """
    Decorator used to log API calls.
    Can be applied to any Django view function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        print(f"[ASPECT] API called: {func.__name__}")

        result = func(*args, **kwargs)

        print(f"[ASPECT] API completed: {func.__name__}")

        return result

    return wrapper