#!/bin/bash

# Navigate to the $HOME/bar directory
cd "$HOME/bar" || {
		echo -e "\033[31mDirectory $HOME/bar does not exist.\033[0m\n"
		exit 1
	}

# Fetch updates from the remote
git fetch

# Check if there are any changes
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    # If they differ, there are updates
    notify-send "Git Update" "New changes are available in the repository!"
else
    # No changes
    notify-send "Git Update" "The repository is up to date."
fi
