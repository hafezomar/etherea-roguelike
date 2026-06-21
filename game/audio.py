"""Optional Windows audio support for Etherea assets."""

from __future__ import annotations

import os
import sys


class AudioManager:
    def __init__(self, asset_dir: str, enabled: bool = True) -> None:
        self.asset_dir = asset_dir
        self.enabled = enabled

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop()
        return self.enabled

    def _cue_path(self, cue: str) -> str | None:
        audio_dir = os.path.join(self.asset_dir, "audio")
        for extension in (".mp3", ".wav"):
            path = os.path.join(audio_dir, f"{cue}{extension}")
            if os.path.exists(path):
                return path
        return None

    def stop(self) -> None:
        if sys.platform != "win32":
            return
        try:
            import winsound

            winsound.PlaySound(None, 0)
        except OSError:
            pass
        try:
            import ctypes

            ctypes.windll.winmm.mciSendStringW("stop etherea_music", None, 0, None)
            ctypes.windll.winmm.mciSendStringW("close etherea_music", None, 0, None)
        except OSError:
            pass

    def play(self, cue: str) -> bool:
        if not self.enabled or sys.platform != "win32":
            return False
        path = self._cue_path(cue)
        if not path:
            return False
        self.stop()
        if path.lower().endswith(".mp3"):
            try:
                import ctypes

                open_result = ctypes.windll.winmm.mciSendStringW(
                    f'open "{path}" type mpegvideo alias etherea_music', None, 0, None
                )
                play_result = ctypes.windll.winmm.mciSendStringW(
                    "play etherea_music repeat", None, 0, None
                )
                return open_result == 0 and play_result == 0
            except OSError:
                return False
        try:
            import winsound

            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            return True
        except OSError:
            return False
