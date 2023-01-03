#!/usr/bin/env bash

files=(subjects.txt predictions/*.txt)

for f in "${files[@]}"; do
    sort -f -o "$f" "$f"
done

