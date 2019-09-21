"""Game audio"""
from pygame import mixer


class SoundManager:
    """Class to handle initialization and playback of audio."""
    def __init__(self):
        mixer.init()
        self.shoot = mixer.Sound("sounds/shoot.wav")

    def play_shoot(self):
        """Play a shooty sound."""
        self.shoot.play()
