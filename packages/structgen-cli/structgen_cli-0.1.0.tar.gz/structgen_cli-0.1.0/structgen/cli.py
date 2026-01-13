from pathlib import Path
import sys


def clean_tree_line(line):
    tree_symbols = ["├──", "└──", "│"]
    for symbol in tree_symbols:
        line = line.replace(symbol, "")
    return line.rstrip()


def normalize_lines(lines):
    return [clean_tree_line(line) for line in lines if line.strip()]


def get_level(line):
    spaces = len(line) - len(line.lstrip(" "))
    return spaces // 4


def main():
    print("STRUCTGEN STARTED")
    print("Paste your folder structure below.")
    print("Finish with Ctrl+Z + Enter (Windows) or Ctrl+D (Mac/Linux)\n")

    # Read pasted input from terminal (STDIN)
    raw_lines = sys.stdin.readlines()
    lines = normalize_lines(raw_lines)

    base_path = Path.cwd()
    stack = [base_path]

    print("\nGENERATING STRUCTURE:")

    for line in lines:
        level = get_level(line)
        name = line.strip()

        while len(stack) > level + 1:
            stack.pop()

        current_path = stack[-1] / name.rstrip("/")

        if name.endswith("/"):
            print("Folder:", current_path)
            current_path.mkdir(exist_ok=True)
            stack.append(current_path)
        else:
            print("File:", current_path)
            current_path.touch(exist_ok=True)


if __name__ == "__main__":
    main()
