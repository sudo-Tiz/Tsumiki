#!/bin/bash

# Word of caution: changing this can break update module, be vigilant

# Parse arguments
DISTRO=""
DO_UPDATE=0
CHECK_FLATPAK=0

check_flatpak_updates() {
    local count=0
    if [[ "$CHECK_FLATPAK" -eq 1 && "$(command -v flatpak)" ]]; then
        count=$(flatpak remote-ls --updates 2>/dev/null | wc -l)
    fi
    echo "$count"
}

run_flatpak_update() {
    if [[ "$CHECK_FLATPAK" -eq 1 && "$(command -v flatpak)" ]]; then
        flatpak update -y || true
    fi
}



check_arch_updates() {
    official_updates=0
    aur_updates=0
    tooltip=""

    official_updates=$(checkupdates 2>/dev/null | wc -l)

    if command -v paru &> /dev/null; then
        aur_helper="paru"
    else
        aur_helper="yay"
    fi

    aur_updates=$($aur_helper -Qum 2>/dev/null | wc -l)

    tooltip="󰣇 Official $official_updates\n󰮯 AUR $aur_updates"
    flatpak_updates=0

    if [[ "$CHECK_FLATPAK" -eq 1 ]]; then
        flatpak_updates=$(check_flatpak_updates)
        tooltip="$tooltip\n Flatpak $flatpak_updates"
    fi


    total_updates=$((official_updates + aur_updates + flatpak_updates))

    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}



check_ubuntu_updates() {
    official_updates=$(apt-get -s -o Debug::NoLocking=true upgrade | grep -c ^Inst)
    flatpak_updates=$(check_flatpak_updates)

    tooltip="󰕈 Official $official_updates"
    [[ "$CHECK_FLATPAK" -eq 1 ]] && tooltip="$tooltip\n Flatpak $flatpak_updates"

    total_updates=$((official_updates + flatpak_updates))
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}

check_fedora_updates() {
    official_updates=$(dnf check-update -q | grep -v '^Loaded plugins' | grep -v '^No match for' | wc -l)
    flatpak_updates=$(check_flatpak_updates)

    tooltip="󰣛 Official $official_updates"
    [[ "$CHECK_FLATPAK" -eq 1 ]] && tooltip="$tooltip\n Flatpak $flatpak_updates"

    total_updates=$((official_updates + flatpak_updates))
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}

check_opensuse_updates() {
    official_updates=$(zypper lu | wc -l)
    flatpak_updates=$(check_flatpak_updates)

    tooltip=" Official $official_updates"
    [[ "$CHECK_FLATPAK" -eq 1 ]] && tooltip="$tooltip\n Flatpak $flatpak_updates"

    total_updates=$((official_updates + flatpak_updates))
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}



update_arch() {
    if command -v paru &> /dev/null; then
		aur_helper="paru"
	else
		aur_helper="yay"
	fi
    command="
    # Display Arch Linux ASCII Art
    echo '        _      _   _       __   __     _       '
    echo '       / \\    / \\  | |     /  \\ /  \\   | |      '
    echo '      /   \\  /   \\ | |    /    \\    \\ | |       '
    echo '     /     \\/     \\| |   /      \\    \\| |      '
    echo '    |  ARCH LINUX   | |  |  LINUX   \\___| '
    echo '      \\    /  | | /    \\       '
    echo '                                  '
    echo '          A R C H LINUX   '
    echo '                                  '
    echo '                                  '
    echo '                                  '


    $aur_helper -Syyu
    flatpak update -y || true
    read -n 1 -p 'Press any key to continue...'
    "
    kitty --title systemupdate sh -c "${command}"
    echo "{\"total\":\"0\", \"tooltip\":\"0\"}"
}


update_ubuntu() {
    command="
    sudo apt upgrade -y
    flatpak update -y || true
    read -n 1 -p 'Press any key to continue...'
    "
    kitty --title systemupdate sh -c "${command}"
    echo "{\"total\":\"0\", \"tooltip\":\"0\"}"
}


update_fedora() {
    command="
    sudo dnf upgrade --assumeyes
    flatpak update -y || true
    read -n 1 -p 'Press any key to continue...'
    "
    kitty --title systemupdate sh -c "${command}"
    echo "{\"total\":\"0\", \"tooltip\":\"0\"}"
}

update_opensuse() {
    command="
    sudo zypper update -y
    flatpak update -y || true
    read -n 1 -p 'Press any key to continue...'
    "
    kitty --title systemupdate sh -c "${command}"
    echo "{\"total\":\"0\", \"tooltip\":\"0\"}"
}





for arg in "$@"; do
    case "$arg" in
        --arch)   DISTRO="arch" ;;
        --ubuntu) DISTRO="ubuntu" ;;
        --fedora) DISTRO="fedora" ;;
        --suse)   DISTRO="suse" ;;
         --flatpak)   CHECK_FLATPAK=1 ;;
        up)       DO_UPDATE=1 ;;
        *)
            echo "Usage: $0 [--arch|--ubuntu|--fedora|--suse]  [--flatpak] [up (optional)]"
            exit 1
            ;;
    esac
done

# Run appropriate action
case "$DISTRO" in
    arch)   (( DO_UPDATE )) && update_arch        || check_arch_updates ;;
    ubuntu) (( DO_UPDATE )) && update_ubuntu      || check_ubuntu_updates ;;
    fedora) (( DO_UPDATE )) && update_fedora      || check_fedora_updates ;;
    suse)   (( DO_UPDATE )) && update_opensuse    || check_opensuse_updates ;;
    *)
        echo "Usage: $0 [--arch|--ubuntu|--fedora|--suse] [--flatpak] [up (optional)]"
        exit 1
        ;;
esac
