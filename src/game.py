from psutil import Process, AccessDenied

from definitions import BlizzardGame, ClassicGame
from pathfinder import PathFinder
from consts import SYSTEM
import time

pathfinder = PathFinder(SYSTEM)


class InstalledGame(object):
    def __init__(self, info: BlizzardGame, uninstall_tag: str, version: str, last_played: str, install_path: str, playable: bool):
        self.info = info
        self.uninstall_tag = uninstall_tag
        self.version = version
        self.last_played = last_played
        self.install_path = install_path
        self.playable = playable

        self.execs = pathfinder.find_executables(self.install_path)
        self._processes = set()

    @property
    def local_game_args(self):
        return (self.info.blizzard_id, self.is_running)

    def add_process(self, process: Process):
        try:
            if process.exe() in self.execs:
                self._processes.add(process)
            else:
                raise ValueError(f"The process exe [{process.exe()}] doesn't match with the game execs: {self.execs}")
        except AccessDenied:
            if isinstance(self.info, ClassicGame):
                if self.info.exe in process.name():
                    self._processes.add(process)
                else:
                    raise ValueError(
                        f"The process name [{process.name()}] doesn't match with the game exe: {self.info.exe}")

    def is_running(self):
        for process in self._processes:
            if process.is_running():
                return True
        else:
            self._processes = set()
            return False

    def wait_until_game_stops(self):
        while self.is_running():
            time.sleep(0.5)
