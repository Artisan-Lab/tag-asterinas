import re
import os

cnt = dict()

def init_tags(filepath: str):
    tags = []
    with open(filepath, "r") as f:
        for line in f.readlines():
            match = re.match(r"^\[tag\.(.+?)\]$", line.strip())
            if match:
                tags.append(match.group(1))
    for tag in tags:
        cnt[tag] = 0

def count_rust_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    pattern_multiline = r'#\[safety\s*\{\s*((?:\w+\([^)]*\)\s*,\s*)*\w+\([^)]*\))\s*(?::\s*"[^"]*")?\s*\}\s*\]'
    matches = re.findall(pattern_multiline, content, re.DOTALL)
    if matches:
        for match in matches:
            tags = re.findall(r'(\w+)\([^)]*\)', match)
            for tag in tags:
                if tag not in cnt:
                    print(f"Error! Invalid tag: {tag}.")
                else:
                    cnt[tag] += 1

def count_rust_files(directory: str):
    rust_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.rs'):
                full_path = os.path.join(root, file)
                rust_files.append(full_path)
    for file in rust_files:
        count_rust_file(file)


if __name__ == "__main__":
    init_tags(r"/home/calvin/Desktop/tag-asterinas/ostd/safety-tags.toml")
    count_rust_files(r"/home/calvin/Desktop/tag-asterinas/ostd/src")
    print(cnt)
    