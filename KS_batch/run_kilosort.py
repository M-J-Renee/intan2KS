from pathlib import Path
from kilosort import run_kilosort


def run_one_recording(dat_path: Path, output_dir: Path, probe_path: Path, fs: int = 30000):
    """
    Run Kilosort4 on a single .dat file.
    """

    # make sure output folder exists
    output_dir.mkdir(parents=True, exist_ok=True)

    settings = {
        "filename": dat_path.name,
        "data_dir": str(dat_path.parent),
        "results_dir": str(output_dir),
        "probe_path": str(probe_path),
        "fs": fs,

        # IMPORTANT: adjust later if needed
        "n_chan_bin": 32,
    }

    print("\n==============================")
    print("Running Kilosort4")
    print(f"File   : {dat_path}")
    print(f"Output : {output_dir}")
    print("==============================\n")

    run_kilosort(settings=settings)