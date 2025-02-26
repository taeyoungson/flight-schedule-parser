from . import client


def report_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            client.send_to_me(f"Error occurred in {func.__name__}: {e}")
            raise e

    return wrapper
