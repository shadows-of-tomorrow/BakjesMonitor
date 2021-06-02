import os
import vlc


class Alarm:

    def __init__(self):
        self.media_player = self._get_media_player()

    def turn_on(self):
        self.media_player.play()

    def turn_off(self):
        self.media_player.stop()

    def _get_media_player(self):
        audio_path = self._get_audio_path()
        return vlc.MediaPlayer(audio_path+'emergency_alarm_003.mpx')

    def _get_audio_path(self):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio')