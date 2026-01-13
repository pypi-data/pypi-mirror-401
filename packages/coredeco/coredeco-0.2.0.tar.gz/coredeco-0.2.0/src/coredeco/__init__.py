import sys
import time
import typing
import asyncio
import functools


# ==-----------------------------------------------------------------------------== #
# Universal functions decorators                                                    #
# ==-----------------------------------------------------------------------------== #
def retry(function_or_coroutine: typing.Callable | None = None, *, retries: int = 1, retry_delay: int | float = 0.0):
    """Decorator, allows to retry function call if exception raises for several times."""

    # If retry times is invalid value
    if retries <= 0:
        raise Exception("retries argument have to be greated than `0`")

    # If retry interval is invalid value
    if retry_delay < 0:
        raise Exception("delay argument have to be greater or equals `0`")

    # Decorator outer wrapper
    def decorator(function: typing.Callable):

        # Wrapper for async version of function
        @functools.wraps(function)
        async def async_wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:

            # Last exception raised on coroutine call
            last_exception = None

            # Trying to call and return result on coroutine while succeed exceeded `retries` + 1 times
            for index in range(retries + 1):

                try:
                    return await function(*args, **kwargs)

                except BaseException as error:

                    # Saving last exception raised on coroutine call
                    last_exception = error

                # If there a more extra retry call coroutine
                if index != retries:
                    await asyncio.sleep(retry_delay)

            # Raising last saved exception
            raise last_exception

        # Wrapper for sync version of function
        @functools.wraps(function)
        def sync_wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:

            # Last exception raised on coroutine call
            last_exception = None

            # Trying to call and return result on function while succeed exceeded `times` + 1 times
            for index in range(retries + 1):

                try:
                    return function(*args, **kwargs)

                except BaseException as error:

                    # Saving last exception raised on coroutine call
                    last_exception = error

                # If there a more extra retry call coroutine
                if index != retries:
                    time.sleep(retry_delay)

            # Raising last saved exception
            raise last_exception

        # Returning async decorator wrapper if function is coroutine else sync decorator wrapper
        return async_wrapper if asyncio.iscoroutinefunction(function) else sync_wrapper

    # If function decorated with arguments
    if function_or_coroutine is None:
        return decorator

    # If function decorated without arguments
    return decorator(function_or_coroutine)


# ==-----------------------------------------------------------------------------== #
# Async functions decorators                                                        #
# ==-----------------------------------------------------------------------------== #
def task(coroutine: typing.Callable | None = None, *, name: str | None = None):
    """Decorator, wraps coroutine to make it's able to run as background non-blocking task."""

    # Decorator outer wrapper
    def decorator(function: typing.Callable):

        # If coroutine is not awaitable function
        if not asyncio.iscoroutinefunction(coroutine):
            raise Exception("`%s` decorator can only be applied to coroutine function" % sys._getframe().f_back.f_code.co_name)

        @functools.wraps(function)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> asyncio.Task:

            # Wraps coroutine as a task and return it's object
            return asyncio.create_task(function(*args, **kwargs), name=name)

        # Returning innter wrapper
        return wrapper

    # If function decorated with arguments
    if coroutine is None:
        return decorator

    # If function decorated without arguments
    return decorator(coroutine)
