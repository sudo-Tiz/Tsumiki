#!/bin/bash

# --- Screen recording function ---
record_screen() {
    local fullscreen=$1
    local save_dir=${2:-"$HOME/Videos/Recordings"}
    local allow_audio=$3
    mkdir -p "$save_dir"

    local timestamp
    timestamp=$(date +'%Y-%m-%d_%H-%M-%S')
    local file_path="$save_dir/$timestamp.mp4"

    local area=""
    local audio=""
    if [[ "$fullscreen" == "false" ]]; then
        region=$(slurp)
        if [[ -z "$region" ]]; then
            notify-send -u critical -a "Tsumiki Recorder" "❌ No area selected"
            return 1
        fi
        area="-g \"$region\""
    fi

    if [[ "$allow_audio" == "true" ]]; then
        audio="--audio"
    fi

    local command="wf-recorder $audio --file=\"$file_path\" --pixel-format yuv420p $area"

    # Run command
    eval "$command"
    local status=$?

    if [[ $status -ne 0 ]]; then
        notify-send -u critical -a "Tsumiki Recorder" "❌ Recording failed"
        return $status
    fi

    notify-send -a "Tsumiki Recorder" -i media-record "✅ Recording saved in $file_path"
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

    if [[ "$1" == "false" ]] && ! command -v slurp &> /dev/null; then
        echo "Error: 'slurp' is required for area selection but not found."
        missing=1
    fi

    if [[ $missing -eq 1 ]]; then
        exit 1
    fi
}

# --- Main argument handling ---
MODE="$1"                # full, area, or short form
CUSTOM_PATH="$2"         # optional save directory
AUDIO_FLAG="$3"          # "audio" to enable audio recording

case "$MODE" in
    full|f)
        check_dependencies "true"
        record_screen "true" "$CUSTOM_PATH" "$([[ $AUDIO_FLAG == "audio" ]] && echo "true" || echo "false")"
        ;;
    area|p)
        check_dependencies "false"
        record_screen "false" "$CUSTOM_PATH" "$([[ $AUDIO_FLAG == "audio" ]] && echo "true" || echo "false")"
        ;;
    *)
        echo "Usage: $0 [full|f|area|p] [optional: /custom/save/path] [optional: audio]"
        echo "Example: $0 area ~/Videos audio"
        exit 1
        ;;
esac
