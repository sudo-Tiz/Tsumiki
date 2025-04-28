# justfile

# Command to freeze current pip packages to requirements.txt
freeze:
    pip freeze > requirements.txt

config:
    cp config.json.bak config.json
