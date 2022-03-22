from logging import getLogger
from pygame import mixer

log = getLogger(__name__)


class AudioManager:
    def __init__(self) -> None:
        self.mixer = mixer
        self.mixer.init()
        log.info("Initialized the audio mixer.")