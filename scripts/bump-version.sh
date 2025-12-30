#!/bin/bash

# Trix Python SDK Version Bump Script
# Usage: ./scripts/bump-version.sh [major|minor|patch]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if bump type is provided
if [ $# -eq 0 ]; then
    print_error "No bump type specified"
    echo "Usage: $0 [major|minor|patch]"
    echo ""
    echo "  major: 1.0.0 → 2.0.0 (breaking changes)"
    echo "  minor: 1.0.0 → 1.1.0 (new features, backward compatible)"
    echo "  patch: 1.0.0 → 1.0.1 (bug fixes, backward compatible)"
    exit 1
fi

BUMP_TYPE=$1

# Validate bump type
if [[ ! "$BUMP_TYPE" =~ ^(major|minor|patch)$ ]]; then
    print_error "Invalid bump type: $BUMP_TYPE"
    echo "Valid options: major, minor, patch"
    exit 1
fi

# Get current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SDK_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$SDK_ROOT"

# Check if git working tree is clean
if [ -n "$(git status --porcelain)" ]; then
    print_error "Working directory is not clean. Commit or stash changes first."
    git status --short
    exit 1
fi

# Check if on main or master branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ ! "$CURRENT_BRANCH" =~ ^(main|master)$ ]]; then
    print_error "Not on main/master branch. Current branch: $CURRENT_BRANCH"
    echo "Switch to main/master branch before releasing."
    exit 1
fi

# Extract current version from pyproject.toml
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)

if [ -z "$CURRENT_VERSION" ]; then
    print_error "Could not extract current version from pyproject.toml"
    exit 1
fi

print_info "Current version: $CURRENT_VERSION"

# Split version into major.minor.patch
IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR="${VERSION_PARTS[0]}"
MINOR="${VERSION_PARTS[1]}"
PATCH="${VERSION_PARTS[2]}"

# Calculate new version
case $BUMP_TYPE in
    major)
        NEW_MAJOR=$((MAJOR + 1))
        NEW_MINOR=0
        NEW_PATCH=0
        ;;
    minor)
        NEW_MAJOR=$MAJOR
        NEW_MINOR=$((MINOR + 1))
        NEW_PATCH=0
        ;;
    patch)
        NEW_MAJOR=$MAJOR
        NEW_MINOR=$MINOR
        NEW_PATCH=$((PATCH + 1))
        ;;
esac

NEW_VERSION="$NEW_MAJOR.$NEW_MINOR.$NEW_PATCH"

print_info "New version: $NEW_VERSION"

# Confirm with user
echo ""
read -p "Bump version from $CURRENT_VERSION to $NEW_VERSION? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Version bump cancelled"
    exit 0
fi

# Update pyproject.toml
print_info "Updating pyproject.toml..."
sed -i "s/^version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml

# Update __init__.py
print_info "Updating src/trix/__init__.py..."
sed -i "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" src/trix/__init__.py

# Update CHANGELOG.md
print_info "Updating CHANGELOG.md..."
CURRENT_DATE=$(date +%Y-%m-%d)

# Add new version section to CHANGELOG
sed -i "/## \[Unreleased\]/a\\
\\
## [$NEW_VERSION] - $CURRENT_DATE\\
\\
### Added\\
- \\
\\
### Changed\\
- \\
\\
### Fixed\\
- " CHANGELOG.md

# Update comparison links
sed -i "s|\[Unreleased\]:.*|\[Unreleased\]: https://github.com/trix/trix-python-sdk/compare/v$NEW_VERSION...HEAD\n[$NEW_VERSION]: https://github.com/trix/trix-python-sdk/releases/tag/v$NEW_VERSION|" CHANGELOG.md

# Create git commit
print_info "Creating git commit..."
git add pyproject.toml src/trix/__init__.py CHANGELOG.md
git commit -m "chore: bump version to $NEW_VERSION"

# Create git tag
print_info "Creating git tag v$NEW_VERSION..."
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"

# Push to remote
print_info "Pushing to remote..."
git push origin "$CURRENT_BRANCH"
git push origin "v$NEW_VERSION"

print_success "Version bumped to $NEW_VERSION and tagged as v$NEW_VERSION"
print_info "GitHub Actions will now build and publish the release automatically"
print_info "Monitor the release at: https://github.com/trix/trix-python-sdk/actions"

echo ""
print_info "Don't forget to update the CHANGELOG.md with actual changes for this release!"
