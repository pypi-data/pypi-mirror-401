import re

def rule_match(text: str):
    t = text.lower().strip()

    # -----------------------------
    # FIND RECENT FILES
    # -----------------------------
    m = re.search(r"(modified|changed).*last\s+(\d+)\s+days?", t)
    if m:
        return f"FIND_RECENT days={m.group(2)}"

    # -----------------------------
    # LIST FILES
    # -----------------------------
    if any(w in t for w in ["list", "show", "display"]) and "file" in t:
        if any(w in t for w in ["detail", "long", "permission", "size"]):
            return "LIST_FILES_LONG"
        if "hidden" in t or "dot" in t:
            return "SHOW_HIDDEN"
        return "LIST_FILES"

    # -----------------------------
    # CURRENT DIRECTORY
    # -----------------------------
    if any(p in t for p in [
        "where am i",
        "current directory",
        "working directory",
        "current folder",
        "my location"
    ]):
        return "PRINT_CWD"

    # -----------------------------
    # CHANGE DIRECTORY
    # -----------------------------
    m = re.search(r"(go to|change directory to|navigate to|move to)\s+(.+)", t)
    if m:
        return f"CHANGE_DIR path={m.group(2)}"

    # -----------------------------
    # CREATE DIRECTORY
    # -----------------------------
    m = re.search(r"(create|make|add).*?(folder|directory)\s+(\w+)", t)
    if m:
        return f"MAKE_DIR name={m.group(3)}"
    
    # -----------------------------
    # DELETE DIRECTORY / FOLDER
    # -----------------------------
    m = re.search(r"(delete|remove|erase)\s+(folder|directory)\s+(.+)", t)
    if m:
        return f"DELETE_DIR path={m.group(3).strip()}"

    # RECURSIVE DELETE DIRECTORY
    m = re.search(r"(delete|remove)\s+(entire|recursive)\s+(folder|directory)\s+(.+)", t)
    if m:
        return f"DELETE_DIR_RECURSIVE path={m.group(4).strip()}"

    # -----------------------------
    # CREATE FILE IN DIRECTORY
    # -----------------------------
    m = re.search(r"(create|make).*file\s+(\S+)\s+(in|inside)\s+(\S+)", t)
    if m:
        return f"CREATE_FILE name={m.group(2)} dir={m.group(4)}"

    # CREATE FILE (current dir)
    m = re.search(r"(create|make).*file\s+(\S+)", t)
    if m:
        return f"CREATE_FILE name={m.group(2)} dir=."

    # -----------------------------
    # RENAME FILE (WITH DESTINATION)
    # -----------------------------
    m = re.search(r"(rename|change name of)\s+(\S+)\s+to\s+(\S+)", t)
    if m:
        return f"RENAME_FILE src={m.group(2)} dst={m.group(3)}"

    # -----------------------------
    # DELETE FILE
    # -----------------------------
    m = re.search(r"(delete|remove|erase)\s+(.+)", t)
    if m:
        return f"DELETE_FILE name={m.group(2).strip()}"


    # -----------------------------
    # COPY FILE
    # -----------------------------
    m = re.search(r"(copy|duplicate).*file\s+(\S+)\s+to\s+(\S+)", t)
    if m:
        return f"COPY_FILE src={m.group(2)} dst={m.group(3)}"

    # -----------------------------
    # MOVE FILE
    # -----------------------------
    m = re.search(r"(move|relocate).*file\s+(\S+)\s+to\s+(\S+)", t)
    if m:
        return f"MOVE_FILE src={m.group(2)} dst={m.group(3)}"

    # -----------------------------
    # FIND LARGE FILES
    # -----------------------------
    m = re.search(r"(larger|bigger|greater).*than\s+(\d+)\s*(mb|gb)", t)
    if m:
        size = m.group(2) + m.group(3).upper()
        return f"FIND_LARGE size={size}"

    # -----------------------------
    # FIND BY NAME / PATTERN
    # -----------------------------
    m = re.search(r"(find|search|locate).*?(named|matching)?\s*(\*\.\w+)", t)
    if m:
        return f"FIND_BY_NAME name={m.group(3)}"
    
    # FIND FILES WITH EXACT NAME
    m = re.search(r"(find|search|locate)\s+(\S+\.\w+)", t)
    if m:
        return f"FIND_BY_NAME name={m.group(2)}"

    # -----------------------------
    # FILE INFO
    # -----------------------------
    m = re.search(r"(show|get|display).*(info|details).*?(?:of\s+)?(.+)", t)
    if m:
        return f"FILE_INFO path={m.group(3).strip()}"

    # -----------------------------
    # READ FIRST N LINES
    # -----------------------------
    m = re.search(r"(show|read|preview).*?(\d+)\s*lines?.*?(?:of\s+)?(.+)", t)
    if m:
        return f"READ_FILE path={m.group(3).strip()} lines={m.group(2)}"
    
    # -----------------------------
    # ZIP & UNZIP
    # -----------------------------
    # ZIP
    m = re.search(r"(zip|compress)\s+(.+)", t)
    if m:
        return f"ZIP path={m.group(2).strip()}"

    # UNZIP
    m = re.search(r"(unzip|extract)\s+(.+)", t)
    if m:
        return f"UNZIP file={m.group(2).strip()}"


    # -----------------------------
    # DIRECTORY TREE
    # -----------------------------
    if "tree" in t or "folder structure" in t:
        return "TREE"

    # -----------------------------
    # DISK USAGE
    # -----------------------------
    if any(w in t for w in ["disk usage", "disk space", "space left", "storage usage"]):
        return "DISK_USAGE"

    # -----------------------------
    # COUNT FILES
    # -----------------------------
    if any(w in t for w in ["count files", "number of files", "how many files"]):
        return "COUNT_FILES"

    # -----------------------------
    # SHOW DATE
    # -----------------------------
    if any(w in t for w in ["today's date", "current date", "show date"]):
        return "SHOW_DATE"

    return None
