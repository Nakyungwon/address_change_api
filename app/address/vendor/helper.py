from functools import wraps
import time


def delay(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        time.sleep(0.3)
        print('실행 완료! {0:.2f}초 걸림'.format(time.time() - start))
        return ret
    return wrapper
