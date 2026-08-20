#!/usr/bin/env python3
"""Rename Nishat 3-Piece images based on product codes from images."""
import os

base = r"E:/Work/Al-Deewan Website/Nishat Linen 3-Piece"

rename_map = [
    # Article 1: 42206126-R (Mauve/Burgundy)
    ("WhatsApp Image 2026-08-18 at 8.35.39 PM.jpeg", "Nishat3Pce_42206126-R_main.jpg"),
    ("WhatsApp Image 2026-08-18 at 8.35.39 PM (1).jpeg", "Nishat3Pce_42206126-R_view2.jpg"),
    ("WhatsApp Image 2026-08-18 at 8.35.39 PM (2).jpeg", "Nishat3Pce_42206126-R_view3.jpg"),
    # Article 2: 42303181-R (Dark Green)
    ("WhatsApp Image 2026-08-18 at 8.35.40 PM.jpeg", "Nishat3Pce_42303181-R_main.jpg"),
    ("WhatsApp Image 2026-08-18 at 8.35.40 PM (1).jpeg", "Nishat3Pce_42303181-R_view2.jpg"),
    ("WhatsApp Image 2026-08-18 at 8.35.40 PM (2).jpeg", "Nishat3Pce_42303181-R_view3.jpg"),
    # Article 3: 42303202-R (Olive/Mustard)
    ("WhatsApp Image 2026-08-18 at 8.35.41 PM.jpeg", "Nishat3Pce_42303202-R_main.jpg"),
    ("WhatsApp Image 2026-08-18 at 8.35.41 PM (1).jpeg", "Nishat3Pce_42303202-R_view2.jpg"),
    # Article 4: 42303186-R (Navy Blue)
    ("WhatsApp Image 2026-08-18 at 8.35.42 PM.jpeg", "Nishat3Pce_42303186-R_main.jpg"),
    ("WhatsApp Image 2026-08-18 at 8.35.42 PM (1).jpeg", "Nishat3Pce_42303186-R_view2.jpg"),
]

print(f"Total renames: {len(rename_map)}")
print()
for old, new in rename_map:
    old_path = os.path.join(base, old)
    new_path = os.path.join(base, new)
    exists_old = os.path.exists(old_path)
    exists_new = os.path.exists(new_path)
    print(f"{'OK' if exists_old and not exists_new else 'WARN' if exists_new else 'ERR'}  {old}")
    print(f"      -> {new}")
    if exists_new:
        print(f"       [WARNING: target already exists!]")
    print()

# Uncomment below to execute
# for old, new in rename_map:
#     os.rename(os.path.join(base, old), os.path.join(base, new))
#     print(f"Renamed: {old} -> {new}")
# print("\nDone!")
