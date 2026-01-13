#!/bin/bash
set -e

# Configuration
PACKAGE_DIR="packages/epist_mcp_server"

# Ensure we are in the project root
if [ ! -d "$PACKAGE_DIR" ]; then
    echo "Error: specific package directory '$PACKAGE_DIR' not found."
    echo "Please run this script from the project root."
    exit 1
fi

echo "📦 Preparing to publish epist-mcp-server..."

# Navigate to package directory
cd "$PACKAGE_DIR"

# Clean previous builds
echo "🧹 Cleaning old builds..."
rm -rf dist/

# Build
echo "🔨 Building package..."
uv build

# Publish
echo "🚀 Publishing to PyPI..."
if [ -z "$UV_PUBLISH_TOKEN" ]; then
    echo "⚠️  UV_PUBLISH_TOKEN is not set."
    echo "   Please export UV_PUBLISH_TOKEN='pypi-...' and run again."
    echo "   Or run: uv publish --token <your-token>"
    exit 1
else
    uv publish
fi

echo "✅ Published successfully!"
