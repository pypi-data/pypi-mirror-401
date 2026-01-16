def format_whitespace(text):
    lines = text.splitlines()
    cleaned_lines = []
    empty_block = False

    for line in lines:
        stripped = line.rstrip()

        if not stripped:
            if not empty_block:
                cleaned_lines.append("")
                empty_block = True
        else:
            cleaned_lines.append(stripped)
            empty_block = False

    return "\n".join(cleaned_lines).strip() + "\n"
