from pathlib import Path
from config import DATA_ROOT, OUTPUT_ROOT, PROBE_PATH
from run_kilosort import run_one_recording

def find_dat_files(root: Path):
    """Recursively find all .dat files in the given root directory."""
    return list(root.rglob('*.dat'))

def main():
    data_root = Path(DATA_ROOT).resolve()
    output_root = Path(OUTPUT_ROOT).resolve()
    probe_path = path(PROBE_PATH).resolve()
    
    print("\n==========")
    print("Kilosort4 Batch Runner")
    print(f"DATA ROOT : {data_root}")
    print(f"OUTPUT ROOT : {output_root}")
    print(f"PROBE PATH : {probe_path}")
    print("============\n")
    
    if not data_root.exists():
     raise FileNotFoundError(f"DATA_ROOT does not exist {data_root}")
     
     if not probe_path.exists():
      raise FileNotFoundError(f"PROBE_PATH does not exist {probe_path}")
     
     dat_files = find_data_files(data_root)
     print(f"Found {len(data_files)} .dat files to process.\n")
     
     if len(data_files) == 0:
        print("No .dat files found. check DATA_ROOT")
     return
     
     for dat in data_files:
        dat = dat.resolve()
     
     try:
        relative = dat.relative_to(data_root)
     except ValueError:
        print(f"Skipping file outside DATA_ROOT: {dat}")
   
        
    output_dir = (output_root / relative.parent / "kilosort4").resolve()
    
    print("\n--------")
    print(f"Running Kilosort4 on: {dat.name}")
    print(f"Full path : {dat}")
    print(f"Output dir: {output_dir}")
    print("----------")
    
    try:
        run_one_recording(
            dat_path=dat,
            output_dir=output_dir,
            probe_path=probe_path,
            fs=25000,
            )
    except Exception as e:
        print(f"\n Failed on {dat,name}")
        print(f"Error: {e}")
        
        
print("\n Batch processing complete.\n")

if __name__ == "__main__":
    main()
