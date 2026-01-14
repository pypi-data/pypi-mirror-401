#!/bin/bash

# find "/home/leyo/Music/deemix Music/Gizo Evoracci - Baguenaude D'un Negre Libre" -type f -print0 | while IFS= read -r -d '' file; do
#     echo "Processing $file"
#     uv run kamasi "$file"
# done


find "/home/leyo/Music/deemix Music/Gizo Evoracci - Superfly/" -type f -print0 | while IFS= read -r -d '' file; do
    echo "Processing $file"
    uv run kamasi -v --config config.yaml "$file"
done
#
# find "~/Music/deemix Music/" -type f -print0 | while IFS= read -r -d '' file; do
#     echo "Processing $file"
#     # uv run kamasi "$file"
# done
#
#
# find "~/Music/deemix Music/" -type f -print0 | while IFS= read -r -d '' file; do
#     echo "Processing $file"
#     # uv run kamasi "$file"
# done
#
#
# find "~/Music/deemix Music/" -type f -print0 | while IFS= read -r -d '' file; do
#     echo "Processing $file"
#     # uv run kamasi "$file"
# done
