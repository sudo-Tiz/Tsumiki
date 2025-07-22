# justfile

# Command to freeze current pip packages to requirements.txt
freeze:
    pip freeze > requirements.txt

doc_gen:
    python doc_gen.py

restore_config:
    cp config.json.bak config.json

