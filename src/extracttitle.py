def extract_title(markdown):
    lines = markdown.split("\n")
    text = None
    h1_found = False
    for line in lines:
        line = line.lstrip()
        if line.startswith("#"):
            if line.startswith("##"):
                continue
            h1_found = True
            text = line[1:].rstrip()
            text = text.lstrip()
            break
        else:
            continue

    if not h1_found:
        raise Exception("No title found in markdown")
    return text
