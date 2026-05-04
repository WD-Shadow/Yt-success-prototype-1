from datetime import datetime

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_output(content):
    with open("output/results.txt", "w", encoding="utf-8") as f:
        f.write(content)

def generate():
    hooks = load_file("prompts/hooks.txt")
    scripts = load_file("prompts/scripts.txt")
    titles = load_file("prompts/titles.txt")

    output = f"""
Generated: {datetime.now()}

--- HOOK RULES ---
{hooks}

--- SCRIPT RULES ---
{scripts}

--- TITLE RULES ---
{titles}

--- FORMAT ---
Idea 1:
Hook:
Script:
Title:
"""

    save_output(output)
    print("Saved to output/results.txt")

if __name__ == "__main__":
    generate()
