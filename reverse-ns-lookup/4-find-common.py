import json
import argparse
from datetime import date

def find_common_records(files, ns_name=None):
    """
    Find records with common 'hostname' across multiple JSON files
    and save them to common-<today>.json with metadata.
    """
    if len(files) < 2:
        print("Please provide at least two JSON files to compare.")
        return

    # Load all records from each file
    all_records_list = []
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                records = json.load(f).get("records", [])
                all_records_list.append(records)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Skipping {file}: {e}")

    if len(all_records_list) < 2:
        print("Not enough valid files to find common records.")
        return

    # Build a set of hostnames for each file
    hostname_sets = [set(r["hostname"] for r in records) for records in all_records_list]

    # Find hostnames common to all files
    common_hostnames = set.intersection(*hostname_sets)
    print(f"Found {len(common_hostnames)} common hostnames across {len(files)} files.")

    # Gather one record per common hostname (from first file that contains it)
    hostname_to_record = {}
    for records in all_records_list:
        for r in records:
            hn = r.get("hostname")
            if hn in common_hostnames and hn not in hostname_to_record:
                hostname_to_record[hn] = r

    common_records = list(hostname_to_record.values())

    # Prepare metadata
    today_str = date.today().isoformat()
    ns_value = ns_name if ns_name else (files[0].split(".")[0])  # default to first file's prefix

    merged_data = {
        "ns": ns_value,
        "date": today_str,
        "total_records": len(common_records),
        "records": common_records
    }

    # Output filename
    output_file = f"common-{today_str}.json"

    # Save
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=2)

    print(f"Saved {len(common_records)} common records to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Find records with common hostnames across multiple JSON files."
    )
    parser.add_argument(
        "files", nargs="+", help="List of JSON files to compare (2 or more)"
    )
    parser.add_argument(
        "-n", "--ns", help="NS name to include in the merged JSON metadata"
    )

    args = parser.parse_args()
    find_common_records(args.files, ns_name=args.ns)


if __name__ == "__main__":
    main()
