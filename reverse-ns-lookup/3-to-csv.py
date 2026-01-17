import json
import csv
import os
import argparse

def json_to_csv(input_file, output_file=None, list_delimiter="|"):
    # Automatically generate output CSV filename if not provided
    if not output_file:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}.csv"

    # Load JSON
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return
    except json.JSONDecodeError:
        print(f"Invalid JSON: {input_file}")
        return

    records = data.get("records", [])
    if not records:
        print("No records found in JSON.")
        return

    # Determine headers safely
    all_keys = set()
    for record in records:
        all_keys.update(record.keys())

    # Ensure hostname is first column
    all_keys.discard("hostname")
    headers = ["hostname"] + sorted(all_keys)

    # Write CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for record in records:
            row = {}
            for key in headers:
                value = record.get(key, "")
                if isinstance(value, list):
                    value = list_delimiter.join(map(str, value))
                row[key] = value
            writer.writerow(row)

    print(f"CSV saved to {output_file} with {len(records)} records.")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a JSON file of records to CSV. 'hostname' will be the first column."
    )
    parser.add_argument("input_file", help="Path to input JSON file")
    parser.add_argument("-o", "--output", help="Output CSV file (optional)")
    parser.add_argument("-d", "--delimiter", default="|", help="Delimiter for list fields (default: '|')")

    args = parser.parse_args()
    json_to_csv(args.input_file, args.output, args.delimiter)


if __name__ == "__main__":
    main()
