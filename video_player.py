import pandas as pd
import vlc 

class VideoPlayer:
    def __init__(self, path: str):
    
        self.instance = vlc.Instance()
        self.player = vlc.MediaPlayer(path)
        self.vid_length = self.player.get_length()
        if self.vid_length == -1:
            raise ValueError("Could not retrieve video length. Ensure the file path is correct.")
        

    def play(self):
        if not self.player.is_playing():
            self.player.play()
        else:
            print("Video is already playing.")
    
    def pause(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            print("Video is not playing.")
    
    def stop(self):
        if self.player.is_playing():
            self.player.stop()
        else:
            print("Video is not playing.")

    def get_time(self):
        return self.player.get_time() / 1000  # Convert milliseconds to seconds
    
    def set_time(self, seconds: float):
        self.player.set_time(int(seconds * 1000))
    


