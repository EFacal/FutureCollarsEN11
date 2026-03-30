import sys
import os
import csv
import json
import pickle


# -------------------------
# BASE CLASS
# -------------------------
class FileHandler:
    def __init__(self, path):
        self.path = path
        self.data = []

    def load(self):
        raise NotImplementedError

    def save(self, dst):
        raise NotImplementedError

    def apply_changes(self, changes):
        for change in changes:
            try:
                parts = change.split(",", 2)
                if len(parts) != 3:
                    raise ValueError

                x = int(parts[0])
                y = int(parts[1])
                value = parts[2]

                if y < 0 or y >= len(self.data):
                    print(f"Skipping '{change}': row out of range")
                    continue

                if x < 0 or x >= len(self.data[y]):
                    print(f"Skipping '{change}': column out of range")
                    continue

                self.data[y][x] = value

            except Exception:
                print(f"Skipping invalid change: '{change}'")

    def display(self):
        print("\nModified content:")
        for row in self.data:
            print(",".join(row))


# -------------------------
# CSV HANDLER
# -------------------------
class CSVHandler(FileHandler):
    def load(self):
        with open(self.path, newline="") as f:
            self.data = list(csv.reader(f))

    def save(self, dst):
        with open(dst, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.data)


# -------------------------
# JSON HANDLER
# -------------------------
class JSONHandler(FileHandler):
    def load(self):
        with open(self.path, "r") as f:
            self.data = json.load(f)

    def save(self, dst):
        with open(dst, "w") as f:
            json.dump(self.data, f, indent=2)


# -------------------------
# PICKLE HANDLER
# -------------------------
class PickleHandler(FileHandler):
    def load(self):
        with open(self.path, "rb") as f:
            self.data = pickle.load(f)

    def save(self, dst):
        with open(dst, "wb") as f:
            pickle.dump(self.data, f)


# -------------------------
# FACTORY FUNCTION
# -------------------------
def get_handler(path):
    if path.endswith(".csv"):
        return CSVHandler(path)
    elif path.endswith(".json"):
        return JSONHandler(path)
    elif path.endswith(".pickle"):
        return PickleHandler(path)
    else:
        raise ValueError("Unsupported file type")


# -------------------------
# HELPER
# -------------------------
def list_files(path):
    directory = os.path.dirname(path) or "."
    print("Files in directory:")
    for f in os.listdir(directory):
        print("-", f)


# -------------------------
# MAIN
# -------------------------
def main():
    if len(sys.argv) < 3:
        print("Usage: python reader.py <src> <dst> <changes...>")
        return

    src = sys.argv[1]
    dst = sys.argv[2]
    changes = sys.argv[3:]

    if not os.path.isfile(src):
        print(f"Error: '{src}' is not a valid file.")
        list_files(src)
        return

    try:
        handler = get_handler(src)
    except ValueError as e:
        print(e)
        return

    # Load data
    handler.load()

    # Apply changes
    handler.apply_changes(changes)

    # Display
    handler.display()

    # Save
    try:
        handler_dst = get_handler(dst)
        handler_dst.data = handler.data
        handler_dst.save(dst)
        print(f"\nSaved to '{dst}'")
    except Exception as e:
        print("Error saving file:", e)


if __name__ == "__main__":
    main()