#!/usr/bin/env bash

cd "$(dirname "$BASH_SOURCE")" || {
    echo "Error getting script directory" >&2
    exit 1
}

echo
echo "Keyboard tracking is multi-threaded, which requires sudo access."
echo

sudo ./dist/air_canvas/air_canvas 
