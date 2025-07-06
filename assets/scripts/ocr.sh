#!/bin/bash
set -euo pipefail


# Check dependencies
for cmd in grimblast tesseract wl-copy notify-send; do
    command -v $cmd &>/dev/null || {
        notify-send "OCR Tool" "Missing dependency: $cmd"
        exit 1
    }
done

# Capture screenshot and perform OCR
ocr_text=$(grimblast --freeze save area - | tesseract -l eng - - 2>/dev/null || true)

# Check if OCR succeeded
if [[ -n "$ocr_text" ]]; then
    echo -n "$ocr_text" | wl-copy
    notify-send -a "Tsumiki" "OCR Success" "Text Copied to Clipboard"
else
    notify-send -a "Tsumiki" "OCR Failed" "No text recognized or operation failed"
fi
