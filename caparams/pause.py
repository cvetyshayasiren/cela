from config import Config
class Pause:
    
    def __init__(self, paused: bool = False, message: str | None = None):
        self.paused: bool = paused
        self.pause_string: str = self._make_pause_string(message)

    def pause(self, message: str | None = None): 
        self.pause_toogle(True)
        self._set_pause_string(message)
        
    def unpause(self): 
        self.pause_toogle(False)
        self.pause_string = ""
        
    def pause_toogle(self, value: bool | None = None):
        if value is not None:
            self.paused = value
        else:
            self.paused = not self.paused

    def is_paused(self) -> bool: return self.paused
    def is_unpaused(self) -> bool: return not self.paused

    def _set_pause_string(self, message: str | None):
        self.pause_string = self._make_pause_string(message)
    
    def _make_pause_string(self, message: str | None) -> str: 
        if not self.paused: return ""
        default = Config.DEFAULT_PAUSE_STRING
        if message is not None:
            return f"[{message}]{default}"
        return default