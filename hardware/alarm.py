import os
import vlc


class Alarm:

    def __init__(self):
        self.media_player = vlc.MediaPlayer('./audio/emergency_alarm_003.mp3')

    def turn_on(self):
        self.media_player.play()

    def turn_off(self):
        self.media_player.stop()