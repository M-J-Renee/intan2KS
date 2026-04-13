from pathlib import Path
from config import DATA_ROOT, OUTPUT_ROOT, PROBE_PATH
from run_kilosort import run_one_recording

def find_dat_files(root: Path):
    """Recursively find all .dat files in the given root directory."""
    return list(root.rglob('*.dat'))

def main():
    dat_files = find_dat_files(DATA_ROOT)
    print(f"Found {len(dat_files)} .dat files to process.\n")

    for dat in dat_files:
        relative = dat.relative_to(DATA_ROOT)
        output_dir = OUTPUT_ROOT / relative.parent / "kilosort4"

        print(f"\n=== Running Kilosort4 on {dat.name} ===")

        run_one_recording(
            dat_path=dat,
            output_dir=output_dir,
            probe_path=PROBE_PATH,
            fs=30000
        )

if __name__ == "__main__":
    main() 