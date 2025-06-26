#!/bin/bash

# --- Screen recording function ---
record_screen() {
    local mode=$1
    local save_dir=${2:-"$HOME/Videos/Recordings"}
    mkdir -p "$save_dir"

    local filename="recording_$(date +'%Y-%m-%d_%H-%M-%S').mp4"
    local final_path="$save_dir/$filename"

    if [[ "$mode" == "area" ]]; then
        region=$(slurp)
        if [[ -z "$region" ]]; then
            notify-send -u critical -a "Tsumiki Recorder" "❌ No area selected"
            return 1
        fi
        if ! wf-recorder -g "$region" -f "$final_path"; then
            notify-send -u critical -a "Tsumiki Recorder" "❌ Recording failed (area)"
            return 1
        fi
    else
        if ! wf-recorder -f "$final_path"; then
            notify-send -u critical -a "Tsumiki Recorder" "❌ Recording failed (full)"
            return 1
        fi
    fi

    notify-send -a "Tsumiki Recorder" -i media-record "✅ Recording saved in ${save_dir}"
    echo "Recording saved to: $final_path"
}


# --- Dependency check ---
check_dependencies() {
    local missing=0

    for cmd in wf-recorder notify-send; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "Error: '$cmd' is not installed or not in PATH."
            missing=1
        fi
    done

    if [[ "$1" == "area" ]] && ! command -v slurp &> /dev/null; then
        echo "Error: 'slurp' is required for area selection but not found."
        missing=1
    fi

    if [ "$missing" -eq 1 ]; then
        exit 1
    fi
}

# --- Main argument handling ---
MODE="$1"
CUSTOM_PATH="$2"

case "$MODE" in
    full|f)
        check_dependencies "full"
        record_screen "full" "$CUSTOM_PATH"
        ;;
    area|p)
        check_dependencies "area"
        record_screen "area" "$CUSTOM_PATH"
        ;;
    *)
        echo "Usage: $0 [full|f|area|p] [optional: /custom/save/path]"
        exit 1
        ;;
esac
