import os
import sys
import shutil
import time
from datetime import datetime

from nl2cmd.rule_engine import rule_match
from nl2cmd.infer import ml_translate
from nl2cmd.safety import safe


def parse_canonical(canonical: str):
    parts = canonical.split()
    cmd = parts[0]
    args = {}

    for p in parts[1:]:
        if "=" in p:
            k, v = p.split("=", 1)
            args[k] = v

    return cmd, args

def resolve_intent(intent: str, text: str):
    """
    Maps ML-predicted intent to safe canonical commands.
    ML decides WHAT the user wants.
    Deterministic logic decides HOW it is executed.
    """

    # -----------------------------
    # FILE LISTING
    # -----------------------------
    if intent == "LIST_FILES":
        return "LIST_FILES"

    if intent == "LIST_FILES_LONG":
        return "LIST_FILES_LONG"

    if intent == "SHOW_HIDDEN":
        return "SHOW_HIDDEN"

    # -----------------------------
    # DIRECTORY INFORMATION
    # -----------------------------
    if intent == "PRINT_CWD":
        return "PRINT_CWD"

    if intent == "TREE":
        return "TREE"

    if intent == "COUNT_FILES":
        return "COUNT_FILES"

    # -----------------------------
    # FILE / DIRECTORY CREATION
    # -----------------------------
    if intent == "MAKE_DIR":
        # ML should not guess folder names
        return None

    if intent == "CREATE_FILE":
        # ML should not guess file names
        return None

    # -----------------------------
    # FILE / DIRECTORY DELETION
    # -----------------------------
    if intent == "DELETE_FILE":
        # Dangerous without explicit path
        return None

    if intent == "DELETE_DIR":
        return None

    if intent == "DELETE_DIR_RECURSIVE":
        return None

    # -----------------------------
    # FILE MANIPULATION
    # -----------------------------
    if intent == "COPY_FILE":
        return None

    if intent == "MOVE_FILE":
        return None

    if intent == "RENAME_FILE":
        return None

    # -----------------------------
    # SEARCH / INSPECTION
    # -----------------------------
    if intent == "FILE_INFO":
        return None

    if intent == "READ_FILE":
        return None

    if intent == "FIND_BY_NAME":
        return None

    if intent == "SEARCH_TEXT":
        # Text argument unknown → safe placeholder
        return "SEARCH_TEXT text=UNKNOWN"

    if intent == "FIND_LARGE":
        # Size must be explicit
        return None

    if intent == "FIND_RECENT":
        # Safe default: last 7 days
        return "FIND_RECENT days=7"

    # -----------------------------
    # ARCHIVING
    # -----------------------------
    if intent == "ZIP":
        return None

    if intent == "UNZIP":
        return None

    # -----------------------------
    # SYSTEM INFO
    # -----------------------------
    if intent == "DISK_USAGE":
        return "DISK_USAGE"

    if intent == "SHOW_DATE":
        return "SHOW_DATE"

    # -----------------------------
    # ML-ONLY HIGH-LEVEL INTENTS
    # -----------------------------
    if intent == "CLEANUP":
        # Conservative cleanup
        return "CLEAR_DIR path=."

    # -----------------------------
    # FALLBACK
    # -----------------------------
    return None

