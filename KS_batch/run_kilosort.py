from pathlib import Path
from kilosort import run_kilosort


def run_one_recording(dat_path: Path, output_dir: Path, probe_path: Path, fs: int, n_chan_bin: int, dmin: int, dminx: int, min_template_size: int, nearest_templates: int):

    output_dir.mkdir(parents=True, exist_ok=True)

    settings = {
        "filename": str(dat_path.resolve()),
        "results_dir": str(output_dir),
        "probe_path": str(probe_path),
        "fs": fs,
        "n_chan_bin": n_chan_bin,
        "dmin": dmin,
        "dminx": dminx,
        "min_template_size": min_template_size,
        "nearest_templates": nearest_templates,
    }

    print("\n==============================")
    print("Running Kilosort4")
    print(f"File   : {dat_path.resolve()}")
    print(f"Output : {output_dir}")
    print("==============================\n")

    run_kilosort(settings=settings)