import re


def extract_markdown_images(text):
    #this will take raw markdown text and return a list of tuples
    # each tuple will contain alt text and URL of any markdown images
    extracted = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted

def extract_markdown_links(text):
    #similar to extract_markdown_images except it extracts links not images
    # returns a tuples of anchor text and urls
    extracted = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted
