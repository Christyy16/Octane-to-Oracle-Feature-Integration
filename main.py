from octane_api import get_features
from parser import parse_features
from save_to_oracle import save_features
import json

def main():

    print("=" * 60)
    print("START OCTANE FEATURE SYNC")
    print("=" * 60)
    print()


    response_json = get_features()

    if response_json is None:
        print("Failed to get data from Octane API.")
        return
    
    records = parse_features(response_json)

    print(f"\nParsed Records: {len(records)}")

    if not records:
        print("No records found.")
        return

    print("FIRST RECORD")
    print("-" * 60)
    print(records[0])

    save_features(records)

    print()
    print("=" * 60)
    print("OCTANE FEATURE SYNC COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()