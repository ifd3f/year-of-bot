#!/bin/sh

tmp=$(mktemp)

cd year_of_bot/data

for f in subjects.txt predictions/*.txt; do
    LC_ALL=C sort -f -o "$f" "$f"
    cp "$f" "$tmp"
    uniq "$tmp" > "$f"
done

