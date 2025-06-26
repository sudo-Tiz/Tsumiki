#!/bin/bash



# --- Dependency check ---
check_dependencies() {
    local missing=0

    for cmd in hyprpicker; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "Error: '$cmd' is not installed or not in PATH."
            missing=1
        fi
    done

    if [ "$missing" -eq 1 ]; then
        exit 1
    fi
}

pick_rgb(){

# Execute hyprpicker with RGB format and save the output to a variable
hyprpicker -a -n -f rgb && sleep 0.1

# Create a temporal 64x64 PNG file with the color in /tmp using convert
magick -size 64x64 xc:"rgb($(wl-paste))" /tmp/color.png

# Send a notification using the file as an icon
notify-send "RGB color picked" "rgb($(wl-paste))" -i /tmp/color.png -a "Hyprpicker"

# Remove the temporal file
rm /tmp/color.png

# Exit
exit 0

}


pick_hex(){

# Execute hyprpicker and save the output to a variable
hyprpicker -a -n -f hex && sleep 0.1

# Create a temporal 64x64 PNG file with the color in /tmp using convert
magick -size 64x64 xc:"$(wl-paste)" /tmp/color.png

# Send a notification using the file as an icon
notify-send "HEX color picked" "$(wl-paste)" -i /tmp/color.png -a "Hyprpicker"

# Remove the temporal file
rm /tmp/color.png

# Exit
exit 0

}


pick_hsv(){

# Copy the color to the clipboard
echo -n "$(hyprpicker -n -f hsv)" | wl-copy -n

# Create a temporal 64x64 PNG file with the color in /tmp using convert
magick -size 64x64 xc:"hsv($(wl-paste))" /tmp/color.png

# Send a notification using the file as an icon
notify-send "HSV color picked" "hsv($(wl-paste))" -i /tmp/color.png -a "Hyprpicker"

# Remove the temporal file
rm /tmp/color.png

# Exit
exit 0

}



case "$1" in
-rgb)
    check_dependencies
    pick_rgb
    ;;
-hsv)
    check_dependencies
    pick_hsv
    ;;
-hex)
    check_dependencies
    pick_hex
    ;;

*)
    echo "Usage: $0 [-rgb|-hex|-hsv]"
    exit 1
    ;;
esac
