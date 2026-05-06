from pathlib import Path
import pickle
from datetime import datetime

class PickleSnapshots:
    def save_snapshot(self, file_path):
        path = Path(file_path)

        with path.open("wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_snapshot(cls, file_path):
        path = Path(file_path)

        with path.open("rb") as f:
            return pickle.load(f)

    def log_history(self, key):
       
        path = Path("history.log")

        if path.exists() and path.stat().st_size > 1024:
            old_path = Path("history.log.old")

            if old_path.exists():
                old_path.unlink()

            path.rename(old_path)
 
        if isinstance(key, (int, float)):
            display = datetime.fromtimestamp(key).strftime("%Y-%m-%d %H:%M:%S")
        else:
            display = key

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("history.log", "a", encoding="utf-8") as f:
            f.write(f"[{now}] Added element: Key=[{display}]\n")