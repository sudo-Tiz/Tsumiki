#! /bin/sh
cd $HOME/bar
if [ ! -d .venv ]; then
  echo "venv does not exist. Creating venv..."
  python3 -m venv .venv
  pip install -r requirements.txt
fi
source .venv/bin/activate
python3 main.py
