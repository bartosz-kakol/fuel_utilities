from os import PathLike
from pathlib import Path
import pickle

from PIL import Image


def compile_assets(destination_file_path: str | PathLike[str] | Path):
    this_script_dir = Path(__file__).resolve().parent
    assets_dir = this_script_dir / "files"
    destination_file_path = Path(destination_file_path)

    if not destination_file_path.is_absolute():
        destination_dir = this_script_dir.parent
        destination_file_path = destination_dir / destination_file_path

    bitmaps = {}

    # Wypisujemy wynik
    for bmp_file in assets_dir.rglob("*.bmp"):
        bmp_file_relative_path = str(bmp_file.relative_to(assets_dir))
        print(f"Compiling '{bmp_file_relative_path}'...")

        img = Image.open(bmp_file).convert("1")
        w, h = img.size
        bitmap = [(w, h)]

        for y in range(h):
            for x in range(w):
                # noinspection PyTypeChecker
                pixel: int = img.getpixel((x, y))

                if pixel == 255:
                    bitmap.append((x, y))

        bitmaps[bmp_file_relative_path] = bitmap

    print("Saving...")

    with open(destination_file_path, "wb") as f:
        # noinspection PyTypeChecker
        pickle.dump(bitmaps, f)

    print(f"✅ Compiled to:\n{destination_file_path}")


if __name__ == "__main__":
    compile_assets("compiled.assets")
