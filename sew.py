"""
This module contains various decorators to help with common tasks involving
the Python `threading` module.

- `thread`: Call a function in a separate thread.

- `thread_join`: Call a function in a separate thread and join the thread.

- `thread_daemon`: Call a function in a separate thread and return
its return value.

- `delay`: Delay before calling a function.

- `delay_join`: Delay before calling a function and join the thread.

- `delay_daemon`: Delay before calling a function in a daemon thread.

- `delay_with_return_value`: Delay before calling a function and return
its return value.
"""

import threading

__all__ = [
    "thread",
    "thread_join",
    "thread_daemon",
    "thread_with_return_value",
    "delay",
    "delay_join",
    "delay_daemon",
    "delay_with_return_value"
]


class _FunctionThreadWithReturnValue(threading.Thread):
    """Calls a function and saves the return value."""

    def __init__(self, function, args, kwargs):
        super().__init__()
        self._call = (function, args, kwargs)
        self.return_value = None

    def run(self):
        function, args, kwargs = self._call
        self.return_value = function(*args, **kwargs)


class _DelayedFunctionWithReturnValue(threading.Timer):
    """Calls a function after a certain delay and saves the return value."""

    def __init__(self, seconds, function, args, kwargs):
        super().__init__(seconds, lambda: None)
        # Gives us a reliable timer while still allowing us to store the
        # return value
        self._call = (function, args, kwargs)
        self.return_value = None

    def run(self):
        super().run()
        function, args, kwargs = self._call
        self.return_value = function(*args, **kwargs)


def thread(function):
    """Run `function` in a separate thread."""
    def call(*args, **kwargs):
        thread = threading.Thread(
            target=function,
            args=args,
            kwargs=kwargs
        )
        thread.start()
    return call


def thread_join(function):
    """Run `function` in a separate thread and join the thread."""
    def call(*args, **kwargs):
        thread = threading.Thread(
            target=function,
            args=args,
            kwargs=kwargs
        )
        thread.start()
        thread.join()
    return call


def thread_daemon(function):
    """Run `function` in a separate daemon thread."""
    def call(*args, **kwargs):
        thread = threading.Thread(
            target=function,
            args=args,
            kwargs=kwargs
        )
        thread.daemon = True
        thread.start()
    return call


def thread_with_return_value(function):
    """Run `function` in a separate thread and return the return value.
    The function call will block due to the use of `join`.
    """
    def call(*args, **kwargs):
        thread = _FunctionThreadWithReturnValue(
            function=function,
            args=args,
            kwargs=kwargs
        )
        thread.start()
        thread.join()
        # Wait for the function to fall through to avoid
        # returning `None`
    return call


def delay(seconds):
    """Wait `seconds` seconds before calling `function`."""
    def wrap(function):
        def call(*args, **kwargs):
            function_timer = threading.Timer(
                seconds,
                function=function,
                args=args,
                kwargs=kwargs
            )
            function_timer.start()
        return call
    return wrap


def delay_join(seconds):
    """Wait `seconds` seconds before calling `function` and join the thread."""
    def wrap(function):
        def call(*args, **kwargs):
            function_timer = threading.Timer(
                seconds,
                function=function,
                args=args,
                kwargs=kwargs
            )
            function_timer.start()
            function_timer.join()
        return call
    return wrap


def delay_daemon(seconds):
    """Wait `seconds` seconds before calling `function` in a daemon thread."""
    def wrap(function):
        def call(*args, **kwargs):
            function_timer = threading.Timer(
                seconds,
                function=function,
                args=args,
                kwargs=kwargs
            )
            function_timer.daemon = True
            function_timer.start()
        return call
    return wrap


def delay_with_return_value(seconds):
    """Wait `seconds` seconds before returning the call to `function`."""
    def wrap(function):
        def call(*args, **kwargs):
            function_timer = _DelayedFunctionWithReturnValue(
                seconds=seconds,
                function=function,
                args=args,
                kwargs=kwargs
            )
            function_timer.start()
            function_timer.join()
            return function_timer.return_value
        return call
    return wrap
