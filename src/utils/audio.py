from os.path import exists
from logging import getLogger
from pygame import mixer

log = getLogger(__name__)


class AudioManager:
    def __init__(self) -> None:
        self.mixer = mixer
        self.mixer.init()
        self.SongLoaded = False
        self.SongPlaying = False
        log.info("Initialized the audio mixer.")

    def play(self):
        if not self.SongLoaded:
            return log.warning("No song currently loaded!")
        elif self.SongPlaying:
            return log.warning("Song Already playing")
        self.SongPlaying = True
        self.mixer.music.play()

    def pause(self):
        if not self.SongLoaded:
            return log.warning("No song currently loaded!")
        elif not self.SongPlaying:
            return log.warning("No song currently !")

        self.SongPlaying = False
        self.mixer.music.play()

    def load(self, MusicFile: str):
        if not exists(MusicFile):
            return log.error(f"Music file {MusicFile} does not exist!")

        self.SongLoaded = True
        self.mixer.music.load(MusicFile)
