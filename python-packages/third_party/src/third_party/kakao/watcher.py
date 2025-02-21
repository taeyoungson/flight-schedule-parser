from . import client


def report(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            client.send_to_me(f"{func.__module__}.{func.__name__} is done.")
            return result
        except Exception as e:
            client.send_to_me(f"Error occurred in {func.__name__}: {e}")
            raise e

    return wrapper
