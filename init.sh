#!/bin/bash
# shellcheck source=/dev/null

start_bar() {
	# Navigate to the $HOME/bar directory
	cd "$HOME/bar" || {
		echo "Directory $HOME/bar does not exist."
		exit 1
	}

	# Check if the virtual environment exists, if not, create it
	if [ ! -d .venv ]; then
		echo -e "\033[32mvenv does not exist. Creating venv...\033[0m"
		python3 -m venv .venv

		if [ $? -ne 0 ]; then
			echo -e "\033[31mFailed to create virtual environment. Exiting...\033[0m"
			exit 1
		fi

		source .venv/bin/activate

		# Install required Python packages
		pip install -r requirements.txt

		if [ $? -ne 0 ]; then
			echo -e "\033[31mFailed to install packages from requirements.txt. Exiting...\033[0m"
			exit 1
		fi
	fi

	cat <<EOF


██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗  █████╗ ███╗   ██╗███████╗██╗
██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║
███████║ ╚████╔╝ ██║  ██║█████╗  ██████╔╝███████║██╔██╗ ██║█████╗  ██║
██╔══██║  ╚██╔╝  ██║  ██║██╔══╝  ██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ██║
██║  ██║   ██║   ██████╔╝███████╗██║     ██║  ██║██║ ╚████║███████╗███████╗
╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝


EOF

	pkill dunst; pkill mako; # to use notifications, kill other notification daemons
	python3 ./main.py
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
	echo -e "\e[1;34mInstalling the pre-requisites, may take a while....\e[0m"

	# Install packages using pacman
	sudo pacman -S --noconfirm pipewire playerctl dart-sass networkmanager wl-clipboard brightnessctl python pacman-contrib gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python-pip python-gobject python-psutil python-cairo python-loguru python-setproctitle pkgconf wf-recorder kitty grimblast gnome-bluetooth


	if command -v yay &> /dev/null; then
		aur_helper="yay"
	elif command -v paru &> /dev/null; then
		aur_helper="paru"
	else
		echo -e "\033[33myay or paru not found. Install the aur packages \033[36mgray-git \033[36mpython-fabric \033[33mwith the aur helper installed.\033[0m"
		exit 1
	fi

	# Install packages using yay (AUR helper)
	$aur_helper -S --noconfirm gray-git python-fabric
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
*)
	echo -e "\033[31mUnknown command. Use \033[32m'-start'\033[33m, \033[32m'-update'\033[33m, \033[32m'-install'\033[31m.\033[0m"
	exit 1
	;;
esac
