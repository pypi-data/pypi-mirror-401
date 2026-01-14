
import json, csv, sys, argparse

def main():
    p = argparse.ArgumentParser(description="Convert JSON to CSV")
    p.add_argument("input", help="Input JSON file")
    p.add_argument("output", help="Output CSV file")
    args = p.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("JSON must be a list of objects")
        sys.exit(1)

    with open(args.output, "w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    main()
