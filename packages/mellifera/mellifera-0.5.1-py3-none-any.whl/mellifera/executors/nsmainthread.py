try:
    from Foundation import NSThread
    from libdispatch import dispatch_async, dispatch_sync, dispatch_get_main_queue
except ModuleNotFoundError:
    raise ModuleNotFoundError("To use mellifera.orchestrators.nsmainthread you need to have pyobjc installed and run on macos")

import signal

from types import SimpleNamespace
import logging
import threading
import functools

from mellifera.orchestrator import Orchestrator
from mellifera.services.nsmainthread import NSMainThreadService
from mellifera.service import Service
from mellifera.executor import Executor

from mellifera.service import ServiceState
import trio

def threadsafe(f):
    @functools.wraps(f)
    def inner(self, *args, **kwargs):
        return self.run_threadsafe(f, self, *args, **kwargs)

    return inner

class NSMainThreadExecutor(Executor):
    requires_run = True

    def __init__(self, orchestrator) -> None:
        self.orchestrator = orchestrator
        self.service = None
        self.logger = logging.getLogger("mellifera.executors.NSMainThreadExecutor")
        self.thread = None
        self.trio_startup = threading.Event()
        self.trio_shutdown = threading.Event()
        self.executor_started = trio.Event()
        self.executor_shutdown = trio.Event()
        self._start_service = False

    def run_threadsafe(self, f, *args, **kwargs):
        self.logger.info(f"Running threadsafe: {f.__name__}")
        if self.thread is None or self.thread == threading.current_thread():
            r = f(*args, **kwargs)
            return None
        else:
            def closure():
                self.logger.debug(f'excecuted closure of {f.__name__} threadsafe via NSMainThreadExecutor')
                return f(*args, **kwargs)
            queue = dispatch_get_main_queue()
            r = dispatch_async(queue, closure)
            return None

    def run_exposed(self, f, service, *args, **kwargs):
        return self.run_threadsafe(f, service, *args, **kwargs)

    def start_service(self, service: Service) -> None:
        assert isinstance(service, NSMainThreadService)
        if self.service is None or self.service == service:
            self._start_service = True
        else:
            raise ValueError(f"Asked to start {service}, but registered {self.service}")

    @threadsafe
    def stop(self) -> None:
        self.service.stop()

    def wait_for_trio_startup(self) -> None:
        self.trio_startup.wait()

    def wait_for_trio_shutdown(self) -> None:
        self.trio_shutdown.wait()

    def set_started(self):
        async def closure():
            self.executor_started.set()
        self.orchestrator.run_async_function(closure)

    def set_shutdown(self):
        async def closure():
            self.executor_shutdown.set()
        self.orchestrator.run_async_function(closure)

    def run_sync(self) -> None:
        self.logger.info("run_sync")
        self.thread = threading.current_thread()
        self.logger.info("Waiting for trio to startup")
        self.wait_for_trio_startup()
        self.logger.info("Trio started up, starting service")
        try:
            self.logger.debug("Starting up")
            if self.service and self._start_service:
                self.logger.debug("Starting service")
                try:
                    try:
                        self.logger.debug("Constructing service")
                        self.service.construct()
                        self.logger.debug("Initializing service")
                        self.service.init_sync()
                        self.logger.debug("Running service")
                        self.service.run_sync()
                        self.logger.debug("Running service done, stopping")
                    except Exception as e:
                        self.logger.error("Encountered an error", exc_info=True)
                        raise e
                    finally:
                        self.logger.error("Stopping all")
                finally:
                    self.service.finalize_sync()
            else:
                if not self.service:
                    self.logger.debug("No service, aborting run")
                elif not self._start_service:
                    self.logger.debug("I have a service, but startup was never requested. Not running service")

        finally:
            self.running = False
            self.set_shutdown()
            self.wait_for_trio_shutdown()
            self.logger.info("run_sync ended")
