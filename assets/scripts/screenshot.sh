#!/bin/bash

# --- Screenshot function ---
take_screenshot() {
    local mode=$1
    local save_dir=${2:-"$HOME/Pictures/Screenshots"}
    local annotate=$3
    mkdir -p "$save_dir"

    local filename="screenshot_$(date +'%Y-%m-%d_%H-%M-%S').png"
    local final_path="$save_dir/$filename"

    if [[ "$annotate" == true ]]; then
        local tmp_file
        tmp_file="$(mktemp /tmp/screenshot_XXXXXX.png)"

        if ! grimblast save "$mode" "$tmp_file"; then
            notify-send -u critical -a "Tsumiki Screenshot" "❌ Screenshot failed (annotated mode)"
            rm -f "$tmp_file"
            return 1
        fi

        if ! satty -f "$tmp_file" -o "$final_path"; then
            notify-send -u critical -a "Tsumiki Screenshot" "❌ Annotation failed"
            rm -f "$tmp_file"
            return 1
        fi

        rm -f "$tmp_file"
    else
        if ! grimblast save "$mode" "$final_path"; then
            notify-send -u critical -a "Tsumiki Screenshot" "❌ Screenshot failed"
            return 1
        fi
    notify-send -a "Tsumiki Screenshot" -i "$final_path" "✅ Saved in ${save_dir}"
    fi


}


# --- Dependency check ---
check_dependencies() {
    local annotate=$1
    local missing=0

    for cmd in grimblast; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "Error: '$cmd' is not installed or not in PATH."
            missing=1
        fi
    done

    if [[ "$annotate" == true ]] && ! command -v satty &> /dev/null; then
        echo "Error: 'satty' is not installed but annotation was requested."
        missing=1
    fi

    if [ "$missing" -eq 1 ]; then
        exit 1
    fi
}

# --- Main argument handling ---
MODE="$1"
CUSTOM_PATH="$2"
ANNOTATE_FLAG="$3"
ANNOTATE=false

if [[ "$ANNOTATE_FLAG" == "-a" || "$ANNOTATE_FLAG" == "--annotate" ]]; then
    ANNOTATE=true
fi

# Handle modes
case "$MODE" in
    full|f)
        check_dependencies "$ANNOTATE"
        take_screenshot screen "$CUSTOM_PATH" "$ANNOTATE"
        ;;
    area|p)
        check_dependencies "$ANNOTATE"
        take_screenshot area "$CUSTOM_PATH" "$ANNOTATE"
        ;;
    *)
        echo "Usage: $0 [full|f|area|p] [optional: /custom/save/path] [-a|--annotate]"
        echo "Example: $0 full /my/path --annotate"
        exit 1
        ;;
esac
