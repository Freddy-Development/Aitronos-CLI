import sys
import re
import os
import subprocess

# Get the absolute path to the setup.py file
SETUP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../setup.py')
REPO = 'Freddy-Development/Aitronos-CLI'  # Replace with your GitHub repo


def read_version():
    """Reads the current version from setup.py."""
    with open(SETUP_FILE, 'r') as f:
        for line in f:
            match = re.search(r"version='([0-9]+\.[0-9]+\.[0-9]+)'", line)
            if match:
                return match.group(1)
    raise ValueError("Version not found in setup.py")

def write_version(new_version):
    """Writes the updated version to setup.py."""
    with open(SETUP_FILE, 'r') as f:
        setup_content = f.read()

    new_setup_content = re.sub(
        r"version='[0-9]+\.[0-9]+\.[0-9]+'",
        f"version='{new_version}'",
        setup_content
    )

    with open(SETUP_FILE, 'w') as f:
        f.write(new_setup_content)

def increment_version(version, part):
    """Increments the specified part of the version."""
    major, minor, patch = map(int, version.split('.'))

    if part == 'patch':
        patch += 1
    elif part == 'minor':
        minor += 1
        patch = 0  # Reset patch to 0 when minor is incremented
    elif part == 'major':
        major += 1
        minor = 0  # Reset minor and patch when major is incremented
        patch = 0
    else:
        raise ValueError("Invalid version part. Use 'patch', 'minor', or 'major'.")

    return f"{major}.{minor}.{patch}"

def create_git_tag(version):
    """Creates a git tag and pushes it to GitHub."""
    subprocess.run(["git", "add", SETUP_FILE], check=True)
    subprocess.run(["git", "commit", "-m", f"Bump version to {version}"], check=True)
    subprocess.run(["git", "push"], check=True)
    subprocess.run(["git", "tag", f"v{version}"], check=True)
    subprocess.run(["git", "push", "origin", f"v{version}"], check=True)
    print(f"Created git tag v{version}")

def create_github_release(version):
    """Creates a GitHub release for the given version using GitHub CLI."""
    subprocess.run(["gh", "release", "create", f"v{version}", "--title", f"v{version}", "--notes", f"Release v{version}"], check=True)
    print(f"Created GitHub release for v{version}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 update_version.py [patch|minor|major]")
        sys.exit(1)

    part = sys.argv[1]
    current_version = read_version()
    new_version = increment_version(current_version, part)

    # Step 1: Update version in setup.py
    write_version(new_version)
    print(f"Version updated to {new_version}")

    # Step 2: Commit and push the new version, create a git tag
    create_git_tag(new_version)

    # Step 3: Create a new GitHub release
    create_github_release(new_version)

# example usage:
# python3 update_version.py patch
# python3 update_version.py minor
# python3 update_version.py major
