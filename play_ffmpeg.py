import subprocess


class PlayFFMPEG:
    """
    Bare bones implementation of running FFMPEG subprocess
    """

    sound_enabled = False

    def __init__(self):
        """
        Will ensure that FFMPEG is available on your system.
        """
        try:
            subprocess.run(
                ["ffplay", "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            print("FFMPEG is installed!")
            self.sound_enabled = True
        except FileNotFoundError:
            print("FFMPEG is not installed! Sound will not be available.")

    def play_sound(self, sound: str, blocking=False):
        """
        Use FFMPEG in a subprocess to play a sound. By default blocking is
        set to False which means this operation happens asynchronously.
        """
        if not self.sound_enabled:
            print("FFMPEG is unavailable, please install it.")
            return None
        if blocking:
            return subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", sound]
            )
        return subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", sound]
        )


if __name__ == "__main__":
    ffmpeg = PlayFFMPEG()
    ffmpeg.play_sound("alert_sound.wav", blocking=True)
