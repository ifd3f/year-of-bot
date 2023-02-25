#!/usr/bin/env bash

files=(subjects.txt predictions/*.txt)

tmp=$(mktemp)

for f in "${files[@]}"; do
    LC_ALL=C sort -f -o "$f" "$f"
    cp "$f" $tmp
    uniq $tmp > "$f"
done