def execute(cmd, args):
    # -----------------------------
    # FILE LISTING
    # -----------------------------
    if cmd == "LIST_FILES":
        print("\n".join(os.listdir(".")))

    elif cmd == "LIST_FILES_LONG":
        for f in os.listdir("."):
            if os.path.isfile(f):
                print(f"{f}\t{os.path.getsize(f)} bytes")

    elif cmd == "SHOW_HIDDEN":
        print("\n".join(f for f in os.listdir(".") if f.startswith(".")))

    # -----------------------------
    # DIRECTORY
    # -----------------------------
    elif cmd == "PRINT_CWD":
        print(os.getcwd())

    elif cmd == "CHANGE_DIR":
        os.chdir(args["path"])
        print(f"Changed directory to {os.getcwd()}")

    elif cmd == "MAKE_DIR":
        os.makedirs(args["name"], exist_ok=True)
        print(f"Folder created: {args['name']}")
    
    elif cmd == "DELETE_DIR":
        path = args["path"]

        if not os.path.isdir(path):
            print(f"❌ Not a directory: {path}")
            return

        # Only delete empty directories (SAFE)
        if os.listdir(path):
            print(f"❌ Directory not empty: {path}")
            print("Refusing to delete non-empty directory")
            return

        os.rmdir(path)
        print(f"Directory deleted: {path}")

    elif cmd == "DELETE_DIR_RECURSIVE":
        path = args["path"]
        shutil.rmtree(path)
        print(f"Directory recursively deleted: {path}")

    # -----------------------------
    # FILE OPERATIONS
    # -----------------------------
    elif cmd == "CREATE_FILE":
        directory = args["dir"]
        name = args["name"]
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, name)
        open(path, "w").close()
        print(f"File created: {path}")

    elif cmd == "DELETE_FILE":
        os.remove(args["name"])
        print(f"File deleted: {args['name']}")

    elif cmd == "RENAME_FILE":
        os.rename(args["src"], args["dst"])
        print(f"Renamed {args['src']} → {args['dst']}")

    elif cmd == "COPY_FILE":
        shutil.copy(args["src"], args["dst"])
        print(f"Copied {args['src']} → {args['dst']}")

    elif cmd == "MOVE_FILE":
        shutil.move(args["src"], args["dst"])
        print(f"Moved {args['src']} → {args['dst']}")

    # -----------------------------
    # SEARCH / INFO
    # -----------------------------
    elif cmd == "FIND_LARGE":
        size = args["size"]
        limit = int(size[:-2]) * (1024 ** (2 if size.endswith("MB") else 3))
        for f in os.listdir("."):
            if os.path.isfile(f) and os.path.getsize(f) > limit:
                print(f)

    elif cmd == "FIND_BY_NAME":
        pattern = args["name"].replace("*", "")
        for f in os.listdir("."):
            if pattern in f:
                print(f)

    elif cmd == "FILE_INFO":
        path = args["path"]
        if not os.path.exists(path):
            print("❌ File not found")
            return

        stat = os.stat(path)
        print(f"Path: {path}")
        print(f"Size: {stat.st_size} bytes")
        print(f"Last modified: {datetime.fromtimestamp(stat.st_mtime)}")

    elif cmd == "READ_FILE":
        path = args["path"]
        lines = int(args["lines"])

        with open(path, "r", errors="ignore") as f:
            for i in range(lines):
                line = f.readline()
                if not line:
                    break
                print(line.rstrip())

    elif cmd == "TREE":
        for root, dirs, files in os.walk("."):
            level = root.count(os.sep)
            indent = " " * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            for f in files:
                print(f"{indent}  {f}")

    elif cmd == "FIND_RECENT":
        days = int(args["days"])
        cutoff = time.time() - days * 86400

        for f in os.listdir("."):
            if os.path.isfile(f) and os.path.getmtime(f) >= cutoff:
                print(f)

    elif cmd == "ZIP":
        shutil.make_archive(args["path"], "zip", args["path"])
        print("Archive created")

    elif cmd == "UNZIP":
        shutil.unpack_archive(args["file"])
        print("Archive extracted")

    elif cmd == "DISK_USAGE":
        total, used, free = shutil.disk_usage(".")
        print(f"Used: {used // (1024**2)} MB")
        print(f"Free: {free // (1024**2)} MB")

    elif cmd == "COUNT_FILES":
        print(len(os.listdir(".")))

    elif cmd == "SHOW_DATE":
        print(datetime.now().strftime("%Y-%m-%d"))

    else:
        print("❌ Unsupported command")


def main():
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("ask> ")

    # 1. Try rule-based parsing first
    canonical = rule_match(text)
    source = "rule-based"

    # 2. Fall back to ML if rules fail
    if canonical is None:
        ml_out = ml_translate(text)
        source = "ml"

        if ml_out and ml_out.startswith("INTENT="):
            intent = ml_out.split("=", 1)[1]
            canonical = resolve_intent(intent, text)

    # 3. If still nothing, give up safely
    if canonical is None:
        print("❌ Could not understand request")
        return

    print(f"Source: {source}")
    print(f"Canonical: {canonical}")

    # 4. Safety check
    if not safe(canonical):
        print("❌ Blocked for safety")
        return

    # 5. Confirmation
    if input("Execute? [y/N]: ").lower() != "y":
        return

    # 6. Execute
    cmd, args = parse_canonical(canonical)
    execute(cmd, args)


if __name__ == "__main__":
    main()
