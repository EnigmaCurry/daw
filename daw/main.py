import time
import sys
import signal
import os
import logging
import importlib
import threading
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
    logger.info(f"reload_handler: Caught signal {signal.Signals(signum)}")
    raise ProjectStop


def reload_handler(signum, frame):
    logger.info(f"reload_handler: Caught signal {signal.Signals(signum)}")
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
    while True:
        try:
            time.sleep(0.5)
            # if not thread.is_alive():
            #     break
        except ProjectStop:
            thread.shutdown_flag.set()
            thread.join()
        except ProjectShutdown:
            thread.shutdown_flag.set()
            thread.join()
            break
        except ProjectReload:
            thread.shutdown_flag.set()
            thread.join()
            thread = ProjectRun(module)
            thread.start()


if __name__ == "__main__":
    main()
