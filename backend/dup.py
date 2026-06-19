import os
import hashlib

ROOT = "data"

hashes = {}
duplicates = []

for root, _, files in os.walk(ROOT):
    for file in files:
        path = os.path.join(root, file)

        try:
            with open(path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            if file_hash in hashes:
                duplicates.append((path, hashes[file_hash]))
            else:
                hashes[file_hash] = path

        except Exception as e:
            print(f"Skipping {path}: {e}")

print(f"\nUnique files: {len(hashes)}")
print(f"Duplicate files: {len(duplicates)}")

for dup, original in duplicates:
    print("\nDuplicate:")
    print("Original :", original)
    print("Duplicate:", dup)