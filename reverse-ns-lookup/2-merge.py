import json
from glob import glob
from datetime import date
import argparse
import os
import shutil

def merge_ns_files(ns_name, delete=False, move=True):
    """
    Merge all JSON files matching <ns_name>_*.json into one <ns_name>.json
    Optionally delete or move the original files.
    """
    file_pattern = f"{ns_name}_*.json"
    output_file = f"{ns_name}.json"
    all_records = []

    # Find all files matching the pattern
    files = glob(file_pattern)
    if not files:
        print(f"No files found matching pattern: {file_pattern}")
        return

    # Process each file
    for filename in sorted(files, key=lambda x: int(os.path.splitext(x)[0].split("_")[-1])):
        try:
            print(f"Processing {filename}...")
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Adjust this path according to your JSON structure
                records = data.get("pageProps", {}).get("serverResponse", {}).get("data", {}).get("records", [])
                all_records.extend(records)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Skipping {filename}: {e}")

    # Prepare merged output
    merged_data = {
        "ns": ns_name,
        "date": date.today().isoformat(),
        "total_records": len(all_records),
        "records": all_records
    }

    # Write the merged JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=2)
    print(f"Merged {len(all_records)} records into {output_file}")

    # Handle move or delete of original files
    if delete:
        for f in files:
            os.remove(f)
        print(f"Deleted {len(files)} original files.")
    elif move:
        dir_name = ns_name
        os.makedirs(dir_name, exist_ok=True)
        for f in files:
            shutil.move(f, os.path.join(dir_name, os.path.basename(f)))
        print(f"Moved {len(files)} original files into directory '{dir_name}'.")


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple JSON files for a given NS name into one JSON."
    )
    parser.add_argument("ns_name", help="The NS name, e.g., 'daisy.ns.cloudflare.com'")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--delete", action="store_true", help="Delete input files after merging")
    group.add_argument("-m", "--move", action="store_true", help="Move input files to a directory (default)")

    args = parser.parse_args()

    # By default, move is True unless delete is specified
    merge_ns_files(args.ns_name, delete=args.delete, move=(not args.delete))


if __name__ == "__main__":
    main()
