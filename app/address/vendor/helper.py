from functools import wraps
import time


def delay(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        time.sleep(0.4)
        print(
            '{0}실행 완료! {1:.2f}초 걸림'.format(
                func.__name__,
                time.time() -
                start))
        return ret
    return wrapper
