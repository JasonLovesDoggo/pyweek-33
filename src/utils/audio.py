import logging
from os.path import exists
from logging import getLogger
from pygame import mixer

log = getLogger(__name__)


class AudioManager:
    def __init__(self) -> None:
        self.mixer = mixer
        self.mixer.init()
        self.SongLoaded = False
        log.info("Initialized the audio mixer.")

    def play(self):
        if not self.SongLoaded:
            log.warning(f'No song currently loaded!')

        self.mixer.music.play()

    def load(self, MusicFile: str):
        if not exists(MusicFile):
            log.error(f'Music file {MusicFile} does not exist!')

        self.SongLoaded = True
        self.mixer.music.load(MusicFile)

