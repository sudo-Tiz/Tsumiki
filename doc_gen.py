import json

from utils.constants import DEFAULT_CONFIG


def type_name(value):
    """Return a string describing the type of a value."""
    if isinstance(value, dict):
        return "object"
    elif isinstance(value, list):
        if len(value) == 0:
            return "list"
        else:
            # show type of first item
            return f"list[{type_name(value[0])}]"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif value is None:
        return "null"
    else:
        return type(value).__name__


def render_md(d, level=0):
    """Recursively render dict to markdown bullet list with type and default value."""
    md = ""
    indent = "  " * level
    if isinstance(d, dict):
        first = True
        for key, value in d.items():
            if level == 0 and not first:
                md += "\n"  # Add a blank line before top-level keys except first
            first = False

            val_type = type_name(value)
            if isinstance(value, dict):
                md += f"{indent}- **`{key}`**: `{val_type}`\n"
                md += render_md(value, level + 1)
            elif (
                isinstance(value, list)
                and len(value) > 0
                and isinstance(value[0], dict)
            ):
                md += f"{indent}- **`{key}`**: `{val_type}`\n"
                # If list of dicts, show example keys from first item
                md += render_md(value[0], level + 1)
            else:
                # Show the value as JSON string for readability
                default_val = json.dumps(value, ensure_ascii=False)
                md += f"{indent}- **`{key}`**: `{val_type}` (default: {default_val})\n"
    else:
        # if not a dict (e.g. list), just show type and example
        val_type = type_name(d)
        default_val = json.dumps(d, ensure_ascii=False)
        md += f"{indent}- `{val_type}`: {default_val}\n"
    return md


def main():
    header = "# Tsumiki Configuration Documentation\n\n"
    body = render_md(DEFAULT_CONFIG)
    content = header + body

    with open("doc.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("doc.md generated successfully.")


if __name__ == "__main__":
    main()
