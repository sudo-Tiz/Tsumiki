#!/bin/bash
# shellcheck source=/dev/null

set -e          # Exit immediately if a command exits with a non-zero status
set -u          # Treat unset variables as an error
set -o pipefail # Prevent errors in a pipeline from being masked

if ! grep -q "arch" /etc/os-release; then
	echo "This script is designed to run on Arch Linux."
	exit 1
fi

INSTALL_DIR=$(dirname -- "$0")

setup_venv() {
	# Navigate to the $INSTALL_DIR directory
	cd "$INSTALL_DIR" || {
		printf "\033[31mDirectory %s does not exist.\033[0m\n" "$INSTALL_DIR" >&2
		exit 1
	}

	# Check if the virtual environment exists, if not, create it
	if [ ! -d .venv ]; then
		echo -e "\033[32m  venv does not exist. Creating venv...\033[0m\n"
		if ! python3 -m venv .venv; then
			printf "\033[31m  Failed to create virtual environment. Exiting...\033[0m\n" >&2
			exit 1
		fi

		printf "\033[32m  Virtual environment created successfully.\033[0m\n"
	else
		printf "\033[33m  Virtual environment already exists.\033[0m\n"
	fi

	# Activate virtual environment
	source .venv/bin/activate

	if ! source .venv/bin/activate; then
		printf "\033[31m  Failed to activate venv. Exiting...\033[0m\n" >&2
		exit 1
	fi
	fi

	# Install Python dependencies
	echo -e "\033[32m  Installing python dependencies, brace yourself.\033[0m\n"
	pip install -r requirements.txt

	if [ $? -ne 0 ]; then
		echo -e "\033[31mFailed to install packages from requirements.txt. Exiting...\033[0m\n"
		deactivate
		exit 1
	fi

	echo -e "\033[32m  Python dependencies installed successfully.\033[0m\n"
	deactivate
}

start_bar() {
	# Navigate to the $INSTALL_DIR directory
	cd "$INSTALL_DIR" || {
		echo -e "\033[31mDirectory $INSTALL_DIR does not exist.\033[0m\n"
		exit 1
	}

	VERSION=$(git describe --tags --abbrev=0)

	# Check if the virtual environment exists, if not, create it
	if [ ! -d .venv ]; then
		echo -e "\033[32m  venv does not exist. Creating venv...\033[0m\n"
		python3 -m venv .venv

		if [ $? -ne 0 ]; then
			echo -e "\033[31m  Failed to create virtual environment. Exiting...\033[0m\n"
			exit 1
		fi

		source .venv/bin/activate

		if [ $? -ne 0 ]; then
			echo -e "\033[31m  Failed to activate venv. Exiting...\033[0m\n"
			exit 1
		fi

		echo -e "\033[32m  Installing python dependencies, brace yourself.\033[0m\n"
		pip install -r requirements.txt

		if [ $? -ne 0 ]; then
			echo -e "\033[31mFailed to install packages from requirements.txt. Exiting...\033[0m\n"
			exit 1
		fi
		echo -e "\033[32m  All done, starting bar.\033[0m\n"
	else
		echo -e "\033[32m  Using existing venv.\033[0m\n"
		source .venv/bin/activate
	fi

	cat <<EOF


████████╗███████╗██╗   ██╗███╗   ███╗██╗██╗  ██╗██╗
╚══██╔══╝██╔════╝██║   ██║████╗ ████║██║██║ ██╔╝██║
   ██║   ███████╗██║   ██║██╔████╔██║██║█████╔╝ ██║
   ██║   ╚════██║██║   ██║██║╚██╔╝██║██║██╔═██╗ ██║
   ██║   ███████║╚██████╔╝██║ ╚═╝ ██║██║██║  ██╗██║
   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝

version:	$VERSION


EOF
	echo -e "\e[32mUsing python:\e[0m \e[34m$(which python)\e[0m\n"
	python3 main.py
	deactivate
}

install_packages() {

	echo "								  "
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣷⣤⣙⢻⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⡿⠛⠛⠿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⠿⣆⠀⠀⠀⠀"
	echo "⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀"
	echo "⠀⢀⣾⣿⣿⠿⠟⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠻⠿⣿⣿⣷⡀⠀"
	echo "⣠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣄"
	echo "								  "

	# Notify user about the installation process
	echo -e "\e[1;34mInstalling the pre-requisites, may take a while....\e[0m\n"

	# Install packages using pacman
	pacman_deps=(
		pipewire
		playerctl
		dart-sass
		networkmanager
		brightnessctl
		power-profiles-daemon
		pkgconf
		wf-recorder
		kitty
		libnotify
		python
		pacman-contrib
		gtk3
		cairo
		gtk-layer-shell
		libgirepository
		gobject-introspection
		gobject-introspection-runtime
		python-pip
		python-gobject
		python-psutil
		python-cairo
		python-loguru
		python-requests
		python-setproctitle
		cliphist
		noto-fonts-emoji
		satty
	)

		aur_deps=(
		gray-git
		python-fabric-git
		gnome-bluetooth-3.0
		python-rlottie-python
		python-pytomlpp
		python-pyjson5
		python-ijson
		slurp
		imagemagick
		tesseract
		tesseract-data-eng
		ttf-jetbrains-mono-nerd
		grimblast-git
	)


	sudo pacman -S --noconfirm --needed "${pacman_deps[@]}"  || true

	if command -v yay &>/dev/null; then
		aur_helper="yay"
	elif command -v paru &>/dev/null; then
		aur_helper="paru"
	else
		echo -e "\033[33myay or paru not found. Install the aur packages \033[36mgray-git \033[36mpython-fabric \033[33mwith the aur helper installed.\033[0m\n"
		exit 1
	fi

	if command -v paru &>/dev/null; then
		aur_helper="paru"
	else
		aur_helper="yay"
	fi

	# Install packages using yay (AUR helper)

	$aur_helper -S --noconfirm --needed "${aur_deps[@]}"  || true

}

# Check the argument passed to the script and call the appropriate function
case "$1" in
-start)
	start_bar # Call the start_bar function
	;;
-update)
	git pull origin master # Placeholder for the update functionality
	;;
-install)
	install_packages # Call the install_packages function
	;;
-setup)
	setup_venv # Call the setup_venv function
	;;
-install-setup)
	install_packages # Install packages first
	setup_venv # Then setup virtual environment
	;;
*)
	echo -e "\033[31mUnknown command. Available options:\033[0m"
	echo -e "\033[32m  -start\033[0m         Start the bar"
	echo -e "\033[32m  -update\033[0m        Update from git"
	echo -e "\033[32m  -install\033[0m       Install system packages only"
	echo -e "\033[32m  -setup\033[0m         Setup virtual environment and Python dependencies only"
	echo -e "\033[32m  -install-setup\033[0m Install packages and setup virtual environment"
	exit 1
	;;
esac
