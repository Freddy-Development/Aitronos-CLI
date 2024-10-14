#!/bin/bash

# Exit the script if any command fails
set -e

# Check for version type argument (patch, minor, or major)
if [ -z "$1" ]; then
  echo "Error: No version type specified. Usage: ./release_homebrew.sh [patch|minor|major]"
  exit 1
fi

VERSION_TYPE=$1
REPO="yourusername/aitronos-cli"
FORMULA_REPO="yourusername/homebrew-aitronos-cli"

# 1. Update the version number in setup.py
echo "Updating the version number..."
python3 update_version.py "$VERSION_TYPE"
VERSION=$(grep "version=" setup.py | sed "s/version='\(.*\)',/\1/")  # Extract version from setup.py
TAR_FILENAME="v$VERSION.tar.gz"

# 2. Create a new git tag for the new version
echo "Creating a new git tag for version $VERSION..."
git tag "v$VERSION"
git push origin "v$VERSION"

# 3. Create a GitHub release for the new version
echo "Creating a new GitHub release..."
gh release create "v$VERSION" --title "v$VERSION" --notes "Release v$VERSION"

# 4. Download the release tarball
echo "Downloading release tarball..."
curl -L -o "$TAR_FILENAME" "https://github.com/$REPO/archive/refs/tags/v$VERSION.tar.gz"

# 5. Generate the SHA256 hash of the tarball
echo "Generating SHA256 hash..."
SHA256=$(shasum -a 256 "$TAR_FILENAME" | awk '{ print $1 }')
echo "SHA256: $SHA256"

# 6. Update the Homebrew formula with the new version and hash
echo "Updating the Homebrew formula..."
sed -i '' "s|url .*|url \"https://github.com/$REPO/archive/v$VERSION.tar.gz\"|" Formula/aitronos.rb
sed -i '' "s|sha256 .*|sha256 \"$SHA256\"|" Formula/aitronos.rb

# 7. Commit and push the changes to the Homebrew tap repository
echo "Committing and pushing the updated formula..."
cd ../homebrew-aitronos-cli  # Make sure you're in the right tap directory
git add Formula/aitronos.rb
git commit -m "Update formula for v$VERSION"
git push origin main

# 8. Cleanup the downloaded tarball
echo "Cleaning up..."
rm "$TAR_FILENAME"

echo "Release process complete for version $VERSION!"