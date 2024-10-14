import sys
import re
import os
import subprocess

# Get the absolute path to the setup.py file
SETUP_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'setup.py')
FORMULA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'homebrew', 'Formula', 'aitronos.rb')
REPO = 'yourusername/aitronos-cli'  # Replace with your GitHub repo
FORMULA_REPO = 'yourusername/homebrew-aitronos-cli'  # Replace with your Homebrew tap repo

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
    subprocess.run(["git", "tag", f"v{version}"], check=True)
    subprocess.run(["git", "push", "origin", f"v{version}"], check=True)
    print(f"Created git tag v{version}")

def create_github_release(version):
    """Creates a GitHub release for the given version using GitHub CLI."""
    subprocess.run(["gh", "release", "create", f"v{version}", "--title", f"v{version}", "--notes", f"Release v{version}"], check=True)
    print(f"Created GitHub release for v{version}")

def download_tarball(version):
    """Downloads the release tarball from GitHub."""
    tar_filename = f"v{version}.tar.gz"
    url = f"https://github.com/{REPO}/archive/refs/tags/v{version}.tar.gz"
    subprocess.run(["curl", "-L", "-o", tar_filename, url], check=True)
    return tar_filename

def generate_sha256(tar_filename):
    """Generates SHA256 hash for the tarball."""
    result = subprocess.run(["shasum", "-a", "256", tar_filename], check=True, stdout=subprocess.PIPE)
    sha256 = result.stdout.split()[0].decode('utf-8')
    print(f"Generated SHA256: {sha256}")
    return sha256

def update_homebrew_formula(version, sha256):
    """Updates the Homebrew formula with the new version and SHA256 hash."""
    with open(FORMULA_PATH, 'r') as f:
        formula_content = f.read()

    new_formula_content = re.sub(r"url \".*\"", f'url "https://github.com/{REPO}/archive/v{version}.tar.gz"', formula_content)
    new_formula_content = re.sub(r"sha256 \".*\"", f'sha256 "{sha256}"', new_formula_content)

    with open(FORMULA_PATH, 'w') as f:
        f.write(new_formula_content)

    print(f"Updated Homebrew formula for v{version}")

def commit_and_push_formula(version):
    """Commits and pushes the updated Homebrew formula to the tap repository."""
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))  # Go to root directory
    subprocess.run(["git", "add", FORMULA_PATH], check=True)
    subprocess.run(["git", "commit", "-m", f"Update formula for v{version}"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(f"Pushed updated formula for v{version} to Homebrew tap")

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

    # Step 2: Create a new git tag
    create_git_tag(new_version)

    # Step 3: Create GitHub release
    create_github_release(new_version)

    # Step 4: Download tarball and generate SHA256
    tarball = download_tarball(new_version)
    sha256 = generate_sha256(tarball)

    # Step 5: Update the Homebrew formula
    update_homebrew_formula(new_version, sha256)

    # Step 6: Commit and push the updated formula to the Homebrew tap
    commit_and_push_formula(new_version)

    # Clean up the tarball
    os.remove(tarball)