#!/usr/bin/env python3
"""
Perform independent randomization of Western and Jyotish profiles.
Saves mapping.json in the output folder.

Usage: python randomize.py /path/to/output/folder
"""

import random
import json
import sys
import os
from datetime import datetime

def randomize(output_folder):
    west_files = ["west_BD", "west_BD+90", "west_BD-90", "west_BD+180"]
    djo_files  = ["djo_BD",  "djo_BD+90",  "djo_BD-90",  "djo_BD+180"]

    random.seed()

    # Shuffle independently
    random.shuffle(west_files)
    random.shuffle(djo_files)

    # Ensure no positional correspondence (same date suffix at same position index)
    def date_suffix(name):
        return name.replace("west_", "").replace("djo_", "")

    attempts = 0
    while any(date_suffix(west_files[i]) == date_suffix(djo_files[i]) for i in range(4)):
        random.shuffle(djo_files)
        attempts += 1
        if attempts > 10000:
            raise RuntimeError("Could not find non-overlapping arrangement after 10000 attempts")

    west_labels = ["A", "B", "C", "D"]
    djo_labels  = ["K", "L", "M", "N"]

    west_map = {label: fname for label, fname in zip(west_labels, west_files)}
    djo_map  = {label: fname for label, fname in zip(djo_labels,  djo_files)}

    # Verify all txt files exist
    missing = []
    for fname in west_files + djo_files:
        path = os.path.join(output_folder, fname + ".txt")
        if not os.path.exists(path):
            missing.append(fname + ".txt")
    if missing:
        print(f"WARNING: Missing files: {missing}")
        print("Continuing with randomization anyway...")

    # Build full mapping with date info
    date_info = {
        "BD":     {"label": "BD",     "type": "Истинная дата"},
        "BD+90":  {"label": "BD+90",  "type": "BD + 90 дней"},
        "BD-90":  {"label": "BD-90",  "type": "BD − 90 дней"},
        "BD+180": {"label": "BD+180", "type": "BD + 180 дней"},
    }

    mapping = {
        "west": west_map,
        "djo":  djo_map,
        "date_info": date_info,
        "randomized_at": datetime.now().isoformat(),
        "positional_conflicts": sum(
            date_suffix(west_files[i]) == date_suffix(djo_files[i]) for i in range(4)
        ),
    }

    # Save mapping.json
    mapping_path = os.path.join(output_folder, "mapping.json")
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    # Print summary
    print("=== РАНДОМИЗАЦИЯ ВЫПОЛНЕНА ===")
    print()
    print("Западная школа:")
    for label, fname in west_map.items():
        suffix = date_suffix(fname)
        print(f"  {label} → {fname}  [{date_info[suffix]['type']}]")
    print()
    print("Джйотиш:")
    for label, fname in djo_map.items():
        suffix = date_suffix(fname)
        print(f"  {label} → {fname}  [{date_info[suffix]['type']}]")
    print()
    print(f"Позиционных совпадений: {mapping['positional_conflicts']}")
    print(f"mapping.json сохранён: {mapping_path}")

    return mapping


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python randomize.py /path/to/output/folder")
        sys.exit(1)

    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"Error: folder not found: {folder}")
        sys.exit(1)

    randomize(folder)
