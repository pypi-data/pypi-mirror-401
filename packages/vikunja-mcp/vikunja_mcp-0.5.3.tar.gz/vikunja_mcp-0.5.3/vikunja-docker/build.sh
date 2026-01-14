#\!/bin/bash
set -e

# Build the Vikunja + Auth Bridge Docker image

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Building Vikunja + Auth Bridge..."

# Files are already in build context (connect.html and matrix-connect.html)

# Build
docker build -t vikunja-auth-bridge "$SCRIPT_DIR"

echo ""
echo "Build complete\! Run with:"
echo ""
echo "  docker run -p 8080:80 \\"
echo "    -e VIKUNJA_SERVICE_PUBLICURL=http://localhost:8080 \\"
echo "    -e VIKUNJA_SERVICE_FRONTENDURL=http://localhost:8080 \\"
echo "    -v vikunja-data:/db \\"
echo "    vikunja-auth-bridge"
echo ""
echo "Then visit:"
echo "  http://localhost:8080/slack-connect?state=test123"
echo "  http://localhost:8080/matrix-connect?state=test456"
