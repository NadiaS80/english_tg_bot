from functools import wraps
from datetime import datetime

# path = r'decorator/logs/log_number.log'
def logger(path):
    """
    Parameterized decorator that logs function call details to a file.
    The log file path is passed as a decorator argument.
    """

    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result_old_func = old_function(*args, **kwargs)
            with open(path, 'a') as f:
                f.write(f'Date of calling func: {datetime.now().date()}\n')
                f.write(f'Time of calling func: {str(datetime.now().time())[:8]}\n')
                f.write(f'Name of func: {old_function.__name__}\n')
                f.write(f'Args of func: {args=}, {kwargs=}\n')
                f.write(f'Return result of func: {result_old_func}\n')
                f.write('-' * 30)
                f.write('\n')
            return result_old_func
        return new_function

    return __logger