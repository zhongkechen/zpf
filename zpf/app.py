from functools import partial, wraps
from inspect import iscoroutinefunction

from celery import Celery

from .pool import SimpleEventPool


def zpf_task(func=None, *, name=None, queue="general", **kwargs):
    if func is None:
        return partial(zpf_task, name=name, queue=queue, **kwargs)

    if iscoroutinefunction(func):
        async_func = func

        @wraps(async_func)
        def func(*args, **kwargs2):
            return SimpleEventPool.run(async_func(*args, **kwargs2))

    task_name = name or func.__name__
    return app.task(name=task_name, queue=queue, **kwargs)(func)


app = Celery()

