import asyncio
from concurrent.futures import ThreadPoolExecutor
import inspect
import threading
import traceback

from adam.utils import log2, log_timing

class AsyncExecutor:
    # some lib does not handle asyncio loop properly, as sync exec submit does not work, use another async loop

    lock = threading.Lock()
    in_queue = set()

    loop: asyncio.AbstractEventLoop = None
    async_exec: ThreadPoolExecutor = None

    def preload(action: callable, log_key: str = None):
        with AsyncExecutor.lock:
            if not AsyncExecutor.loop:
                AsyncExecutor.loop = asyncio.new_event_loop()
                AsyncExecutor.async_exec = ThreadPoolExecutor(max_workers=6, thread_name_prefix='async')
                AsyncExecutor.loop.set_default_executor(AsyncExecutor.async_exec)

            async def a():
                try:
                    arg_needed = len(action.__code__.co_varnames)

                    if log_key:
                        with log_timing(log_key):
                            r = action(None) if arg_needed else action()
                    else:
                        r = action(None) if arg_needed else action()
                    if inspect.isawaitable(r):
                        await r

                    AsyncExecutor.in_queue.remove(log_key)
                except Exception as e:
                    log2('preloading error', e, inspect.getsourcelines(action)[0][0])
                    traceback.print_exc()

            if log_key not in AsyncExecutor.in_queue:
                AsyncExecutor.in_queue.add(log_key)
                AsyncExecutor.async_exec.submit(lambda: AsyncExecutor.loop.run_until_complete(a()))