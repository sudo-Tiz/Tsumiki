# justfile

# Command to freeze current pip packages to requirements.txt
freeze:
    pip freeze > requirements.txt

copy_config:
    cp config.json config.json.bak

restore_config:
    cp config.json.bak config.json
    rm config.json.bak
