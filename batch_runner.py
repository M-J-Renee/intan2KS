from pathlib import Path
from config import DATA_ROOT, OUTPUT_ROOT, PROBE_PATH

def find_dat_files(root: Path):
    """Recursively find all .dat files in the given root directory."""
    return list(root.rglob('*.dat'))

def main():
    dat_files = find_dat_files(DATA_ROOT)
    print(f"Found {len(dat_files)} .dat files to process.")
    
    for dat in dat_files:
        relative = dat.relative_to(DATA_ROOT)
        output_dir = OUTPUT_ROOT / relative.parent/ "kilosort4"

        print("Would process:")
        print(f"  Data file: {dat}")
        print(f"  Output dir: {output_dir}\n")

        if __name__ == "__main__":
          main() 