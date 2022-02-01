import time
import sys
import signal
import os
import logging
import importlib
import threading
from queue import Queue, Empty
from watchgod import watch
from asyncio import Event

from .ui.main import DAW
from .audio import play

logger = logging.getLogger(__name__)


class ProjectRun(threading.Thread):
    def __init__(self, module):
        self.module = module
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()

    def run(self):
        module = importlib.reload(self.module)
        clip = module.main()
        play(clip, self.shutdown_flag)


class FileWatcher(threading.Thread):
    def __init__(self, path, events_queue, stop_event):
        self.path = path
        self.events_queue = events_queue
        self.stop_event = stop_event
        threading.Thread.__init__(self)

    def run(self):
        logger.info(f"Watching {self.path} for changes ...")
        for changes in watch(self.path, stop_event=self.stop_event):
            self.events_queue.put(changes)


class ProjectShutdown(Exception):
    pass


class ProjectReload(Exception):
    pass


class ProjectStop(Exception):
    pass


def shutdown_handler(signum, frame):
    logger.info(f"shutdown_handler: Caught signal {signal.Signals(signum).name}")
    raise ProjectShutdown


def stop_handler(signum, frame):
    logger.info(f"stop_handler: Caught signal {signal.Signals(signum).name}")
    raise ProjectStop


def reload_handler(signum, frame):
    logger.info(f"reload_handler: Caught signal {signal.Signals(signum).name}")
    raise ProjectReload


def main():
    try:
        project = sys.argv[1]
    except IndexError:
        logger.error("Missing required argument: PROJECT")
        return 1

    module = importlib.import_module(f"projects.{project}")

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGUSR1, stop_handler)
    signal.signal(signal.SIGUSR2, reload_handler)

    thread = ProjectRun(module)
    thread.start()

    live_reload = os.getenv("LIVE_RELOAD", "true").lower() == "true"
    if live_reload:
        file_change_queue = Queue()
        file_change_stop_event = Event()
        file_watcher = FileWatcher(
            os.path.join("projects", f"{project}.py"),
            file_change_queue,
            file_change_stop_event,
        )
        file_watcher.start()

    while True:
        try:
            time.sleep(0.5)
            if live_reload:
                try:
                    file_change_queue.get(timeout=0.5)
                    raise ProjectReload
                except Empty:
                    pass
                else:
                    raise ProjectReload
        except ProjectStop:
            thread.shutdown_flag.set()
            thread.join()
            logger.warning(f"Stopped project {project} (waiting for reload) ... ")
        except ProjectShutdown:
            logger.warning("Shutting down ... ")
            thread.shutdown_flag.set()
            thread.join()
            break
        except ProjectReload:
            thread.shutdown_flag.set()
            thread.join()
            thread = ProjectRun(module)
            thread.start()
            logger.warning(f"Reloaded project {project}")

    if live_reload:
        file_change_stop_event.set()
        file_watcher.join()


if __name__ == "__main__":
    main()
