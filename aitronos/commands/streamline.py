import os


def create_project_structure(project_name):
    project_structure = {
        "src/main/": "",
        "src/test/": "",
        "resources/": "",
        "requirements.txt": "",
        "config.freddy": "",
        "knowledge.json": "",
        "knowledge.py": "",
        "documentation.txt": "",
        "execution_log.json": ""
    }
    try:
        for path, content in project_structure.items():
            full_path = os.path.join(project_name, path)
            if path.endswith("/"):
                os.makedirs(full_path, exist_ok=True)
            else:
                with open(full_path, 'w') as f:
                    f.write(content)
        print(f"Project '{project_name}' created successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

def handle_streamLine_command(args):
    if len(args) < 1:
        print("Usage: aitronos streamLine init <project_name>")
        return

    subcommand = args[0]

    if subcommand == "init":
        if len(args) < 2:
            print("Please provide a project name.")
        else:
            create_project_structure(args[1])
    else:
        print(f"Unknown subcommand: {subcommand}")