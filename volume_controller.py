from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys 

class VolumeController:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        vol_range = self.volume.GetVolumeRange()
        self.min_vol = vol_range[0]
        self.max_vol = vol_range[1]

    def set_volume_by_distance(self, distance, min_distance=20, max_distance=200):
        # Clamp the distance between min and max
        distance = max(min_distance, min(max_distance, distance))
        # Map distance to volume level
        volume = self.min_vol + (self.max_vol - self.min_vol) * ((distance - min_distance) / (max_distance - min_distance))
        self.volume.SetMasterVolumeLevel(volume, None)
        return volume

    def get_current_volume(self):
        # Read current system volume level
        return self.volume.GetMasterVolumeLevel()

    def get_volume_percent(self):
        # Calculate volume percentage based on system volume level
        current_vol = self.get_current_volume()
        percent = int((current_vol - self.min_vol) * 100 / (self.max_vol - self.min_vol))
        # Clamp percent between 0 and 100
        return max(0, min(100, percent))
    
    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()
        sys.exit(0)

