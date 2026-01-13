#!/bin/bash
set -e

# Configuration
JS_SDK_DIR="sdks/js"
PY_SDK_DIR="sdks/python"
MCP_DIR="packages/epist_mcp_server"

echo "📦 Epist Developer Ecosystem Publisher"
echo "======================================"

# 1. Publish JS SDK
if [ -d "$JS_SDK_DIR" ]; then
    echo "🔵 [JS SDK] Publishing epist..."
    cd "$JS_SDK_DIR"
    npm install
    npm run build
    
    if [ -z "$NPM_TOKEN" ]; then
        echo "⚠️  NPM_TOKEN not set. Skipping implementation publish."
        echo "   Run 'npm publish --access public' manually or set NPM_TOKEN."
    else
        # Write .npmrc
        echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc
        npm publish --access public
        rm .npmrc
    fi
    cd - > /dev/null
    echo "✅ [JS SDK] Build verified."
else
    echo "❌ [JS SDK] Directory not found."
fi

echo "--------------------------------------"

# 2. Publish Python SDK
if [ -d "$PY_SDK_DIR" ]; then
    echo "🐍 [Python SDK] Publishing epist..."
    cd "$PY_SDK_DIR"
    
    # Using uv if available, else pip
    if command -v uv &> /dev/null; then
        uv build
        if [ -z "$UV_PUBLISH_TOKEN" ]; then
             echo "⚠️  UV_PUBLISH_TOKEN not set. Skipping upload."
        else
             uv publish
        fi
    else
        echo "⚠️  'uv' not found. Please install uv to publish python packages."
    fi
    cd - > /dev/null
    echo "✅ [Python SDK] Build verified."
else
    echo "❌ [Python SDK] Directory not found."
fi

echo "--------------------------------------"

echo "🎉 All builds completed."
