
def extract_title(markdown):    
    blocks = markdown.splitlines()
    title = ""
    found = False
    for block in blocks:
        if len(block) > 1 and block[0] == "#" and block[1] == " ":
            title = block
            found = True
            title = title[1:].strip()
            return title
    if not found:
        raise Exception("Title not found")
    
    

