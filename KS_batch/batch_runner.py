from pathlib import Path
from config import DATA_ROOT, OUTPUT_ROOT, PROBE_PATH
from run_kilosort import run_one_recording
from datetime import datetime, timedelta
import shutil
import numpy as np
import scipy.io


TWO_HOURS = timedelta(hours=2)


def load_meta(dat_path: Path) -> dict:
    """Load _meta.mat saved alongside a .dat file."""
    meta_path = dat_path.with_name(dat_path.stem + '_meta.mat')
    return scipy.io.loadmat(str(meta_path), simplify_cells=True)




def extract_datetime_from_name(dat_path: Path):
   
    stem = dat_path.stem
    parts = stem.split("_")

    date_str = parts[-2]
    time_str = parts[-1]

    return datetime.strptime(date_str + time_str, "%y%m%d%H%M%S")


def extract_subject_from_name(dat_path: Path):
   
    return dat_path.stem.split("_")[0]


def find_dat_files(root: Path):
    return list(root.rglob("*.dat"))



def group_sessions(dat_files):
    """
    Groups files by:
        1) Same subject
        2) Same calendar day
        3) Within 2 hours of previous file
    """

    dat_files = sorted(dat_files, key=extract_datetime_from_name)

    sessions = []
    current_group = []

    for dat in dat_files:

        dt = extract_datetime_from_name(dat)
        subj = extract_subject_from_name(dat)

        if not current_group:
            current_group.append(dat)
            continue

        last = current_group[-1]
        last_dt = extract_datetime_from_name(last)
        last_subj = extract_subject_from_name(last)

        same_subject = subj == last_subj
        same_day = dt.date() == last_dt.date()
        within_window = (dt - last_dt) <= TWO_HOURS

        if same_subject and same_day and within_window:
            current_group.append(dat)
        else:
            sessions.append(current_group)
            current_group = [dat]

    if current_group:
        sessions.append(current_group)

    return sessions


def concatenate_dat_files(dat_group, concat_path, metas):
    import json

    concat_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\nCreating concatenated file:\n{concat_path}")

    fs = int(metas[0]['fs'])
    n_channels = int(metas[0]['n_channels'])

    metadata = {
        "files": [],
        "start_datetimes": [],
        "sample_offsets": [],
        "fs": fs,
        "n_channels": n_channels,
    }

    sample_offset = 0
    combined_events = {}

    with open(concat_path, "wb") as wfd:

        for dat, meta in zip(dat_group, metas):

            dt = extract_datetime_from_name(dat)

            print(f"  Adding {dat.name}")

            n_bytes = dat.stat().st_size
            n_samples = n_bytes // (2 * n_channels)

            metadata["files"].append(str(dat))
            metadata["start_datetimes"].append(dt.isoformat())
            metadata["sample_offsets"].append(sample_offset)

            # Shift this recording's events by its start time in the concat file
            offset_sec = sample_offset / fs
            for ch, timestamps in meta['events'].items():
                shifted = np.array(timestamps, dtype=float).ravel() + offset_sec
                if ch not in combined_events:
                    combined_events[ch] = []
                combined_events[ch].append(shifted)

            with open(dat, "rb") as fd:
                shutil.copyfileobj(fd, wfd)

            sample_offset += n_samples

    for ch in combined_events:
        combined_events[ch] = np.concatenate(combined_events[ch])

    # Save JSON manifest
    meta_path = concat_path.with_suffix(".json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved manifest: {meta_path}")

    # Save combined events as .mat alongside the concat .dat
    concat_meta_path = concat_path.with_name(concat_path.stem + '_meta.mat')
    scipy.io.savemat(str(concat_meta_path), {
        'events': combined_events,
        'fs': fs,
        'n_channels': n_channels,
    })
    print(f"Saved combined events: {concat_meta_path}")


def main():

    data_root = Path(DATA_ROOT).resolve()
    output_root = Path(OUTPUT_ROOT).resolve()
    probe_path = Path(PROBE_PATH).resolve()

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

    dat_files = find_dat_files(data_root)
    print(f"Found {len(dat_files)} .dat files.\n")

    if len(dat_files) == 0:
        print("No .dat files found. Check DATA_ROOT.")
        return

    sessions = group_sessions(dat_files)
    print(f"Grouped into {len(sessions)} session(s).\n")

    for group in sessions:

        group = sorted(group, key=extract_datetime_from_name)

        first_dt = extract_datetime_from_name(group[0])
        subject = extract_subject_from_name(group[0])
        date_str = first_dt.strftime("%y%m%d")

        metas = [load_meta(dat) for dat in group]
        fs = int(metas[0]['fs'])
        n_channels = int(metas[0]['n_channels'])

        # -------------------------
        # SINGLE FILE SESSION
        # -------------------------
        if len(group) == 1:

            dat_path = group[0]
            session_name = group[0].stem

            print(f"\nRunning single file session: {dat_path.name}")

        # -------------------------
        # MULTI-FILE SESSION
        # -------------------------
        else:

            session_name = f"{subject}_{date_str}_concat"
            concat_dir = output_root / "concatenated"
            dat_path = concat_dir / f"{session_name}.dat"

            if not dat_path.exists():
                concatenate_dat_files(group, dat_path, metas)
            else:
                print(f"\nConcatenated file already exists: {dat_path}")

        output_dir = (output_root / "kilosort4" / session_name).resolve()

        print("\n--------")
        print(f"Running Kilosort4 on session: {session_name}")
        print(f"Input file : {dat_path}")
        print(f"Output dir : {output_dir}")
        print(f"fs={fs} Hz, n_channels={n_channels}")
        print("----------")

        try:
            run_one_recording(
                dat_path=dat_path,
                output_dir=output_dir,
                probe_path=probe_path,
                fs=fs,
                n_chan_bin=n_channels,
            )
        except Exception as e:
            print(f"\nFailed on session {session_name}")
            print(f"Error: {e}")
            continue

    print("\nBatch processing complete.\n")


if __name__ == "__main__":
    main()