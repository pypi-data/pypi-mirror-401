from typing import Callable, Optional, Any, Dict
import uuid
import functools
import asyncio

from .sdk_client import SDKClient
from .task_context import TaskContext
from .enums import TaskTypes
from . import context


class NoActiveRunError(Exception):
    pass

''' resolves sdk client (from context.current_run if not given) and creates a taskcontext
enters it before runnnig the wrapped function, maybe injects the taskcontext into the wrapped function (optinal)'''
def sdk_task(task_step_id: Optional[str] = None,
             type: TaskTypes = TaskTypes.GENERIC,
             metadata: Optional[Dict[Any, Any]] = None,
             client: Optional[SDKClient] = None,
             inject_context: bool = False):
    """Decorator to label  function
    params:
        task_step_id: optional explicit id if none auto-generated as module.func
        type: TaskTypes enum
        metadata: optional metadata dict
        client: optional SDKClient; if not given resolved from context.current_run
        inject_context: if true the decorator will pass the TaskContext to the wrapped function as a keyword-only argument _task_context (this is for firect context access)
    """
    metadata = metadata or {}

    '''this supports sync and async functions'''
    def decorator(func: Callable):
        is_coro = asyncio.iscoroutinefunction(func)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            ''' get resolved client (either going to be client arg or from context.current_run)'''
            nonlocal client
            resolved_client = client
            if not resolved_client:
                curr_run = context.current_run.get()
                if not curr_run:
                    raise NoActiveRunError("call Workflow.start_run() before using sdk_task.")
                resolved_client = curr_run.client

            resolved_task_id = task_step_id or uuid.uuid4()
            ctx = TaskContext(
                task_step_id=resolved_task_id,
                client=resolved_client,
                func_name= f"{func.__module__}.{func.__qualname__}",
                type=type,
                metadata=metadata)
            ctx.__enter__()
            # call wrapped function
            try:
                if inject_context:
                    result = func(*args, _task_context=ctx, **kwargs)
                else:
                    result = func(*args, **kwargs)
            except Exception:
                import sys
                exc_info = sys.exc_info()
                ctx.__exit__(exc_info[0], exc_info[1], exc_info[2])
                raise
            else:
                ctx.__exit__(None, None, None)
                return result

        # same as sync wrapper but await wrapped coroutine call
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            nonlocal client
            resolved_client = client
            if not resolved_client:
                curr_run = context.current_run.get()
                if not curr_run:
                    raise NoActiveRunError("call Workflow.start_run() before using sdk_task.")
                resolved_client = curr_run.client

            resolved_task_id = task_step_id or uuid.uuid4()
            ctx = TaskContext(
                task_step_id=resolved_task_id,
                client=resolved_client,
                func_name= f"{func.__module__}.{func.__qualname__}",
                type=type,
                metadata=metadata)
            ctx.__enter__()
            try:
                if inject_context:
                    result = await func(*args, _task_context=ctx, **kwargs)
                else:
                    result = await func(*args, **kwargs)
            except Exception:
                import sys
                exc_info = sys.exc_info()
                ctx.__exit__(exc_info[0], exc_info[1], exc_info[2])
                raise
            else:
                ctx.__exit__(None, None, None)
                return result

        sync_wrapper.__globals__.update(func.__globals__)
        async_wrapper.__globals__.update(func.__globals__)

        return async_wrapper if is_coro else sync_wrapper

    return decorator
