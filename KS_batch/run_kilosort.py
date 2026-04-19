from pathlib import Path
from kilosort import run_kilosort


def run_one_recording(dat_path: Path, output_dir: Path, probe_path: Path, fs: int = 25000):

    output_dir.mkdir(parents=True, exist_ok=True)

    settings = {
        "filename": str(dat_path.resolve()),  # 🔥 FIX
        "results_dir": str(output_dir),
        "probe_path": str(probe_path),
        "fs": fs,
        "n_chan_bin": 16,
    }

    print("\n==============================")
    print("Running Kilosort4")
    print(f"File   : {dat_path.resolve()}")
    print(f"Output : {output_dir}")
    print("==============================\n")

    run_kilosort(settings=settings)