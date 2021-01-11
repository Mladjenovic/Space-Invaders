import os
from pathlib import Path


def get_image_path(image_path: str) -> str:

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = image_path
    abs_file_path = Path(os.path.join(script_dir, rel_path)).resolve()
    return str(abs_file_path)
