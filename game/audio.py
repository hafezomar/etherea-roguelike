"""Optional standard-library audio support for future Etherea assets."""

from __future__ import annotations

import os
import sys


class AudioManager:
    def __init__(self, asset_dir: str, enabled: bool = True) -> None:
        self.asset_dir = asset_dir
        self.enabled = enabled

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        return self.enabled

    def play(self, cue: str) -> bool:
        if not self.enabled or sys.platform != "win32":
            return False
        path = os.path.join(self.asset_dir, "audio", f"{cue}.wav")
        if not os.path.exists(path):
            return False
        try:
            import winsound

            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            return True
        except OSError:
            return False
