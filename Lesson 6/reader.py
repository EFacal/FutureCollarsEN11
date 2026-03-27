import sys
import os
import csv


def print_files_in_directory(path):
    directory = os.path.dirname(path) or "."
    print("Available files in directory:")
    for f in os.listdir(directory):
        print(" -", f)


def main():
    # Check minimum arguments
    if len(sys.argv) < 3:
        print("Usage: python reader.py <src> <dst> <change1> <change2> ...")
        return

    src = sys.argv[1]
    dst = sys.argv[2]
    changes = sys.argv[3:]

    # Check if source file exists
    if not os.path.isfile(src):
        print(f"Error: '{src}' is not a valid file.")
        print_files_in_directory(src)
        return

    # Read CSV into memory
    data = []
    try:
        with open(src, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
    except Exception as e:
        print("Error reading file:", e)
        return

    # Apply changes
    for change in changes:
        try:
            parts = change.split(",", 2)
            if len(parts) != 3:
                raise ValueError("Invalid format")

            x = int(parts[0])  # column
            y = int(parts[1])  # row
            value = parts[2]

            if y < 0 or y >= len(data):
                print(f"Skipping change '{change}': row out of range")
                continue

            if x < 0 or x >= len(data[y]):
                print(f"Skipping change '{change}': column out of range")
                continue

            data[y][x] = value

        except Exception:
            print(f"Skipping invalid change: '{change}'")

    # Print modified CSV
    print("\nModified CSV content:")
    for row in data:
        print(",".join(row))

    # Save to destination
    try:
        with open(dst, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"\nFile saved to '{dst}'")
    except Exception as e:
        print("Error writing file:", e)


if __name__ == "__main__":
    main()